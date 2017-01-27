import re


def pre_processing(string):
    """
    do all the pre_processing here
    :param string:
    :return: a list of tokens
    """
    # Todo: make all the input files homogeneous through operations in this function
    # separate the affixed particles into individual words
    string = string.strip()
    string = string.replace('-', ' -')
    string = string.replace('།', '')
    string = string.replace('\u2005', ' -')
    string = string.replace('\n', '')
    string = re.sub(r'\s+', ' ', string)
    return string.split(' ')
