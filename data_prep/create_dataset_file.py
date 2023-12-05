import os

read_dir = '../data/constructed/'
out_file_n = '_dataset.txt'
out_file = open(out_file_n, 'w', encoding='utf-8')

ep_names = {}
sub_file_ns = os.listdir(read_dir)
for fn in sub_file_ns:
    name = fn.split('#')[0]
    name = name.replace('_', ' ').strip()
    name = ' '.join(name.split())[:-12]
    ep_names[fn] = name

for fn, name in ep_names.items():
    out_file.write(f'-----\n\n')

    with open(read_dir + fn, 'r') as ep_txt:
        out_file.write(f'{ep_txt.read()}\n\n')

out_file.close()
