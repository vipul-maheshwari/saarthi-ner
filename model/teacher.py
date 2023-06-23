import sys
import numpy as np
from sklearn.decomposition import PCA

import tensorflow as tf
from tensorflow.keras import Model
from tensorflow.keras.layers import Input, Dense, Dropout
from transformers import TFAutoModel, AutoTokenizer, AutoConfig

from .base import ModelBase
from .layers import get_output_layers

from losses.getters import get_losses
from metrics.getters import get_metrics


class Teacher(ModelBase):
    """Wrapper class for teacher model.

    Args:
        model_name (str): Name of the teacher model to initialize. Can be one of the following: bert, distil-bert, roberta, xlm-roberta, albert
        max_seq_len (int):
        strategy (tf.distribute.Strategy): 
    """

    def __init__(self, model_name, max_seq_len, strategy, logger_name):
        super().__init__(max_seq_len, strategy, logger_name)
        self.checkpoints = {
            "bert": "bert-base-uncased",
            "distil-bert": "distilbert-base-uncased",
            "roberta": "roberta-base",
            "xlm-roberta": "jplu/tf-xlm-roberta-base",
            "albert": "albert-base-v2",
            'muril': 'google/muril-base-cased'
        }
        self.checkpoint = self.checkpoints[model_name]
        config = AutoConfig.from_pretrained(self.checkpoint, output_hidden_states=True)

        self.tokenizer = AutoTokenizer.from_pretrained(self.checkpoint)

        with self.strategy.scope():
            self.inputs = Input(shape=(self.max_seq_len,), dtype=tf.int32)
            self.encoder = TFAutoModel.from_pretrained(self.checkpoint, config=config)

    def get_finetuning_compiled_model(self, classes):
        """Returns teacher model compiled on Adam optimizer and relevant losses and metrics.

        Args:
            classes (dict): Dictionary containing classes mapped to their possible values.
            multi_column (list): List of strings containing names of the classes that are multilabel targets.

        Returns:
            tf.keras.Model: Model compiled for fine tuning.
        """
        with self.strategy.scope():
            model = self.get_finetuning_model(classes)
            losses = get_losses(classes)
            metrics = get_metrics(classes)

            model.compile(tf.keras.optimizers.Adam(), loss=losses, metrics=metrics)

        return model

    def get_intermediate_layer_model(self, layer):
        """Returns teacher model's intermediate layer made into a tf.keras.Model object.
 
        Args:
            layer (int): Layer number you want the output from.

        Returns:
            tf.keras.Model: Model whose output is the teacher's intermediate layer's logits.
        """
        with self.strategy.scope():
            embedding = self.encoder(self.inputs)[2][layer][:, 0]
            model = Model(inputs=self.inputs, outputs=embedding)
        return model

    def get_finetuning_model(self, classes):
        """Returns teacher model initialized from checkpoint.

        Returns:
            tf.keras.Model: Model configured for fine tuning.
        """
        with self.strategy.scope():
            encoder_outs = eval(f'self.encoder.{self.encoder.base_model_prefix}(self.inputs)')
            sequence_outs = encoder_outs[0]
            embedding = encoder_outs[1]
            outputs = get_output_layers(embedding, sequence_outs, classes)
            model = Model(inputs=self.inputs, outputs=outputs)

        return model

    def get_tokenizer(self):
        """Returns teacher model's tokenizer.

        Returns:
            HuggingFace tokenizer: Pretrained tokenizer
        """
        return self.tokenizer

    def get_special_tokens(self):
        """Returns a dictionary containing all the special tokens used by the teacher model.

        Returns:
            dict: Dictionary containing special tokens used by the teacher.
        """
        if hasattr(self.tokenizer, "pad_token"):
            pad_token = self.tokenizer.pad_token
        else:
            pad_token = "<pad>"
        if getattr(self.tokenizer, "name_or_path") in [self.checkpoints['bert'], self.checkpoints['muril']]:
            bos_token = self.tokenizer.cls_token
            eos_token = self.tokenizer.sep_token
        else:
            if hasattr(self.tokenizer, "bos_token"):
                bos_token = self.tokenizer.bos_token
            else:
                bos_token = "<s>"
            if hasattr(self.tokenizer, "eos_token"):
                eos_token = self.tokenizer.eos_token
            else:
                eos_token = "</s>"
        return {"eos_token": eos_token, "bos_token": bos_token, "pad_token": pad_token}

    def get_word_embeddings(self, word_emb_dim):
        """Applies PCA on the teacher's word embeddings and returns them.

        Args:
            word_emb_dim (int): Dimension word embedding dimension.

        Returns:
            dict: Dictionary mapping words to corresponding embedding vector.
        """
        if self.encoder.base_model_prefix == "bert":
            word_embedding_matrix = self.encoder.weights[0].numpy()
        elif self.encoder.base_model_prefix == "transformer":
            word_embedding_matrix = (
                self.encoder.transformer.embeddings.get_weights()[0]
            )
        elif self.encoder.base_model_prefix == "distilbert":
            word_embedding_matrix = (
                self.encoder.distilbert.embeddings.get_weights()[0]
            )
        elif self.encoder.base_model_prefix == "roberta":
            word_embedding_matrix = ( 
               self.encoder.roberta.embeddings.weight.numpy()
            )
        else:
            word_embedding_matrix = np.random.uniform(
                size=(len(self.tokenizer.get_vocab()), word_emb_dim)
            )
        # embedding factorization to reduce embedding dimension
        if word_embedding_matrix.shape[1] > word_emb_dim:
            pca = PCA(n_components=word_emb_dim)
            pca.fit(word_embedding_matrix)
            word_embedding_matrix = pca.transform(word_embedding_matrix)
            word_emb = dict(zip(self.tokenizer.get_vocab(), word_embedding_matrix))

        return word_emb

    def load_weights(self, path):
        self.encoder.load_weights(path)
