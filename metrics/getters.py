import tensorflow as tf
# from .ner_metrics import NERF1


def get_metrics(classes):
    """Returns a dictionary containing all the metrics required for evaluation.

    Args:
        classes (dict): Label map.
        multi_columns (list): List of strings containing names of the classes that are multilabel targets.

    Returns:
        dict: Dictionary containing relevant metrics for all targets.
    """
    metrics = {}
    for classname, _ in classes.items():
        if classname == 'ner':
            metrics[classname] = get_ner_metric(classes['ner'])
        else:
            metrics[classname] = get_single_output_metric()

    return metrics


def get_single_output_metric():
    """[summary]

    Returns:
        [type]: [description]
    """        
    return tf.keras.metrics.SparseCategoricalAccuracy('accuracy')


def get_ner_metric(label_list):
    """_summary_

    Returns:
        _type_: _description_
    """
    # return NERF1(label_list)
    return tf.keras.metrics.SparseCategoricalAccuracy('ner_acc')
    # return F1Score(num_classes=len(label_list), threshold=0.5, average='micro')
