import random

test_f = './annotated_w_names/_dataset.txt'
with open(test_f, 'r') as t:
    lines = t.readlines()

r = random.randint(0, len(lines) - 11)
out = lines[r: r + 10]
for o in out:
    print(o[:-1])
