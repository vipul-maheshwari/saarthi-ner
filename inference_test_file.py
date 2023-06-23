import sys
import timeit
import pickle
import numpy as np
import tensorflow as tf
# import onnxruntime as ort
from transformers import AutoTokenizer

from utilities.general import get_labels
from utilities.math_funcs import softmax
from postprocessing.main import postprocess_entities

import requests
from tqdm import tqdm
import pytz
from datetime import datetime as Date
import pandas as pd
import ast
import os
import json

def setup():
    global max_seq_len
    global label_map
    global pretrained_tokenizer
    global distil_tokenizer
    global model

    max_seq_len = 24
    root_dir = "/Users/shubhamchaurasia/Downloads/Deployment_Models/ner_model/model_39/ner_"

    with open(os.path.join(root_dir, 'label_map.json'), 'r', encoding='utf8') as f:
        label_map = json.load(f)
    
    with open(os.path.join(root_dir, 'tokenizer.pickle'), 'rb') as f:
        distil_tokenizer = pickle.load(f)

    pretrained_tokenizer = AutoTokenizer.from_pretrained('jplu/tf-xlm-roberta-base')
    model = tf.keras.models.load_model(os.path.join(root_dir, 'saved_model_distil'), compile=False)
    # model = ort.InferenceSession('../outputs/model.onnx')


def inference(text, current_date=None, language = "hindi"):
    # print(f'Hit with text: {text}')
    tokens = pretrained_tokenizer.tokenize(text)
    pure_length = len(tokens)
    tokens = ['<s>'] + tokens[:max_seq_len - 2] + ['</s>']
    pad_len = max_seq_len - len(tokens)
    tokens = tokens + ['<pad>'] * pad_len
    model_in = [distil_tokenizer.word_index.get(token, 1) for token in tokens]
    model_in = np.array([model_in], dtype=np.int32)
    lower_eighth = chr(9601)
    indices = [idx for idx, token in enumerate(tokens) if token.startswith(lower_eighth)]
    # for idx, token in enumerate(tokens):
    #     if token.startswith(chr(9601)):
    #         indices.append(idx)

    outs = model(model_in)

    # outs = {'ner': outs[1]}
    entity_range = pure_length + 1 if pure_length + 1 < max_seq_len else max_seq_len
    outs['ner'] = np.array([outs['ner'][0][index] for index in range(entity_range)])
    probs = {'ner': np.array([softmax(token) for token in outs['ner']])}
    output =  {'ner': [label_map['ner'][np.argmax(token)] for token in probs['ner']]}
    post_processed_ner_tags = [tag for idx, tag in enumerate(output['ner']) if idx in indices]
    output['ner_tags'] = post_processed_ner_tags
    # print(f'Tags: {output["ner_tags"]}')
    output['ner'] = postprocess_entities(text, output['ner_tags'], current_date=current_date, lang = language)

    # return {
    #     "text": text,
    #     "entities": [{"entity": "date", "extractor": "saarthi-ner", "value": output["ner"]["date"][0], "tags": tags} for value, tags in zip(output['ner'], [output['ner_tags']]) if value != "none"]
    # }
    return output["ner"]

def convert_date_time_format(date, current_format = "%Y-%m-%d %H:%M:%S", required_format = "%d/%m/%Y %H:%M:%S"):
    try:
        updated_date = Date.strptime(date, current_format)
        return Date.strftime(updated_date, required_format)
    except Exception as ex:
        return None

if __name__=='__main__':
    setup()
    df = pd.read_csv('/Users/shubhamchaurasia/Documents/NER/saarthi_ner/testing_data/combined_testing_data_ner.csv')
    lang = "hindi"
    text = df["text"]
    language = df["language"]
    date = df["created_at"].apply(convert_date_time_format)

    ner_date, ner_time = [], []
    for i in tqdm(range(len(df))):
        response = inference(str(text[i]), date[i], language[i])
        if len(response["date"]) == 0:
            ner_date.append("none")
        else:
            ner_date.append(response["date"][0])
        if len(response["time"]) == 0:
            ner_time.append("none")
        else:
            ner_time.append(response["time"][0])

    df1 = pd.DataFrame()
    df1["Text"] = text
    df1["Reference_Date"] = date
    df1["NER2.0 Date"] = ner_date
    df1["NER2.0 Time"] = ner_time
    # print(ner_date)
    df1.to_csv("/Users/shubhamchaurasia/Documents/NER/saarthi_ner/testing_data/combined_testing_data_ner_predictions.csv", index = False)
