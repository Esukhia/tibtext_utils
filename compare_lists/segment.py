import PyTib
from PyTib.common import open_file, write_file


seg = PyTib.Segment()

content = open_file('output/non_monlam.txt').strip().split('\n')
segmented = [seg.segment(a) for a in content]
segmented = '\n'.join([a for a in segmented if '#' in a])
write_file('output/misplelt_non_monlam.txt',segmented)

print('ok')