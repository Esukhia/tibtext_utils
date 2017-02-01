from common import open_file, write_file, tib_sort


families_selection = open_file('2b_roots_suffixes_selection/stems.csv').strip().split('\n')

new_families = []
line_fields = [a.split(',') for a in families_selection]
for line in line_fields:
    entry = line[3]
    fields = [a for a in line[5:] if a != '']
    members = [fields[a] for a in range(1, len(fields), 2)]
    new_families.append('{}:    {}'.format(entry, '    '.join(members)))
new_families = '\n'.join(new_families)

# read additions to add at the end of families.txt
additions = open_file('3additions/lemmas.txt')

complete = '{}\n{}'.format(new_families, additions)

write_file('families.txt', complete)