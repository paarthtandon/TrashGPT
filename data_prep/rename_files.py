import os

path = '../data/' # replace with the path to your directory

for filename in os.listdir(path):
    if " " in filename:
        new_filename = filename.replace(" ", "_")
        os.rename(os.path.join(path, filename), os.path.join(path, new_filename))
