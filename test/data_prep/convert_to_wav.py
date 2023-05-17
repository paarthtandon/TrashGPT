import subprocess
import os

dir_path = '../test_raw_data/'

for file_name in os.listdir(dir_path):
    if file_name.endswith('.m4a'):
        file_path = os.path.join(dir_path, file_name)
        
        # Set output file path and name
        output_file_name = file_name[:-4] + '.wav'
        output_file_path = os.path.join(dir_path, output_file_name)
        
        # Run FFmpeg command to convert file
        subprocess.run(['ffmpeg', '-i', file_path, '-acodec', 'pcm_s16le', '-ar', '44100', output_file_path])
        
print('Conversion complete.')
