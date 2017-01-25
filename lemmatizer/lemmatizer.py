import os
import re
from collections import defaultdict
import simplejson as json
from PyTib.common import open_file, write_file, tib_sort


def gen_verb_families():
    raw = open_file('resources/monlam_verbs.json')
    monlam = json.loads(raw)
    # generate the structure for all
    all_families = defaultdict(list)
    for form, lemmas in monlam.items():
        for details in lemmas:
            if 'བྱ་ཚིག' in details.keys():
                lemma = details['བྱ་ཚིག']
                if lemma not in all_families[lemma]:
                    all_families[lemma].append(form)
    # discard all verbs that only have one form
    families = {}
    for lemma, members in all_families.items():
        if len(members) == 1:
            if lemma != members[0]:
                families[lemma] = members+[lemma]
        else:
            families[lemma] = list(set(members))  # remove duplicates
    return families


def gen_particle_families():
    particles = json.loads(open_file('resources/particles.json'))
    return particles


def format_families(families):
    lemmas_sorted = tib_sort(list(families.keys()))
    formatted = []
    for lemma in lemmas_sorted:
        members = families[lemma]
        formatted.append('{}:    {}'.format(lemma, '    '.join(members)))
    return '\n'.join(tib_sort(formatted))

verb_families = gen_verb_families()
verbs_formatted = format_families(verb_families)

particle_families = gen_particle_families()
particle_formatted = format_families(particle_families)
write_file('output/lemmas.txt', particle_formatted+'\n'+verbs_formatted)
print('ok')
