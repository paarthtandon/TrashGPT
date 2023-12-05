import os
import shutil

def copy_json_files(source_directory, destination_directory):
    # Ensure the destination directory exists, create if not
    if not os.path.exists(destination_directory):
        os.makedirs(destination_directory)

    # Search for .json files with ".en." in their names
    for file in os.listdir(source_directory):
        if file.endswith('.json3') and ".en." in file:
            source_file = os.path.join(source_directory, file)
            destination_file = os.path.join(destination_directory, file)
            shutil.copy2(source_file, destination_file)
            print(f"Copied: {file}")

source_directory = '../data/raw/'
destination_directory = '../data/json/'

copy_json_files(source_directory, destination_directory)
