import os
import json
import logging
import numpy as np
import tensorflow as tf
import pickle5 as pickle
from transformers import AutoTokenizer

from utilities.math_funcs import softmax
from postprocessing.main import postprocess_entities


def inference(text, date=None, lang='hindi'):
    tokens = pretrained_tokenizer.tokenize(text)
    pure_length = len(tokens)
    tokens = ['<s>'] + tokens[:max_seq_len - 2] + ['</s>']
    pad_len = max_seq_len - len(tokens)
    tokens = tokens + ['<pad>'] * pad_len
    model_in = [distil_tokenizer.word_index.get(token, 1) for token in tokens]
    model_in = np.array([model_in])
    lower_eighth = chr(9601)
    indices = [idx for idx, token in enumerate(tokens) if token.startswith(lower_eighth)]

    outs = model(model_in)
    entity_range = pure_length + 1 if pure_length + 1 < max_seq_len else max_seq_len
    outs['ner'] = np.array([outs['ner'][0][index] for index in range(entity_range)])
    probs = {'ner': np.array([softmax(token) for token in outs['ner']])}
    output =  {'ner': [label_map['ner'][np.argmax(token)] for token in probs['ner']]}
    post_processed_ner_tags = [tag for idx, tag in enumerate(output['ner']) if idx in indices]
    output['ner_tags'] = post_processed_ner_tags
    output['ner'] = postprocess_entities(text, output['ner_tags'], date, lang)

    entity_output = []
    for entity_type, entity_values in output['ner'].items():
        for value in entity_values:
            entity_output.append({
                'entity': entity_type,
                'extractor': 'saarthi-ner',
                'value': value
            })

    return {
        "text": text,
        "entities": entity_output,
        "tags": output['ner_tags']
    }


def init():
    global model
    global label_map
    global pretrained_tokenizer
    global distil_tokenizer
    global max_seq_len
    global logger

    logger = logging.getLogger('azure-inf')
    root_dir = os.getenv('AZUREML_MODEL_DIR') +"/outputs"

    max_seq_len = 24

    with open(os.path.join(root_dir, 'label_map.json'), 'r', encoding='utf8') as f:
        label_map = json.load(f)
    
    with open(os.path.join(root_dir, 'tokenizer.pickle'), 'rb') as f:
        distil_tokenizer = pickle.load(f)

    pretrained_tokenizer = AutoTokenizer.from_pretrained('jplu/tf-xlm-roberta-base')
    model = tf.keras.models.load_model(os.path.join(root_dir, 'saved_model_distil'), compile=False)


def run(raw_data):
    text = raw_data
    date = None
    lang = 'hindi'

    return inference(text, date, lang)
