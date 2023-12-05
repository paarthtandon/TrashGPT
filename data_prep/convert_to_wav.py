import subprocess
import os
from concurrent.futures import ProcessPoolExecutor

def convert_file(file_name, dir_path, out_path):
    if file_name.endswith('.m4a'):
        file_path = os.path.join(dir_path, file_name)
        
        # Set output file path and name
        output_file_name = file_name[:-4] + '.wav'
        output_file_path = os.path.join(out_path, output_file_name)
        
        # Run FFmpeg command to convert file
        subprocess.run(['../ffmpeg-6/bin/ffmpeg.exe', '-i', file_path, '-acodec', 'pcm_s16le', '-ar', '44100', output_file_path])

def main():
    dir_path = '../data/raw/'
    out_path = '../data/wav/'

    # List of file names in the directory
    files = os.listdir(dir_path)

    # Use ProcessPoolExecutor to parallelize the conversion
    with ProcessPoolExecutor() as executor:
        # Map the convert_file function to all files
        executor.map(convert_file, files, [dir_path]*len(files), [out_path]*len(files))

    print('Conversion complete.')

if __name__ == "__main__":
    main()
