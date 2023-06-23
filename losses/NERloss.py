# Source: https://keras.io/examples/nlp/ner_transformers/
import tensorflow as tf
from tensorflow.keras.losses import SparseCategoricalCrossentropy

class CustomNonPaddingTokenLoss(tf.keras.losses.Loss):
    def __init__(self, name="ner_loss"):
        super().__init__(name=name)

    def call(self, y_true, y_pred):
        loss_fn = SparseCategoricalCrossentropy(from_logits=True, reduction=tf.keras.losses.Reduction.NONE)
        loss = loss_fn(y_true, y_pred)
        # 0 and 1 are the indices of the padding token and X token respectively
        mask = tf.cast((y_true > 0), dtype=tf.float32)
        loss = loss * mask
        return tf.reduce_sum(loss) / tf.reduce_sum(mask)