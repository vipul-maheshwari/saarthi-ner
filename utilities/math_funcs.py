import numpy as np
import tensorflow as tf


def gelu(x):
    """Gaussian Error Linear Unit.

  This is a smoother version of the RELU.
  Original paper: https://arxiv.org/abs/1606.08415
  Args:
    x: float Tensor to perform activation.

  Returns:
    `x` with the GELU activation applied.
  """
    cdf = 0.5 * (1.0 + tf.tanh((np.sqrt(2 / np.pi) * (x + 0.044715 * tf.pow(x, 3)))))
    return x * cdf


def softmax(x, axis=0):
    """Softmax function

    Args:
        x (float Iterable): Input to perform activation

    Returns:
        numpy.ndarray: Numpy array with softmax applied on the innermost vectors
    """
    return np.exp(x) / np.sum(np.exp(x), axis=axis)


def sigmoid(x):
  """Softmax function

    Args:
        x (float Iterable): Input to perform activation

    Returns:
        numpy.ndarray: Numpy array with softmax applied on the innermost vectors
  """
  return 1 / (1 + np.exp(x))