import os
import re
from collections import defaultdict
from common import open_file, write_csv


def generate_prefixes(syls):
    sequences = []
    for i in range(len(syls) - 1):  # -1 to not take the whole word
        sub_sequence = '་'.join(syls[0:i + 1])
        sequences.append(sub_sequence)
    return sequences


def generate_infixes(syls):
    sequences = []
    syls_stripped = syls[1:-1]
    for i in range(len(syls_stripped)):
        sub_sequence = '་'.join(syls_stripped[0:i + 1])
        sequences.append(sub_sequence)
    return sequences


def generate_postfixes(syls):
    sequences = []
    syls_inverted = list(reversed(syls))
    for i in range(len(syls_inverted)-1):  # -1 to not take the whole word
        sub_sequence = '་'.join(list(reversed(syls_inverted[0:i+1])))
        sequences.append(sub_sequence)
    return sequences


def generate_sub_sequences(syls):
    prefixes = generate_prefixes(syls)
    infixes = generate_infixes(syls)
    postfixes = generate_postfixes(syls)
    return {'prefixes': prefixes, 'infixes': infixes, 'postfixes': postfixes}


def find_affixes(word_list):
    potential_prefixes = defaultdict(int)
    potential_infixes = defaultdict(int)
    potential_postfixes = defaultdict(int)
    for word in word_list:
        syls = word.split('་')
        sub_sequences = generate_sub_sequences(syls)
        for kind, affixes in sub_sequences.items():
            if kind == 'prefixes':
                for a in affixes:
                    potential_prefixes[a] += 1
            if kind == 'infixes':
                for a in affixes:
                    potential_infixes[a] += 1
            if kind == 'postfixes':
                for a in affixes:
                    potential_postfixes[a] += 1
    return potential_prefixes, potential_infixes, potential_postfixes


def sort_potentials(prefixes, infixes, postfixes):
    prefixes_sorted = sorted([(postfix, freq) for postfix, freq in prefixes.items()],
                             key=lambda x: x[1], reverse=True)
    infixes_sorted = sorted([(postfix, freq) for postfix, freq in infixes.items()],
                            key=lambda x: x[1], reverse=True)
    postfixes_sorted = sorted([(postfix, freq) for postfix, freq in postfixes.items()],
                              key=lambda x: x[1], reverse=True)
    return prefixes_sorted, infixes_sorted, postfixes_sorted


def pre_processing(string):
    """
    do all the pre_processing here
    :param string:
    :return: a list of tokens
    """
    # separate the affixed particles into individual words
    string = string.replace('-', ' -')
    string = string.replace('།', '')
    string = string.replace('\u2005', ' -')
    string = string.replace('\n', '')
    string = re.sub(r'\s+', ' ', string)
    # delete tseks ending words
    string = string.replace('་ ', ' ')
    return string.split(' ')


def process(in_path):
    if in_path.endswith('.txt'):
        word_list = open_file('resources/uncompound_lexicon.txt').strip().split('\n')
        prefixes, infixes, postfixes = find_affixes(word_list)
        sorted_pre, sorted_in, sorted_post = sort_potentials(prefixes, infixes, postfixes)
    else:
        prefixes, infixes, postfixes = defaultdict(int), defaultdict(int), defaultdict(int)
        for f in os.listdir(in_path):
            word_list = pre_processing(open_file('{}/{}'.format(in_path, f)))
            new_prefixes, new_infixes, new_postfixes = find_affixes(word_list)
            # inject affixes in the defaultdicts
            for pre, freq in new_prefixes.items():
                prefixes[pre] += freq
            for inf, freq in new_infixes.items():
                infixes[inf] += freq
            for post, freq in new_postfixes.items():
                postfixes[post] += freq
        sorted_pre, sorted_in, sorted_post = sort_potentials(prefixes, infixes, postfixes)
    # write to csv files
    write_csv('1affixes/potential_prefixes.csv', sorted_pre)
    write_csv('1affixes/potential_infixes.csv', sorted_in)
    write_csv('1affixes/potential_postfixes.csv', sorted_post)


def main():
    in_path = 'raw_corpus'
    # in_path = 'resources/uncompound_lexicon.txt'
    process(in_path)


if __name__ == '__main__':
    main()
