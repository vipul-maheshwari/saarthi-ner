import numpy as np
import tensorflow as tf
from tensorflow.keras.callbacks import EarlyStopping

from callbacks.schedulers import CosineLRSchedule, OneCycleScheduler, create_learning_rate_scheduler


def get_cosine_scheduler(lr_high, lr_low):
    """Returns a cosine learning rate scheduler.

    Args:
        lr_high (float): Highest value of the learning rate.
        lr_low (float): Lowest value of the learning rate.

    Returns:
        tf.keras.callbacks.LearningRateScheduler: Cosine Scheduler
    """
    return tf.keras.callbacks.LearningRateScheduler(
        CosineLRSchedule(lr_high=lr_high, lr_low=lr_low), verbose=1
    )


def get_one_cycle_scheduler(lr, epochs, batch_size, train_size):
    """Returns a one cycle learning rate scheduler.

    Args:
        lr (float): Value of the learning rate.
        epochs (int): Number of epochs to train on.
        batch_size (int): Batch size for training.
        train_size (int): Size of the teacher transfer texts.

    Returns:
        OneCycleScheduler object: One cycle learning rate scheduler.
    """
    steps = np.ceil(train_size / batch_size) * epochs
    sch = OneCycleScheduler(lr, steps)
    return sch


def get_custom_lr_scheduler(epochs):
    """Returns learning rate scheduler callback.

    Args:
        epochs (int): Number of training epochs.

    Returns:
        tf.keras.callbacks.LearningRateScheduler: LR scheduler keras callback.
    """
    return create_learning_rate_scheduler(
        max_learn_rate=1e-4,
        end_learn_rate=1e-7,
        warmup_epoch_count=10,
        total_epoch_count=epochs,
    )

def get_early_stopping(patience=10):
    """Returns an early stopping keras callback.

    Args:
        patience (int, optional): Amount of epochs to wait before stopping training. Defaults to 10.

    Returns:
        tf.keras.callbacks.EarlyStopping: Early stopping keras callback.
    """
    return EarlyStopping(
        monitor="val_loss", patience=patience, restore_best_weights=True, verbose=1
    )