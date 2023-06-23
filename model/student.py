import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.layers import Input, Dropout, Dense

from model.base import ModelBase
from model.layers import get_output_layers, get_embedding_layer, get_bilstm_layer

from losses.getters import get_losses
from metrics.getters import get_metrics


class BiLSTMModel(ModelBase):
    """BiLSTM student model wrapper class

    Args:
        max_seq_len (int): Maximum length of sequence to process.
        word_index (): Word to index mapping.
        word_emb (): Dictionary containing word to embedding vector mapping.
        lstm_hidden_size (): LSTM hidden dimension.
        dense_hidden_size (): Dense layer hidden size.
        dense_act_func (): Dense layer activation function.
        dropout_rate (): Dropout probability.
        strategy (tf.distribute.Strategy): Tensorflow training strategy.

    Inherits from:
        ModelBase
    """

    def __init__(
        self,
        max_seq_len,
        word_index,
        word_emb,
        lstm_hidden_size,
        dense_hidden_size,
        dense_act_func,
        dropout_rate,
        strategy,
        logger_name
    ):
        super().__init__(max_seq_len, strategy, logger_name)

        self.word_index = word_index
        self.word_emb = word_emb
        self.lstm_hidden_size = lstm_hidden_size
        self.dense_hidden_size = dense_hidden_size
        self.dense_act_func = dense_act_func
        self.dropout_rate = dropout_rate

        self.model_in = Input(shape=(self.max_seq_len,), dtype="int32", name="input")
        self.lstm_features, self.sequence_out = self.get_lstm_out(self.model_in)
        # self.lstm_features = self.get_lstm_out(self.model_in)

    def get_stage1_model(self):
        """Returns model for stage 1 of distillation.

        Returns:
            tf.keras.Model: LSTM student model compiled for stage 1 distillation.
        """
        with self.strategy.scope():
            model = Model(inputs=self.model_in, outputs=self.lstm_features)
            model.compile(optimizer=tf.keras.optimizers.Adam(), loss=['mse'], metrics=['mse'])

        return model

    def get_stage2_model(self, s1model, shared_layers, classes, multi_columns):
        """Returns model for stage 2 (and greater) distillation.

        Args:
            classes (dict): Dictionary containing classes mapped to their possible values.
            multi_columns (list): List of strings containing names of the classes that are multilabel targets.

        Returns:
            tf.keras.Model: LSTM student model for stage 2 (and greater) distillation.
        """
        # TODO: Add the sequence output head.
        with self.strategy.scope():
            x = Dropout(self.dropout_rate)(self.lstm_features)
            outputs = get_output_layers(x, self.sequence_out, classes)
            model = Model(inputs=self.model_in, outputs=outputs)
 
            self.logger.info("Copying stage 1 weights")

            for layer in shared_layers:
                model.get_layer(layer).set_weights(s1model.get_layer(layer).get_weights())
                model.get_layer(layer).trainable = False
            
            losses = [MeanSquaredError(name=classname) for classname, _ in classes.items()]
            model.compile(optimizer=tf.keras.optimizers.Adam(), loss=losses, metrics=losses)

        return model

    def compile_transfer_logits_model(self, s2model, shared_layers, stage, classes):
        """[summary]

        Args:
            s2model ([type]): [description]
            shared_layers ([type]): [description]
            stage ([type]): [description]
            classes ([type]): [description]

        Returns:
            [type]: [description]
        """        
        self.logger.info(f'Unfreezing layer {shared_layers[stage - 3]}')
        with self.strategy.scope():
            s2model.get_layer(shared_layers[stage - 3]).trainable = True

            losses = [MeanSquaredError(name=classname) for classname, _ in classes.items()]
            s2model.compile(optimizer=tf.keras.optimizers.Adam(), loss=losses, metrics=losses)

        return s2model

    def compile_labelled_ce_model(self, prev_model, shared_layers, classes, multi_columns):
        """[summary]

        Args:
            prev_model ([type]): [description]
            shared_layers ([type]): [description]
            classes ([type]): [description]
            multi_columns ([type]): [description]

        Returns:
            [type]: [description]
        """        
        for layer in shared_layers:
            prev_model.get_layer(layer).trainable = False
        
        losses = get_losses(classes)
        metrics = get_metrics(classes)
        
        with self.strategy.scope():
            prev_model.compile(optimizer=tf.keras.optimizers.Adam(), loss=losses, metrics=metrics)

        return prev_model
    
    def compile_labelled_e2e_ce_model(self, prev_model, shared_layers, classes, multi_columns, stage):
        """[summary]

        Args:
            prev_model ([type]): [description]
            shared_layers ([type]): [description]
            classes ([type]): [description]
            multi_columns ([type]): [description]
            stage ([type]): [description]

        Returns:
            [type]: [description]
        """        
        self.logger.info(f'Unfreezing layer {shared_layers[stage - 4 - len(shared_layers)]}')
        prev_model.get_layer(shared_layers[stage - 4 - len(shared_layers)]).trainable = True

        losses = get_losses(classes)
        metrics = get_metrics(classes)

        with self.strategy.scope():
            prev_model.compile(tf.keras.optimizers.Adam(), loss=losses, metrics=metrics)

        return prev_model
    
    def get_shared_layers(self):
        """[summary]

        Returns:
            [type]: [description]
        """        
        with self.strategy.scope():
            model = self.get_stage1_model()

        # Get shared layers for student models
        shared_layers = []
        for layer in model.layers:
            if len(layer.trainable_weights) > 0:
                shared_layers.append(layer.name)
        # Update parameters top down from the shared layers
        shared_layers.reverse()

        return shared_layers

    def get_lstm_out(self, inp):
        """Returns the output from the LSTM feature extractor.

        Args:
            inp ([type]): Model inputs from the keras Input layer.

        Returns:
            [type]: Outputs from the LSTM -> Dense layer.
        """
        with self.strategy.scope():
            emb_layer = get_embedding_layer(self.word_index, self.word_emb, self.strategy, self.max_seq_len)
            rnn_layer = get_bilstm_layer(units=self.lstm_hidden_size, layer_name="bilstm", strategy=self.strategy)
            dense_layer = Dense(
                self.dense_hidden_size, activation=self.dense_act_func, name="dense"
            )

            x = emb_layer(inp)
            x = Dropout(self.dropout_rate)(x)
            out = rnn_layer(x)
            sequence_out = out[0]
            x = tf.concat([out[1], out[2]], 1)
            # x = rnn_layer(x)
            x = Dropout(self.dropout_rate)(x)
            x = dense_layer(x)

        return x, sequence_out
