from collections import defaultdict
from PyTib.common import open_file, write_csv, tib_sort


def format_families(families):
    lemmas_sorted = tib_sort(list(families.keys()))
    formatted = []
    for lemma in lemmas_sorted:
        members = families[lemma]
        formatted.append('{}:    {}'.format(lemma, '    '.join(members)))
    return '\n'.join(tib_sort(formatted))


def find_potentials(shorter_words, longer_words):
    prefix_family = defaultdict(list)
    infix_family = defaultdict(list)
    postfix_family = defaultdict(list)
    for short in shorter_words:
        for long in longer_words:
            if long.startswith(short+'་'):
                prefix_family[short].append(long)
            if '་{}་'.format(short) in long:
                infix_family[short].append(long)
            if long.endswith('་'+short):
                postfix_family[short].append(long)
    return {'prefixes': prefix_family, 'infixes': infix_family, 'postfixes': postfix_family}


def count_syl_amount(string):
    return string.count('་')+1


def find_all_potentials(words):
    total_potentials = {}
    # generate lists of different sizes and process them
    maximum_word_length = sorted(list(set([count_syl_amount(a) for a in words])), reverse=True)[0]
    for i in range(maximum_word_length-1):  # -1 because we want to ensure there are always longer words
        current_size = i+1
        shorter_list = [word for word in words if count_syl_amount(word) == current_size]
        longer_list = [word for word in words if count_syl_amount(word) > current_size]
        potentials = find_potentials(shorter_list, longer_list)
        for kind, groups in potentials.items():
            for stem, members in groups.items():
                # initialize structure
                if stem not in total_potentials.keys():
                    total_potentials[stem] = {}
                if kind not in total_potentials[stem].keys():
                    total_potentials[stem][kind] = []

                total_potentials[stem][kind].append(members)
    return total_potentials


def format_potentials(potentials):
    rows = []
    lemmas_sorted = tib_sort(list(potentials.keys()))
    for lemma in lemmas_sorted:
        lemma_field = lemma
        family = potentials[lemma]
        comments = {'prefixes': 'as a prefix', 'infixes': 'as an infix', 'postfixes': 'as a postfix'}
        for kind in ['prefixes', 'infixes', 'postfixes']:
            if kind in family.keys():
                current_row = [lemma_field, comments[kind]]
                for members in family[kind]:
                    current_row.extend(members)
                rows.append(current_row)
        rows.append([])
    return rows


def main():
    word_list = open_file('resources/uncompound_lexicon.txt').strip().split('\n')
    all_potentials = find_all_potentials(word_list)
    formatted = format_potentials(all_potentials)
    write_csv('output/affixes.csv', formatted)


if __name__ == '__main__':
    main()
