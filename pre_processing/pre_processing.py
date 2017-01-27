import re

def clean_string(string,
                 tabs2spaces=False, under2spaces=False, spaces2same=False,
                 single_spaces=False, single_returns=False, single_unders=False,
                 del_spaces=False, del_returns=False, del_dashes=False,
                 l_strip=False, r_strip=False, strip=False, ):


    # Replacements
    if tabs2spaces: string = string.replace('\t', ' ')
    if under2spaces: string = string.replace('_', ' ')
    if spaces2same: string = re.sub(r'\s', ' ', string)

    # Reducing to one element
    if single_spaces: string = re.sub(r' +', r' ', string)
    if single_returns: string = re.sub(r'\n+', r'\n', string)
    if single_unders: string = re.sub(r'_+', r'_', string)

    # Delete the given elements
    if del_spaces: string = string.replace(' ', '')
    if del_returns: string = string.replace('\n', '')
    if del_dashes: string = string.replace('-', '')

    # strips
    if l_strip: string = string.lstrip()
    if r_strip: string = string.rstrip()
    if strip: string = string.strip()

    return string


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
