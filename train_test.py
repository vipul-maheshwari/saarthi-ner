import sys
import json
# import tf2onnx
import numpy as np
import pandas as pd
import tensorflow as tf
from sklearn.model_selection import train_test_split

from model.teacher import Teacher
from utilities.math_funcs import gelu
from training.trainer import TeacherTrainer, Distiller
from utilities.general import get_labels, remove_special_characters_df

ner_tagged_parsed_path = "./inputs/ner_tagged_parsed.json"
ner_labels_file_path = "./inputs/ner_labels.csv"
intent_file_path = "./inputs/data.csv"
transfer_file_path = "./inputs/transfer.csv"

label_map = get_labels(ner_labels_file_path)

with open(ner_tagged_parsed_path, 'r') as f:
    data_json = json.load(f)

text = []
intent = []
ner = []

for sample in data_json:
    text.append(sample['text'])
    intent.append(sample['intent'])
    ner.append(sample['ner'])

data = pd.DataFrame({'text': text, 'label': intent, 'ner': ner})
ner_data = remove_special_characters_df(ner_data)
train_ner, dev_ner = train_test_split(ner_data, test_size=0.1, random_state=43)

intent_data = pd.read_csv(intent_file_path)
intent_data = remove_special_characters_df(intent_data)
train_intent, dev_intent = train_test_split(intent_data, test_size=0.1, random_state=43)

transfer = pd.read_csv(transfer_file_path)
print(f'Train data: {len(train_ner)}')
print(f'Validation data: {len(dev_ner)}')
print(f'Transfer data: {len(transfer)}')

strategy = tf.distribute.MirroredStrategy()
teacher = Teacher('xlm-roberta', 24, strategy, 'teacher-factory')
trainer = TeacherTrainer(train_intent, label_map, teacher, strategy, 128, 80, 24, '../outputs', 'trainer', dev_set=dev_intent)
trainer.run_training()
finetuned_teacher = trainer.get_finetuned_model()
# finetuned_teacher = tf.keras.models.load_model('../outputs/saved_model_teacher', compile=False)

student_config = {
    'word_emb_dim': 300,
    'lstm_hidden_size': 600,
    'dense_hidden_size': 768,
    'dense_act_func': gelu,
    'dropout': 0.2
}
distiller = Distiller(ner_data, transfer, label_map, teacher, finetuned_teacher, strategy, 512, 200, 300000, 24, student_config, '../outputs', 'distiller')
distilled = distiller.run_training()

spec = (tf.TensorSpec((None, 24), tf.int32, name='input'),)
model_proto, _ = tf2onnx.convert.from_keras(distilled, input_signature=spec, opset=13, output_path='../outputs/model.onnx')
output_names = [n.name for n in model_proto.graph.output]
print(output_names)
