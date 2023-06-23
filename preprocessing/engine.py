import os
import sys
import pickle
import logging
import numpy as np
from abc import ABC, abstractmethod
from tensorflow.keras.preprocessing.text import Tokenizer

from utilities.general import convert_to_unicode


class PreprocessingEngineBase(ABC):
    """Base class for all preprocessing engines. Preprocessing engines contain the main preprocessing logic.

    Args:
        max_seq_len (int): Maximum permissible length of the input text (counted in terms of the number of tokens the text gets tokenized into)
        special_tokens (dict): Dictionary containing beginning of sequence, end of sequence, and padding tokens
        pretrained_tokenizer (Hugging Face Tokenizer): Pretrained hugging face tokenizer of teacher model
        logger_name (str): Name of the logger object.
    """

    def __init__(self, max_seq_len, special_tokens, pretrained_tokenizer, label_map, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        self.max_seq_len = max_seq_len
        self.pretrained_tokenizer = pretrained_tokenizer
        self.special_tokens = special_tokens
        self.label_map = label_map

    def tokenize_and_pad_to_max(self, text, return_len=False):
        """Tokenizes input text, pads it to the maximum sequence length and returns it.

        Args:
            text (str): Input raw text.

        Returns:
            List[str]: List of tokens padded to `max_seq_len`.
        """
        text = convert_to_unicode(text)
        tokens = self.pretrained_tokenizer.tokenize(text)
        token_length = len(tokens)
        tokens = self.pad_to_max(tokens)

        if return_len:
            return tokens, token_length

        return tokens

    def pad_to_max(self, tokens):
        if len(tokens) > self.max_seq_len - 2:
            tokens = tokens[: self.max_seq_len - 2]
            tokens.insert(0, self.special_tokens["bos_token"])
            tokens.extend([self.special_tokens["eos_token"]])
        else:
            diff = self.max_seq_len - 2 - len(tokens)
            tokens = (
                [self.special_tokens["bos_token"]]
                + tokens
                + [self.special_tokens["eos_token"]]
                + [self.special_tokens["pad_token"]] * diff
            )

        return tokens

    @abstractmethod
    def run(self):
        """Runs the base preprocessing logic.
        """


class TeacherPreprocessingEngine(PreprocessingEngineBase):

    def __init__(self, max_seq_len, special_tokens, pretrained_tokenizer, label_map, logger_name):
        super().__init__(max_seq_len, special_tokens, pretrained_tokenizer, label_map, logger_name)
        self.special_tokens = {k: self.pretrained_tokenizer.convert_tokens_to_ids(v) for k, v in self.special_tokens.items()}

    def run(self, input_data):
        X, y = self.ner_preproc(input_data)
    
        return X, y

    def preproc(self, input_data):
        X = []
        y = []

        for _, row in input_data.iterrows():
            ids = self.pretrained_tokenizer(row['text'], padding='max_length', truncation=True, max_length=self.max_seq_len)['input_ids']
            label_id = self.label_map['label'].index(row['label'])

            X.append(ids)
            y.append(label_id)
        
        X = np.array(X)
        y = np.array(y)

        return X, {'label': y}


    def ner_preproc(self, input_data):
        intent_ids = []
        slot_ids = []
        X = []

        for _, row in input_data.iterrows():
            text_ids = []
            current_text_slot_ids = []
            text = row['text'].strip()
            tags = row['ner'].split(' ')
            try:
                intent_id = self.label_map['label'].index(row['label'])
            except:
                intent_id = 0

            for idx, word in enumerate(text.split(' ')):
                word_ids = self.pretrained_tokenizer.encode(word, add_special_tokens=False)
                text_ids.extend(word_ids)
                current_text_slot_ids.extend([self.label_map['ner'].index(tags[idx])] * len(word_ids))

            # Max sequence length clipping and adding special tokens
            text_ids = [self.special_tokens['bos_token']] + text_ids[:self.max_seq_len - 2] + [self.special_tokens['eos_token']]
            current_text_slot_ids = [self.label_map['ner'].index('<pad>')] + current_text_slot_ids[:self.max_seq_len - 2] + [self.label_map['ner'].index('<pad>')]

            # Padding
            padding_len = self.max_seq_len - len(text_ids)
            text_ids = text_ids + [self.special_tokens['pad_token']] * padding_len
            current_text_slot_ids = current_text_slot_ids + [self.label_map['ner'].index('<pad>')] * padding_len

            X.append(text_ids)
            intent_ids.append(intent_id)
            slot_ids.append(current_text_slot_ids)

        X = np.array(X)
        intent_ids = np.array(intent_ids)
        slot_ids = np.array(slot_ids)

        return X, {'label': intent_ids, 'ner': slot_ids}
    
    def run_transfer(self, input_file):
        X_transfer = []
        for idx, text in enumerate(input_file['text']):
            ids = self.pretrained_tokenizer(text, padding='max_length', truncation=True, max_length=self.max_seq_len)['input_ids']
            X_transfer.append(ids)
        # X_transfer = [self.pretrained_tokenizer(text, padding='max_length', truncation=True, max_length=self.max_seq_len)['input_ids'] for text in input_file['text']]
        X_transfer = np.array(X_transfer)

        return X_transfer


class DistilPreprocessingEngine(PreprocessingEngineBase):

    def __init__(self, max_seq_len, special_tokens, pretrained_tokenizer, label_map, output_path, logger_name, distil_tokenizer=None):
        super().__init__(max_seq_len, special_tokens, pretrained_tokenizer, label_map, logger_name)
        self.output_path = output_path
        self.set_tokenizer(distil_tokenizer)

    def run(self, input_data):
        if not self.distil_tokenizer:
            # TODO: Fix this output path hardcoding.
            self.fit_tokenizer(input_data['text'], self.output_path)
            self.special_tokens = {name: self.distil_tokenizer.word_index[token] for name, token in self.special_tokens.items()}

        intent_ids = []
        slot_ids = []
        X = []

        for _, row in input_data.iterrows():
            text_ids = []
            current_text_slot_ids = []
            text = row['text'].strip()
            tags = row['ner'].split(' ')
            try:
                intent_id = self.label_map['label'].index(row['label'])
            except:
                intent_id = 0
    
            for idx, word in enumerate(text.split(' ')):
                word_tokens = self.pretrained_tokenizer.tokenize(word)
                text_ids.extend([self.distil_tokenizer.word_index.get(token, 1) for token in word_tokens])
                current_text_slot_ids.extend([self.label_map['ner'].index(tags[idx])] * len(word_tokens))
            
            # Max sequence length clipping and adding special tokens
            text_ids = [self.special_tokens['bos_token']] + text_ids[:self.max_seq_len - 2] + [self.special_tokens['eos_token']]
            current_text_slot_ids = [self.label_map['ner'].index('<pad>')] + current_text_slot_ids[:self.max_seq_len - 2] + [self.label_map['ner'].index('<pad>')]

            # Padding
            padding_len = self.max_seq_len - len(text_ids)
            text_ids = text_ids + [self.special_tokens['pad_token']] * padding_len
            current_text_slot_ids = current_text_slot_ids + [self.label_map['ner'].index('<pad>')] * padding_len

            X.append(text_ids)
            intent_ids.append(intent_id)
            slot_ids.append(current_text_slot_ids)

        X = np.array(X)
        intent_ids = np.array(intent_ids)
        slot_ids = np.array(slot_ids)

        return X, {'label': intent_ids, 'ner': slot_ids}
    
    def run_transfer(self, input_file):
        tokenized_texts = []
        for text in input_file['text']:
            tokens = self.pretrained_tokenizer.tokenize(text)
            tokens = [self.special_tokens['bos_token']] + tokens[:self.max_seq_len - 2] + [self.special_tokens['eos_token']]
            pad_len = self.max_seq_len - len(tokens)
            tokens = tokens + [self.special_tokens['pad_token']] * pad_len
            tokenized_texts.append(tokens)
        
        X_transfer = self.distil_tokenizer.texts_to_sequences(tokenized_texts)
        X_transfer = np.array(X_transfer)
        
        return X_transfer

    def fit_tokenizer(self, texts, outpath):
        self.logger.info("************ Initializing Distil Tokenizer ************")

        distil_tokenizer = Tokenizer(filters="", lower=False, oov_token="[UNK]")
        tokenized_texts = [[self.special_tokens['bos_token']] + self.pretrained_tokenizer.tokenize(text) + [self.special_tokens['eos_token']] for text in texts]
        distil_tokenizer.fit_on_texts(tokenized_texts)
        distil_tokenizer.word_index[self.special_tokens["pad_token"]] = 0

        with open(os.path.join(outpath, "tokenizer.pickle"), "wb") as handle:
            pickle.dump(distil_tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

        self.logger.info("Size of tokenizer word index {}".format(len(distil_tokenizer.word_index)))

        self.set_tokenizer(distil_tokenizer)

    def set_tokenizer(self, distil_tokenizer):
        self.distil_tokenizer = distil_tokenizer

    def get_tokenizer(self):
        return self.distil_tokenizer
