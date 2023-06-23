import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import (
    Embedding,
    LSTM,
    Bidirectional,
    Dense,
)


def get_output_layers(model_out, model_out_sequence, classes):
    """Returns a dict of all the output heads to be attached to the base model.

    Args:
        model_out ([type]): Last output from the model.
        classes (dict): Dictionary containing classes mapped to their possible values.
        multi_columns (list): List of strings containing names of the classes that are multilabel targets.

    Returns:
        dict: Dictionary containing dense layers corresponding to all the different outputs.
    """
    outputs = {}
    for classname, classvalues in classes.items():
        if classname == 'ner':
            outputs[classname] = Dense(units=len(classvalues), activation='linear', name=classname)(model_out_sequence)
            continue
        outputs[classname] = Dense(units=len(classvalues), activation='linear', name=classname)(model_out)

    return outputs


def get_single_output_layer(n_units, layer_name, model_out):
    """Returns output from single output target output heads.

    Args:
        n_units (int): Hidden size of layer.
        layer_name (str): Name of the layer.
        model_out ([type]): Last output from the model.

    Returns:
        [type]: Softmaxed output from the dense layer.
    """
    return Dense(units=n_units, activation="softmax", name=layer_name)(model_out)


def get_embedding_layer(word_index, word_emb, strategy, max_seq_len):
    """Returns embedding layer.

    Returns:
        tf.keras.layers.Embedding: Embedding layer consisting of the downscaled teacher embedding weights.
    """
    num_words = len(word_index)
    word_emb_dim = len(next(iter(word_emb.values())))

    with strategy.scope():
        embedding_matrix = np.zeros((num_words + 2, word_emb_dim))
        for word, i in word_index.items():
            embedding_vector = word_emb.get(word)
            if embedding_vector is not None:
                embedding_matrix[i] = embedding_vector
            else:
                embedding_matrix[i] = np.random.uniform(-0.1, 0.1, word_emb_dim)
        
        embedding_layer = Embedding(
            num_words + 2,
            word_emb_dim,
            weights=[embedding_matrix],
            input_length=max_seq_len,
            mask_zero=False,
            name="embedding_layer",
        )

    return embedding_layer

def get_bilstm_layer(units, layer_name, strategy):
    """Returns a bidirectional LSTM layer.

    Args:
        units (int): Hidden size of the LSTM layer.
        layer_name (str): Name of the layer.

    Returns:
        tf.keras.layers.Bidirectional: LSTM layer wrapped in the Bidirectional wrapper.
    """
    with strategy.scope():
        layer = Bidirectional(
            LSTM(
                units=units,
                recurrent_activation="sigmoid",
                activation="tanh",
                dropout=0.2,
                recurrent_dropout=0,
                return_sequences=True,
                return_state=True
            ),
            name=layer_name,
        )

    return layer


def get_single_output_layer(n_units, layer_name, model_out):
    """Returns output from single output target output heads.

    Args:
        n_units (int): Hidden size of layer.
        layer_name (str): Name of the layer.
        model_out ([type]): Last output from the model.

    Returns:
        [type]: Softmaxed output from the dense layer.
    """
    return Dense(units=n_units, activation="softmax", name=layer_name)(model_out)


def get_multi_output_layer(n_units, layer_name, model_out):
    """Returns output form multi output target output heads.

    Args:
        n_units (int): Hidden size of layer.
        layer_name (str): Name of the layer.
        model_out ([type]): Last output from the model.

    Returns:
        [type]: Sigmoid output from the dense layer.
    """
    return Dense(units=n_units, activation="sigmoid", name=layer_name)(model_out)


def get_dense_layer(dense_hidden_size, dense_act_func):
    """Returns a regular dense layer.

    Returns:
        tf.keras.layers.Dense: Regular dense layer.
    """
    dense_layer = Dense(dense_hidden_size, activation=dense_act_func, name="dense")
    return dense_layer
