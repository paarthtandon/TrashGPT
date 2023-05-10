import os
import string

path = '../data/' # replace with the path to your directory
valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

for filename in os.listdir(path):
    if any((c not in valid_chars) for c in filename):
        new_filename = ''.join(c for c in filename if c in valid_chars)
        new_filename = new_filename.replace(" ", "_")
        os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
