import tensorflow as tf
from .NERloss import CustomNonPaddingTokenLoss


def get_losses(classes):
    """Returns a dictionary containing all the losses required for training.

    Args:
        classes (dict): Label map.
        multi_columns (list): List of strings containing names of the classes that are multilabel targets.

    Returns:
        dict: Dictionary containing relevant losses for all targets.
    """
    losses = {}
    for classname, _ in classes.items():
        if classname == 'ner':
            losses[classname] = get_ner_loss()
        else:
            losses[classname] = get_single_output_loss()

    return losses


def get_single_output_loss():
    """[summary]

    Returns:
        [type]: [description]
    """
    return tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)


def get_ner_loss():
    """_summary_

    Returns:
        _type_: _description_
    """    
    return CustomNonPaddingTokenLoss(name='ner_loss')