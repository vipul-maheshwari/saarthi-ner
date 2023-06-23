import sys
import timeit
import pickle
import numpy as np
import tensorflow as tf
import os
import json
from transformers import AutoTokenizer

from utilities.general import get_labels
from utilities.math_funcs import softmax
from postprocessing.main import postprocess_entities


def init():
    global max_seq_len
    global label_map
    global pretrained_tokenizer
    global distil_tokenizer
    global model

    max_seq_len = 24
    root_dir = "/Users/shubhamchaurasia/Downloads/Deployment_Models/ner_model/model_40/ner_"

    with open(os.path.join(root_dir, 'label_map.json'), 'r', encoding='utf8') as f:
        label_map = json.load(f)
    
    with open(os.path.join(root_dir, 'tokenizer.pickle'), 'rb') as f:
        distil_tokenizer = pickle.load(f)

    pretrained_tokenizer = AutoTokenizer.from_pretrained('jplu/tf-xlm-roberta-base')
    model = tf.keras.models.load_model(os.path.join(root_dir, 'saved_model_distil'), compile=False)
    # model = ort.InferenceSession('../../outputs/model.onnx')


def inference(text, lang = "hindi"):
    print(f'Hit with text: {text}')
    tokens = pretrained_tokenizer.tokenize(text)
    pure_length = len(tokens)
    tokens = ['<s>'] + tokens[:max_seq_len - 2] + ['</s>']
    pad_len = max_seq_len - len(tokens)
    tokens = tokens + ['<pad>'] * pad_len
    model_in = [distil_tokenizer.word_index.get(token, 1) for token in tokens]
    model_in = np.array([model_in], dtype=np.int32)
    lower_eighth = chr(9601)
    indices = [idx for idx, token in enumerate(tokens) if token.startswith(lower_eighth)]

    # outs = model.run(None, {'input': model_in})

    outs = model(model_in)

    # outs = {'ner': outs[1]}
    entity_range = pure_length + 1 if pure_length + 1 < max_seq_len else max_seq_len
    outs['ner'] = np.array([outs['ner'][0][index] for index in range(entity_range)])
    probs = {'ner': np.array([softmax(token) for token in outs['ner']])}
    output =  {'ner': [label_map['ner'][np.argmax(token)] for token in probs['ner']]}
    post_processed_ner_tags = [tag for idx, tag in enumerate(output['ner']) if idx in indices]
    output['ner_tags'] = post_processed_ner_tags
    # print(f'Tags: {output["ner_tags"]}')
    output['ner'] = postprocess_entities(text, output['ner_tags'])

    return {
        "text": text,
        "entities": [{"entity": "date", "extractor": "saarthi-ner", "value": value, "tags": tags} for value, tags in zip(output['ner'], [output['ner_tags']]) if value != "none"]
    }


if __name__=='__main__':
    # print(timeit.repeat(setup="setup()", stmt="inference('दे दूंगा मै दो दिनों में पैसे')", number=1, repeat=5, globals=globals()))
    init()
    print(inference('7ই সেপ্টেম্বর পর্যন্ত আমাকে সময় দিন'))

def run(raw_data):
    # raw_data = raw_data
    # print(type(raw_data))
    text = raw_data['data']
    date = None
    lang = 'hindi'
    if 'date' in raw_data:
        date = raw_data['date']
    if 'lang' in raw_data:
        lang = raw_data['lang']

    return inference(text, lang)