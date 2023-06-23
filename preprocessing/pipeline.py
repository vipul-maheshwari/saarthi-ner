import logging
from .engine import TeacherPreprocessingEngine, DistilPreprocessingEngine

class AutoPreprocessor:
    """Zero effort pipeline that takes care of all the preprocessing.

    Args:
        special_tokens (dict): Dictionary containing beginning of sequence, end of sequence, and padding tokens.
        pretrained_tokenizer (HuggingFace tokenizer): Pretrained tokenizer of the teacher model.
        label_map (dict): Dictionary mapping all targets to a list of all their possible values.
        max_seq_len (int): Maximum permissible length of the input text (counted in terms of the number of tokens the text gets tokenized into). Defaults to 16.
    """
    def __init__(self, special_tokens, pretrained_tokenizer, label_map, output_path, max_seq_len=16):
        self.teacher_engine = TeacherPreprocessingEngine(max_seq_len, special_tokens, pretrained_tokenizer, label_map, 'teacher_engine')
        self.distil_engine = DistilPreprocessingEngine(max_seq_len, special_tokens, pretrained_tokenizer, label_map, output_path, 'distil_engine')
        self.preprocessor = Preprocessor(self.teacher_engine, 'auto_preprocessor')

    def get_teacher_data(self, input_file=None, transfer_file=None):
        """Returns data required for teacher model.

        Args:
            input_file (pandas.DataFrame): DataFrame containing input data.
            transfer_file (pandas.DataFrame): DataFrame containing transfer texts.

        Returns:
            List[List[int]], List[List[int]], Dict[str, List[int]]: Training data, Transfer data, Labels
        """
        self.preprocessor.set_preprocessing_engine(self.teacher_engine)
        return self.preprocessor.get_data(input_file=input_file, transfer_file=transfer_file)

    def get_student_data(self, input_file=None, transfer_file=None):
        self.preprocessor.set_preprocessing_engine(self.distil_engine)
        return self.preprocessor.get_data(input_file=input_file, transfer_file=transfer_file)


class Preprocessor:

    def __init__(self, preprocessing_engine, logger_name):
        self.logger = logging.getLogger(logger_name)
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False

        self.preprocessing_engine = preprocessing_engine

    def process_file(self, file, transfer=False):
        X = None
        y = {}
        if self.file_exists(file):
            if transfer:
                X = self.preprocessing_engine.run_transfer(file)
            else:
                X, y = self.preprocessing_engine.run(file)

        return X, y

    def get_data(self, input_file=None, transfer_file=None):
        X, y = self.process_file(input_file)
        X_transfer, _ = self.process_file(transfer_file, transfer=True)

        if self.file_exists(X):
            self.logger.info(f"X shape: {X.shape}")
            self.logger.info(f"y: {y.keys()}")
        if self.file_exists(X_transfer):
            self.logger.info(f"X_transfer shape: {X_transfer.shape}")

        return X, y, X_transfer

    def get_data_ner(self, input_file=None, transfer_file=None):
        X, y = self.process_file_ner(input_file)
        X_transfer, _ = self.process_file_ner(transfer_file, transfer=True)

        if self.file_exists(X):
            self.logger.info(f"X shape: {X.shape}")
            self.logger.info(f"y: {y.keys()}")
        if self.file_exists(X_transfer):
            self.logger.info(f"X_transfer shape: {X_transfer.shape}")

        return X, y, X_transfer

    def process_file_ner(self, file, transfer=False):
        X = None
        y = {}
        if self.file_exists(file):
            if transfer:
                X = self.preprocessing_engine.run_transfer(file)
            else:
                X, y = self.preprocessing_engine.run(file)

        return X, y

    def get_data_intent(self, input_file=None, transfer_file=None):
        X, y = self.process_file_intent(input_file)
        X_transfer, _ = self.process_file_intent(transfer_file, transfer=True)

        if self.file_exists(X):
            self.logger.info(f"X shape: {X.shape}")
            self.logger.info(f"y: {y.keys()}")
        if self.file_exists(X_transfer):
            self.logger.info(f"X_transfer shape: {X_transfer.shape}")

        return X, y, X_transfer

    def process_file_intent(self, file, transfer=False):
        X = None
        y = {}
        if self.file_exists(file):
            if transfer:
                X = self.preprocessing_engine.run_transfer(file)
            else:
                X, y = self.preprocessing_engine.run(file)

        return X, y

    def file_exists(self, input_file):
        return input_file is not None

    def set_preprocessing_engine(self, engine):
        """Setter method for preprocessing engine.

        Args:
            engine (PreprocessingEngineBase): Preprocessing engine object.
        """        
        self.preprocessing_engine = engine
