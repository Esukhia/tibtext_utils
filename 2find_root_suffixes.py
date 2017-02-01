import os
import re
from collections import defaultdict

from common import open_file, write_csv, tib_sort


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


def find_prefix_stems(prefixes, stems, token):
    for pre in prefixes:
        if len(token) > len(pre) and token.startswith(pre+'་'):
            # populating stems
            if pre not in stems:
                stems[pre] = {}
            if 'prefixes' not in stems[pre]:
                stems[pre]['prefixes'] = defaultdict(int)
            # increment the count
            stems[pre]['prefixes'][token] += 1


def find_postfix_stems(postfixes, stems, token):
    for post in postfixes:
        if len(token) > len(post) and token.endswith('་'+post):
            # populating stems
            if post not in stems:
                stems[post] = {}
            if 'postfixes' not in stems[post]:
                stems[post]['postfixes'] = defaultdict(int)
            # increment the count
            stems[post]['postfixes'][token] += 1


def find_infix_stems(infixes, stems, token):
    if token.count('་') >= 2:
        for inf in infixes:
            if len(token) > len(inf) and '་{}་'.format(inf) in token:
                # populating stems
                if inf not in stems:
                    stems[inf] = {}
                if 'infixes' not in stems[inf]:
                    stems[inf]['infixes'] = defaultdict(int)
                # increment the count
                stems[inf]['infixes'][token] += 1


def process_corpus(in_path, prefixes, infixes, postfixes):
    stems = {}
    for num, f in enumerate(os.listdir(in_path)):  # [:10] limiting to the first ten files
        tokens = pre_processing(open_file('{}/{}'.format(in_path, f)))
        tokens = [a for a in tokens if '་' in a]  # filters all the monosyllabled entries to speed up the execution
        for token in tokens:
            find_prefix_stems(prefixes, stems, token)
            find_infix_stems(infixes, stems, token)
            find_postfix_stems(postfixes, stems, token)
        print(num+1, f)
    return stems


def prepare_affixes(affix_path):
    raw_aff = open_file(affix_path).strip()
    return [line.split(',')[0] for line in raw_aff.split('\n') if line.split(',')[0] != '']


def rowify(stem_dict):
    rows = []
    sorted_stems = tib_sort(list(stem_dict.keys()))
    for stem in sorted_stems:
        for affix, msg in [('prefixes', 'as a prefix'), ('infixes', 'as an infix'), ('postfixes', 'as a postfix')]:
            if affix in stem_dict[stem]:
                tupled = [(token, freq) for token, freq in stem_dict[stem][affix].items()]
                tupled = sorted(tupled, key=lambda x: x[1], reverse=True)
                flattened = [a for tup in tupled for a in tup]
                rows.append([stem, msg] + flattened)
    return rows


def main():
    prefixes = prepare_affixes('1b_affixes_selection/potential_prefixes.csv')
    infixes = prepare_affixes('1b_affixes_selection//potential_infixes.csv')
    postfixes = prepare_affixes('1b_affixes_selection//potential_postfixes.csv')
    in_path = 'raw_corpus'
    stems = process_corpus(in_path, prefixes, infixes, postfixes)
    write_csv('2a_roots_suffixes/stems.csv', rowify(stems))


if __name__ == '__main__':
    main()
