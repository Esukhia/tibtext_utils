import os
import re
from collections import defaultdict
import simplejson as json
from PyTib.common import open_file, write_file, tib_sort


def format_families(families):
    lemmas_sorted = tib_sort(list(families.keys()))
    formatted = []
    for lemma in lemmas_sorted:
        members = families[lemma]
        formatted.append('{}:    {}'.format(lemma, '    '.join(members)))
    return '\n'.join(tib_sort(formatted))


def find_potential_suffixes():
    raw = open_file('resources/uncompound_lexicon.txt')
    words = raw.split('\n')
    single_syllabled = [word for word in words if '་' not in word]
    multi_syllabled = [word for word in words if '་' in word]

    # searching prefixes
    prefix_family = defaultdict(list)
    # searching infixes
    infix_family = defaultdict(list)
    # searching post-fixes
    postfix_family = defaultdict(list)
    for s_w in single_syllabled:
        for m_w in multi_syllabled:
            if m_w.startswith(s_w+'་'):
                prefix_family[s_w].append(m_w)
            if '་{}་'.format(s_w) in m_w:
                infix_family[s_w].append(m_w)
            if m_w.endswith(s_w):
                postfix_family[s_w].append(m_w)
    return prefix_family, infix_family, postfix_family

def format_potential(potentials):
    rows = []

    for p in potentials:
        rows.append()


prefixes, infixes, postfixes = find_potential_suffixes()
