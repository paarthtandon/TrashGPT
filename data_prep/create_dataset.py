import os


read_dir = '../annotated_w_names/'
out_file_n = '../annotated_w_names/dataset.txt'
out_file = open(out_file_n, 'w', encoding='utf-8')

files = os.listdir(read_dir)
for file_n in files:
    file = open(read_dir + file_n, 'r', encoding='utf-8')
    text = file.read()
    file.close()

    if '<SPEAKER_' in text:
        continue

    out_file.write('\n--------------------\n')
    out_file.write(text)

out_file.close()
