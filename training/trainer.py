import os
import pickle
import logging
from abc import ABC, abstractmethod

import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split

from model.student import BiLSTMModel
from preprocessing.pipeline import AutoPreprocessor
from callbacks.getters import get_custom_lr_scheduler, get_early_stopping, get_cosine_scheduler, get_one_cycle_scheduler


class BaseTrainer(ABC):
    """Base trainer class"""

    def __init__(self, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        self.gpus = tf.config.list_physical_devices("GPU")

    def save(self, model, path, name):
        """Saves weights of given model to the provided output directory.

        Args:
            model (tf.keras.Model): Model to save.
            path (str): Path to save the model to.
            name (str): Name of the saved model.
        """
        model.save(os.path.join(path, name))

    @abstractmethod
    def run_training(self):
        """Runs training."""

    @abstractmethod
    def get_data(self):
        """Returns data for use by the model."""


class TeacherTrainer(BaseTrainer):
    def __init__(
        self,
        data,
        label_map,
        teacher,
        strategy,
        batch_size,
        epochs,
        max_seq_len,
        output_path,
        logger_name,
        dev_set=None,
    ):
        super().__init__(logger_name)

        self.teacher = teacher

        self.strategy = strategy
        self.epochs = epochs
        self.batch_size = batch_size
        self.output_path = output_path

        self.gpus = tf.config.list_physical_devices("GPU")

        self.logger.info("*******PREPROCESSING DATA*******")
        self.set_label_map(label_map)
        self.multi_columns = None
        self.callbacks = []
        self.preprocessor = self.get_preprocessor(max_seq_len)

        if dev_set is not None:
            self.set_data(data, mode='train')
            self.set_data(dev_set, mode='dev')
        else:
            train, dev = train_test_split(data, test_size=0.1, random_state=43)
            self.set_data(train, mode='train')
            self.set_data(dev, mode='dev')

        self.init_model()

    def run_training(self):
        """Fine tunes teacher model."""
        self.logger.info("*******FINETUNING TEACHER*******")
        self.fine_tune_teacher(epochs=self.epochs, batch_size=self.batch_size)
        self.logger.info('*******TEACHER FINETUNING FINISHED*******')

    def fine_tune_teacher(self, epochs, batch_size):
        """Fine tunes the teacher model on the given input data. Saves model in the output folder.

        Args:
            epochs (int): Number of epochs.
            batch_size (int): Batch size for training.
        """
        self.logger.info(self._model.summary())
        self.add_default_callbacks(epochs=epochs)

        self._model.fit(
            x=self.x_train_teacher,
            y=self.y_train_teacher,
            batch_size=batch_size * len(self.gpus),
            shuffle=True,
            epochs=epochs,
            callbacks=self.callbacks,
            validation_data=(self.x_dev_teacher, self.y_dev_teacher),
            verbose=1,
        )

        # self.save(self._model, self.output_path, "saved_model_teacher")

    def freeze_head(self, classname):
        self._model.get_layer(name=classname).trainable = False
    
    def unfreeze_head(self, classname):
        self._model.get_layer(name=classname).trainable = True

    def add_default_callbacks(self, epochs):
        self.add_callback(get_custom_lr_scheduler(epochs))
        self.add_callback(get_early_stopping(10))

    def add_callback(self, callback):
        self.callbacks.append(callback)

    def get_data(self, data):
        """Preprocesses and returns the teacher the student input data.

        Args:
            data (pd.DataFrame): A pandas dataframe containing the input data.
            max_seq_len (int): Maximum length of token sequence allowed.

        Returns:
            dict: Dictionary containing inputs, transfer text inputs, and labels for both teacher and student models.
        """
        x_teacher, y_teacher, _ = self.preprocessor.get_teacher_data(input_file=data)

        return {
            "train": x_teacher,
            "labels": y_teacher,
        }

    def set_data(self, data, mode='train'):
        self.logger.info(self.preprocessor.get_teacher_data(input_file=data))
        x_teacher, y_teacher, _ = self.preprocessor.get_teacher_data(input_file=data)

        if mode == 'train':
            self.x_train_teacher = x_teacher
            self.y_train_teacher = y_teacher
        elif mode == 'dev':
            self.x_dev_teacher = x_teacher
            self.y_dev_teacher = y_teacher

    def get_preprocessor(self, max_seq_len):
        special_tokens = self.teacher.get_special_tokens()
        pretrained_tokenizer = self.teacher.get_tokenizer()
        preprocessor = AutoPreprocessor(
            special_tokens=special_tokens,
            pretrained_tokenizer=pretrained_tokenizer,
            label_map=self.classes,
            output_path=self.output_path,
            max_seq_len=max_seq_len,
        )        

        return preprocessor

    def init_model(self):
        self._model = self.teacher.get_finetuning_compiled_model(self.classes)

    def set_model(self, teacher_finetuned):
        """Setter method for finetuned teacher model.

        Args:
            teacher_finetuned (tf.keras.Model): Finetuned teacher model
        """
        self._model = teacher_finetuned

    def get_finetuned_model(self):
        """Getter method for finetuned teacher model.

        Returns:
            tf.keras.Model: Finetuned teacher model
        """
        return self._model

    def set_label_map(self, label_map):
        self.classes = label_map


class Distiller(BaseTrainer):
    """Distils a given finetuned teacher model into a smaller student model.

        Args:
            data ([type]): [description]
            transfer_file_path ([type]): [description]
            label_path ([type]): [description]
            student ([type]): [description]
            finetuned_teacher ([type]): [description]
            intermediate_layer_teacher ([type]): [description]
            strategy ([type]): [description]
            distil_batch_size ([type]): [description]
            distil_epochs ([type]): [description]
            distil_chunk_size ([type]): [description]
            max_seq_len ([type]): [description]
            output_path ([type]): [description]
            logger_name ([type]): [description]
        
        Inherits from:
            BaseTrainer
        """
    def __init__(
        self,
        data,
        transfer_file,
        label_map,
        teacher,
        finetuned_teacher,
        strategy,
        distil_batch_size,
        distil_epochs,
        distil_chunk_size,
        max_seq_len,
        student_config,
        output_path,
        logger_name,
    ):
        super().__init__(logger_name)
        self.teacher = teacher
        self.finetuned_teacher = finetuned_teacher
        self.intermediate_layer_teacher = self.teacher.get_intermediate_layer_model(6)

        self.strategy = strategy
        self.distil_batch_size = distil_batch_size
        self.distil_epochs = distil_epochs
        self.distil_chunk_size = distil_chunk_size
        self.output_path = output_path

        self.phase1_callbacks = []
        self.phase2_callbacks = []
        self.phase3_callbacks = []
        self.phase4_callbacks = []
        self.phase5_callbacks = []

        self.logger.info("*******PREPROCESSING DATA*******")
        self.classes = label_map
        self.multi_columns = None
        self.preprocessor = self.get_preprocessor(max_seq_len)

        train, dev = train_test_split(data, test_size=0.2, random_state=43)
        train_data = self.get_data(train, transfer_file)
        dev_data = self.get_data(dev, None)

        self.x_transfer_teacher = train_data["teacher"]["transfer"]

        self.x_train_student = train_data['student']['train']
        self.y_train_student = train_data['student']['labels']
        self.x_transfer_student = train_data['student']['transfer']

        self.x_dev_student = dev_data['student']['train']
        self.y_dev_student = dev_data['student']['labels']

        for phase in range(1, 6):
            if phase < 6:
                self.add_default_early_callbacks(phase=phase)
            else:
                self.add_default_late_callbacks(phase=phase, epochs=self.distil_epochs, batch_size=self.distil_batch_size)
        
        with open(os.path.join(self.output_path, 'tokenizer.pickle'), 'rb') as f:
            distil_tokenizer = pickle.load(f)
        word_index = distil_tokenizer.word_index
        word_emb = self.teacher.get_word_embeddings(student_config['word_emb_dim'])

        self.student = BiLSTMModel(max_seq_len, word_index, word_emb, student_config['lstm_hidden_size'], student_config['dense_hidden_size'], student_config['dense_act_func'], student_config['dropout'], self.strategy, 'bilstm-student')

        self.shared_layers = self.student.get_shared_layers()
        self.logger.info(f"Shared layers: {self.shared_layers}")

    def run_training(self):
        """Distils the given student model."""
        self.logger.info("*******STARTING DISTILLATION*******")

        for stage in range(1, 2 * len(self.shared_layers) + 4):
            self.logger.info(f"*******STARTING STAGE {stage}*******")

            if stage == 1:
                # Student learns how to produce hidden representations like the lth layer of the teacher.
                s1model = self.train_stage_1(self.distil_epochs, self.distil_batch_size)
            elif stage == 2:
                # Student learns how to produce logits similar to those of the teacher (training the output heads only).
                s2model = self.train_stage_2(s1model, self.distil_epochs, self.distil_batch_size)
            elif stage > 2 and stage < 3 + len(self.shared_layers):
                # Student learns how to produce logits similar to those of the teacher with gradual unfreezing.
                arg_model = s2model if stage == 3 else prev_model
                prev_model = self.train_transfer_logits(arg_model, stage, self.distil_epochs, self.distil_batch_size)
            elif stage == 3 + len(self.shared_layers):
                # Student learns from the data while only training the output heads.
                prev_model = self.train_labelled_ce(prev_model, self.distil_epochs, self.distil_batch_size)
            elif stage > 3 + len(self.shared_layers):
                # Student learns from the data and is getting trained end to end.
                prev_model = self.train_labelled_e2e(prev_model, stage, self.distil_epochs, self.distil_batch_size)

        self.logger.info("*******DISTILLATION DONE*******")
        return prev_model

    def train_stage_1(self, epochs, batch_size):
        """Performs stage 1 of the student distillation.

        Args:
            batch_size (int): Batch size for training.
            epochs (int): Number of epochs to train on.

        Returns:
            tf.keras.Model: Model obtained after stage 1 distillation.
        """
        with self.strategy.scope():
            model = self.student.get_stage1_model()

        start_teacher = 0

        while start_teacher < len(self.x_transfer_teacher):
            end_teacher = min(
                start_teacher + self.distil_chunk_size, len(self.x_transfer_teacher)
            )
            y_teacher = self.intermediate_layer_teacher.predict(
                np.array(self.x_transfer_teacher[start_teacher:end_teacher]),
                batch_size=batch_size * len(self.gpus),
            )

            model_file = f"model-stage-1-indx-{start_teacher}.h5"
            if os.path.exists(os.path.join(self.output_path, model_file)):
                self.logger.info(f"Loadings weights for stage 1 from {model_file}")
                model.load_weights(os.path.join(self.output_path, model_file))
            else:
                self.logger.info(model.summary())
                model.fit(
                    self.x_transfer_student[start_teacher:end_teacher],
                    y_teacher,
                    shuffle=True,
                    batch_size=batch_size * len(self.gpus),
                    verbose=2,
                    epochs=epochs,
                    callbacks=self.phase1_callbacks,
                    validation_split=0.1,
                )
                # model.save_weights(os.path.join(self.output_path, model_file))

            start_teacher = end_teacher

        return model

    def train_stage_2(self, s1model, epochs, batch_size):
        """Performs stage 2 distillation on student from stage 1.

        Args:
            s1model (tf.keras.Model): Model from stage 1.
            epochs (int): Number of epochs to train on.
            batch_size (int): Batch size for training.

        Returns:
            tf.keras.Model: Model obtained after stage 2 distillation.
        """
        with self.strategy.scope():
            model = self.student.get_stage2_model(
                s1model, self.shared_layers, self.classes, self.multi_columns
            )

        start_teacher = 0

        while start_teacher < len(self.x_transfer_teacher):
            end_teacher = min(
                start_teacher + self.distil_chunk_size, len(self.x_transfer_teacher)
            )
            y_teacher = self.finetuned_teacher.predict(
                np.array(self.x_transfer_teacher[start_teacher:end_teacher]),
                batch_size=batch_size * len(self.gpus),
            )

            model_file = f"model-stage-2-indx-{start_teacher}.h5"
            if os.path.exists(os.path.join(self.output_path, model_file)):
                self.logger.info(f"Loading weights for stage 2 from {model_file}")
                model.load_weights(os.path.join(self.output_path, model_file))
            else:
                self.logger.info(model.summary())
                model.fit(
                    self.x_transfer_student[start_teacher:end_teacher],
                    y_teacher,
                    shuffle=True,
                    batch_size=batch_size * len(self.gpus),
                    verbose=2,
                    epochs=epochs,
                    callbacks=self.phase2_callbacks,
                    validation_split=0.1,
                )
                # self.save(model, self.output_path, model_file)

            start_teacher = end_teacher

        return model

    def train_transfer_logits(self, s2model, stage, epochs, batch_size):
        """Optimizes model on the logits of teacher on the transfer texts.

        Args:
            s2model (tf.keras.Model): Model obtained after stage 2 distillation.
            stage (int): Current distillation stage.
            epochs (int): Number of epochs to train on.
            batch_size (int): Batch size for training.
        """
        with self.strategy.scope():
            model = self.student.compile_transfer_logits_model(
                s2model, self.shared_layers, stage, self.classes
            )

        start_teacher = 0
        while start_teacher < len(self.x_transfer_teacher):
            end_teacher = min(
                start_teacher + self.distil_chunk_size, len(self.x_transfer_teacher)
            )
            y_teacher = self.finetuned_teacher.predict(
                np.array(self.x_transfer_teacher[start_teacher:end_teacher]),
                batch_size=batch_size * len(self.gpus),
            )

            model_file = f"model-stage-{stage}-indx-{start_teacher}.h5"
            if os.path.exists(os.path.join(self.output_path, model_file)):
                self.logger.info(f"Loading weights for stage 2 from {model_file}")
                model.load_weights(os.path.join(self.output_path, model_file))
            else:
                self.logger.info(model.summary())
                model.fit(
                    self.x_transfer_student[start_teacher:end_teacher],
                    y_teacher,
                    shuffle=True,
                    batch_size=batch_size * len(self.gpus),
                    verbose=2,
                    epochs=epochs,
                    callbacks=self.phase3_callbacks,
                    validation_split=0.1,
                )
                # self.save(model, self.output_path, model_file)

            start_teacher = end_teacher

        return model

    def train_labelled_ce(self, prev_model, epochs, batch_size):
        """Optimizes model's all but last layer on the labelled data using crossentropy loss.

        Args:
            prev_model (tf.keras.Model): Model obtained from previous distillation stage.
            epochs (int): Number of epochs to train on.
            batch_size (int): Batch size for training.
        """
        with self.strategy.scope():
            model = self.student.compile_labelled_ce_model(
                prev_model, self.shared_layers, self.classes, self.multi_columns
            )

        # TODO: Fix the index in this f-string
        model_file = f"model-stage-{3 + len(self.shared_layers)}.h5"

        if os.path.exists(os.path.join(self.output_path, model_file)):
            self.logger.info("Loadings weights for stage 3 from {}".format(model_file))
            model.load_weights(model_file)
        else:
            self.logger.info(model.summary())
            model.fit(
                self.x_train_student,
                self.y_train_student,
                batch_size=batch_size * len(self.gpus),
                verbose=2,
                shuffle=True,
                epochs=epochs,
                callbacks=self.phase4_callbacks,
                validation_data=(self.x_dev_student, self.y_dev_student),
            )
            # model.save(os.path.join(self.output_path, "saved_model_distil"))

        return model

    def train_labelled_e2e(self, prev_model, stage, epochs, batch_size):
        """Trains student model end to end on the labelled data.

        Args:
            prev_model (tf.keras.Model): Model obtained from previous distillation stage.
            stage (int): Current stage of distillation.
            epochs (int): Number of epochs to train on.
            batch_size (int): Batch size for training.
        """
        with self.strategy.scope():
            model = self.student.compile_labelled_e2e_ce_model(
                prev_model, self.shared_layers, self.classes, self.multi_columns, stage
            )

        model_file = f"model-stage-{stage}.h5"
        if os.path.exists(model_file):
            self.logger.info("Loadings weights for stage 3 from {}".format(model_file))
            model.load_weights(os.path.join(self.output_path, model_file))
        else:
            self.logger.info(model.summary())
            model.fit(
                self.x_train_student,
                self.y_train_student,
                batch_size=batch_size * len(self.gpus),
                verbose=2,
                shuffle=True,
                epochs=epochs,
                callbacks=self.phase5_callbacks,
                validation_data=(self.x_dev_student, self.y_dev_student),
            )
            if stage == 2 * len(self.shared_layers) + 3:
                model.save(os.path.join(self.output_path, "saved_model_distil"))

        return model
    
    def add_default_early_callbacks(self, phase):
        """Method that adds callbacks for phases 1-3

        Args:
            phase (int): Phase number.
        """        
        self.add_callback(get_cosine_scheduler(lr_high=0.001, lr_low=1e-8), phase)
        self.add_callback(get_early_stopping(10), phase)
    
    def add_default_late_callbacks(self, phase, epochs, batch_size):
        """Methods that adds callbacks for phases 4 and 5

        Args:
            phase (int): Phase number.
            epochs (int): Number of training epochs.
            batch_size (int): Batch size during training.
        """        
        self.add_callback(get_one_cycle_scheduler(lr=5e-5,epochs=epochs,batch_size=batch_size,train_size=len(self.x_transfer_teacher)), phase)
        self.add_callback(get_early_stopping(10), phase)
    
    def add_metric_tracking_callback(self, callback):
        self.add_callback(callback, 4)
        self.add_callback(callback, 5)

    def clear_callbacks(self, phase):
        eval(f'self.phase{phase}_callbacks.clear()')

    def add_callback(self, callback, phase):
        eval(f'self.phase{phase}_callbacks.append(callback)')


    def get_data(self, data, transfer_file):
        """Preprocesses and returns the teacher the student input data.

        Args:
            data (pd.DataFrame): A pandas dataframe containing the input data.
            transfer_file (pd.DataFrame): Pandas dataframe containing the transfer texts.

        Returns:
            dict: Dictionary containing inputs, transfer text inputs, and labels for teacher and student models.
        """
        self.multi_columns = []

        _, _, x_transfer_teacher = self.preprocessor.get_teacher_data(transfer_file=transfer_file)
        x_student, y_student, x_transfer_student = self.preprocessor.get_student_data(input_file=data, transfer_file=transfer_file)

        return {
            "teacher": {
                "transfer": x_transfer_teacher,
            },
            "student": {
                "train": x_student,
                "transfer": x_transfer_student,
                "labels": y_student,
            },
        }

    def get_preprocessor(self, max_seq_len):
        special_tokens = self.teacher.get_special_tokens()
        pretrained_tokenizer = self.teacher.get_tokenizer()

        preprocessor = AutoPreprocessor(
            max_seq_len=max_seq_len,
            special_tokens=special_tokens,
            label_map=self.classes,
            pretrained_tokenizer=pretrained_tokenizer,
            output_path=self.output_path
        )

        return preprocessor
