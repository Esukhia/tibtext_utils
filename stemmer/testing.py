import os
import re
from collections import defaultdict
import simplejson as json
from PyTib.common import open_file


def gen_verb_families():
    monlam = json.loads(open_file('resources/monlam_verbs.json'))
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


verb_families = gen_verb_families()
print('ok')
