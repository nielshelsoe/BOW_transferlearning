import re
import string
def clean_text (df, row_name):
    #lower all text
    df[row_name] = df[row_name].str.lower()
    #remove all numbers
    df[row_name] = df[row_name].apply(lambda x: x.translate(str.maketrans('','','0123456789')))
    #remove all special chareters
    df[row_name] = df[row_name].apply(lambda x: re.sub('[\W]+', ' ', x))
    #make translation tabel where punctuation is removed and apply it to the text
    table = str.maketrans({key: None for key in string.punctuation})
    df[row_name] = df[row_name].apply(lambda x: x.translate(table))
    return df


