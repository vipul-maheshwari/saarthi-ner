import os
import sys
import json
import logging
import numpy as np
import pandas as pd
import tensorflow as tf
from argparse import ArgumentParser
from tensorflow.keras.callbacks import Callback
from sklearn.model_selection import train_test_split

from model.teacher import Teacher
from utilities.math_funcs import gelu
from training.trainer import TeacherTrainer, Distiller
from utilities.general import get_labels, remove_special_characters_df

from azureml.core import Run
from azureml.core import Workspace, Dataset

run = Run.get_context()

def download_data(task,version=1):
	workspace = run.experiment.workspace
	dataset = Dataset.get_by_name(workspace, name=task, version=int(version))
	dataset.download(target_path=task, overwrite=False)


class LogRunMetrics(Callback):
    # callback at the end of every epoch
	def on_epoch_end(self, epoch, log):
		# log a value repeated which creates a list
		for k,v in log.items():
			run.log(k, v)

logger = logging.getLogger('ner')
logging.basicConfig(level = logging.INFO)

parser = ArgumentParser()

parser.add_argument('--task',required=True, help='Name of the dataset')
parser.add_argument('--version', required=True, help='Version of the dataset')


def main(argv):
    print(argv)
    args = vars(parser.parse_args(argv[1:]))
    logger.info(args)
    task_name = args['task']
    version = args['version']
    model_dir = './outputs'

    download_data(task_name, version)
    if os.path.exists(model_dir) and os.path.isdir(model_dir):
        pass
    else:
        os.mkdir(model_dir)
    
    if os.path.exists(os.path.join(model_dir, 'artifacts')) and os.path.isdir(os.path.join(model_dir, 'artifacts')):
        pass
    else:
        os.mkdir(os.path.join(model_dir, 'artifacts'))
    
    logger.info ("Directory of script ".format(os.path.dirname(os.path.abspath(__file__))))

    with open(f'{task_name}/ner_tagged_parsed.json', 'r') as f:
        data_json = json.load(f)
    label_map = get_labels(f'{task_name}/ner_labels.csv')

    text = []
    intent = []
    ner = []

    for sample in data_json:
        text.append(sample['text'])
        intent.append(sample['intent'])
        ner.append(sample['ner'])

    data = pd.DataFrame({'text': text, 'label': intent, 'ner': ner})
    # data = pd.DataFrame({'text': text, 'ner': ner})
    transfer = pd.read_csv(f'{task_name}/transfer.csv')
    data = remove_special_characters_df(data)
    train, dev = train_test_split(data, test_size=0.1)
    print(f'Train data: {len(train)}')
    print(f'Validation data: {len(dev)}')
    print(f'Transfer data: {len(transfer)}')

    strategy = tf.distribute.MirroredStrategy()
    teacher = Teacher('xlm-roberta', 24, strategy, 'teacher-factory')
    trainer = TeacherTrainer(train, label_map, teacher, strategy, 128, 80, 24, './outputs', 'trainer', dev_set=dev)
    trainer.add_callback(LogRunMetrics())
    trainer.run_training()
    finetuned_teacher = trainer.get_finetuned_model()

    student_config = {
        'word_emb_dim': 300,
        'lstm_hidden_size': 600,
        'dense_hidden_size': 768,
        'dense_act_func': gelu,
        'dropout': 0.2
    }
    distiller = Distiller(data, transfer, label_map, teacher, finetuned_teacher, strategy, 512, 200, 300000, 24, student_config, './outputs', 'distiller')
    distiller.add_metric_tracking_callback(LogRunMetrics())
    distiller.run_training()

    with open(os.path.join(model_dir, 'label_map.json'), 'w') as f:
        json.dump(label_map, f, indent=2)

if __name__=='__main__':
    main(sys.argv)