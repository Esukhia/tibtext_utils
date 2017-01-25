import os
import re
from collections import defaultdict
from PyTib.common import open_file, write_csv


def pre_processing(string):
    """
    do all the pre_processing here
    :param string:
    :return:
    """
    # separate the affixed particles into individual words
    string = string.replace('-', ' -')
    string = string.replace('\u2005', ' -')
    string = string.replace('\n', '')
    return string


def find_raw_freqs(word_list):
    freqs = defaultdict(int)
    for word in word_list:
        freqs[word] += 1
    return freqs


def parse_families():
    """
    parses families.txt into a dict with lists in the value slot
    :return:
    """
    content = open_file('families.txt')
    groups = {}
    for line in content.strip().split('\n'):
        lemma, group = line.split(':')
        group = re.sub(r' +', ' ', group).strip()
        members = group.split(' ')
        groups[lemma] = members
    return groups


def find_families(raw_freqs):
    groups = parse_families()

    inversed_groups = {}
    for lemma, members in groups.items():
        inversed_groups[tuple(members)] = lemma

    headwords = defaultdict(dict)
    for word in raw_freqs:
        for members, lemma in inversed_groups.items():
            if word in members:
                pass
                #headwords[lemma][word]


def create_headwords(word_list):
    raw_frequencies = find_raw_freqs(word_list)
    regrouped_frequencies = find_families(raw_frequencies)


def stem(input):
    for f in os.listdir(input):
        content = open_file('{}/{}'.format(input, f))
        content = pre_processing(content)
        segmented = content.split(' ')
        # apply regexes
        headwords = create_headwords(segmented)

        pass

def main():
    in_path = 'input'
    stemmed = stem(in_path)

main()