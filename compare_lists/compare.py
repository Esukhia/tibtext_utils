from PyTib.common import open_file, write_file
import os

monlam = open_file('input/monlam1_total_corrected.txt').split('\n')
monlam_entries = [a.split(' | ')[0] for a in monlam]
monlam_entries = [a.rstrip('་') for a in monlam_entries]
monlam_dict = {a: True for a in monlam_entries}

non_monlam = {}
in_path = 'input/user_vocabs'
for f in os.listdir(in_path):
    content = open_file('{}/{}'.format(in_path, f)).replace('\n', ' ').split(' ')
    words = [a.rstrip('་') for a in content]
    for word in words:
        if word not in monlam_dict:
            non_monlam[word] = True
non_words = '\n'.join(list(non_monlam.keys()))
write_file('output/non_monlam.txt', non_words)
