import six
import pandas as pd


def convert_to_unicode(text):
    """Converts input text to unicode (if it's not already), assuming utf-8 input.

        Args:
            text (str/bytes): Input text

        Raises:
            ValueError: Unsupported string type error for Python 3.
            ValueError: Unsupported string type error for Python 2.
            ValueError: Unsupported Python version.

        Returns:
            str: Input text in unicode string format
        """
    if six.PY3:
        text = str(text)
        if isinstance(text, str):
            return text
        elif isinstance(text, bytes):
            return text.decode("utf-8", "ignore")
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    elif six.PY2:
        if isinstance(text, str):
            return text.decode("utf-8", "ignore")
        elif isinstance(text, unicode):
            return text
        else:
            raise ValueError("Unsupported string type: %s" % (type(text)))
    else:
        raise ValueError("Not running on Python2 or Python 3?")


def get_labels(label_file):
    """Returns a label map from a file containing all the labels.

    Args:
        label_file (str): Path to the file containing the labels
        special_tokens (dict, optional): Dictionary containing beginning of sequence, end of sequence and padding tokens. Defaults to None.

    Returns:
        dict: A python dictionary containing all the labels for all the columns
    """
    label_map = {}
    labels = pd.read_csv(label_file)
    
    for column in labels:
        series = labels[column]
        series = series.dropna()
        label_map[column] = list(series)

    return label_map


def remove_special_characters_df(df):
    """Removes special characters from the text column of the input dataframe.

    Args:
        df (pd.DataFrame): Input data.

    Returns:
        pd.DataFrame: DataFrame with text column cleaned.
    """    
    spec_chars = ["!",'"',"#","&","(",")",
              "*","+",",",";","<",
              "=",">","?","@","[","\\","]","^",
              "`","{","|","}","~","–"]
    for char in spec_chars:
        df['text'] = df['text'].str.replace(char, ' ')
    df['text'] = df['text'].str.split().str.join(" ")
    return df
