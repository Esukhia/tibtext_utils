import os
import re
from collections import defaultdict
from common import open_file, write_csv


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

    families = defaultdict(dict)
    for word, freq in raw_freqs.items():
        has_a_family = False
        for lemma, members in groups.items():
            if word in members:
                families[lemma][word] = freq
                has_a_family = True

        # if the headword is a loner
        if not has_a_family:
            families[word][word] = freq
    return families


def group_families(word_list):
    raw_frequencies = find_raw_freqs(word_list)
    regrouped_frequencies = find_families(raw_frequencies)
    return regrouped_frequencies


def gen_total_types(input):
    def update_total(lemma, family):
        for member, freq in family.items():
            total_grouped_families[lemma][member] += freq
    total_grouped_families = {}
    for f in os.listdir(input):
        content = open_file('{}/{}'.format(input, f))
        segmented = pre_processing(content)
        current_families = group_families(segmented)
        for lemma, family in current_families.items():
            if lemma not in total_grouped_families:
                total_grouped_families[lemma] = defaultdict(int)
                update_total(lemma, family)
            else:
                update_total(lemma, family)
    return total_grouped_families


def gen_grouped_freq(member_freq):
    grouped_stems = []
    for lemma, family in member_freq.items():
        if len(family.keys()) == 1:
            grouped_stems.append([(lemma, family[lemma])])
        else:
            freq = sum(list(family.values()))
            pair = (lemma, freq)
            sorted_family = sorted([(member, m_freq) for member, m_freq in family.items()],
                                   key=lambda x: x[1], reverse=True)
            grouped_stems.append([pair]+sorted_family)
    freq_sorted = sorted(grouped_stems, key=lambda x: x[0][1], reverse=True)
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
    grouped_freqs = gen_grouped_freq(members_freq)
    flattened = flatten_freq_struct(grouped_freqs)
    header = generate_header(grouped_freqs)
    write_csv('output/total_freqs.csv', flattened, header=header)


if __name__ == '__main__':
    main()
