import os
import re


read_dir = 'annotated_w_names/'
diar_dir = 'speech_diarization/'
out_file_n = '_test_dataset.txt'
out_file = open(out_file_n, 'w', encoding='utf-8')

diar_file_ns = os.listdir(diar_dir)
ep_names = [fn.split('.')[0] for fn in diar_file_ns]

trans_file_ns = os.listdir(read_dir)
ep_to_trans = {}
for ep_name in ep_names:
    ep_to_trans[ep_name] = ''
    for t in trans_file_ns:
        if ep_name in t and len(t) > len(ep_to_trans[ep_name]):
            ep_to_trans[ep_name] = t

for title, file_n in ep_to_trans.items():
    if file_n == '':
        continue
    file = open(read_dir + file_n, 'r', encoding='utf-8')
    text = file.read()
    file.close()

    if '<SPEAKER_' in text:
        continue

    out_file.write('\n--------------------\n')
    # print(title)
    title = title.lower()
    title = re.split(r"trash_taste_\d+", title)[0]
    title = re.sub(r'[^a-zA-Z]+', ' ', title)
    # print(title)
    out_file.write(f'<title>{title}</title>\n')
    out_file.write(text)

out_file.close()
