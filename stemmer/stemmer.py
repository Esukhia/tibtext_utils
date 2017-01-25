import os
import re
from collections import defaultdict
from PyTib.common import open_file, write_csv


def pre_processing(string):
    """
    do all the pre_processing here
    :param string:
    :return: a list of tokens
    """
    # Todo: make all the input files homogeneous through operations in this function
    # separate the affixed particles into individual words
    string = string.replace('-', ' -')
    string = string.replace('།', '')
    string = string.replace('\u2005', ' -')
    string = string.replace('\n', '')
    string = re.sub(r'\s+', ' ', string)
    return string.split(' ')


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
    # Todo: change the input format and adapt this function
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

    headwords = defaultdict(dict)
    for word, freq in raw_freqs.items():
        has_a_family = False
        for lemma, members in groups.items():
            if word in members:
                headwords[lemma][word] = freq
                has_a_family = True

        # if the headword is a loner
        if not has_a_family:
            headwords[word][word] = freq
    return headwords


def create_headwords(word_list):
    raw_frequencies = find_raw_freqs(word_list)
    regrouped_frequencies = find_families(raw_frequencies)
    return regrouped_frequencies


def gen_total_types(input):
    def update_total(lemma, family):
        for member, freq in family.items():
            total_headwords[lemma][member] += freq
    total_headwords = {}
    for f in os.listdir(input):
        content = open_file('{}/{}'.format(input, f))
        segmented = pre_processing(content)
        current_headwords = create_headwords(segmented)
        for lemma, family in current_headwords.items():
            if lemma not in total_headwords:
                total_headwords[lemma] = defaultdict(int)
                update_total(lemma, family)
            else:
                update_total(lemma, family)
    return total_headwords


def gen_headwords_freq(member_freq):
    headwords = []
    for lemma, family in member_freq.items():
        if len(family.keys()) == 1:
            headwords.append([(lemma, family[lemma])])
        else:
            freq = sum(list(family.values()))
            headword = (lemma, freq)
            sorted_family = sorted([(member, m_freq) for member, m_freq in family.items()], key=lambda x: x[1], reverse=True)
            headwords.append([headword]+sorted_family)
    freq_sorted = sorted(headwords, key=lambda x: x[0][1], reverse=True)
    return freq_sorted


def generate_header(freqs):
    longest = 0
    for el in freqs:
        if len(el) > longest:
            longest = len(el)
    lemma_header = ['stem', 'freq']
    members_header = []
    for a in range(longest):
        members_header.append('word' + str(a))
        members_header.append('freq')
    return lemma_header+members_header


def flatten_freq_struct(freqs):
    flattened = []
    for row in freqs:
        flattened.append([b for a in row for b in a])
    return flattened


def main():
    members_freq = gen_total_types('input')
    headwords_freqs = gen_headwords_freq(members_freq)
    flattened = flatten_freq_struct(headwords_freqs)
    header = generate_header(headwords_freqs)
    write_csv('output/total_freqs.csv', flattened, header=header)

main()
