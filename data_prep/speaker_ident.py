import os
from dotenv import load_dotenv
from pyannote.audio import Pipeline
import time

load_dotenv()
HF_TOKEN = os.getenv('HF')
data_dir = '../data/'
output_dir = '../data/'

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization@2.1', use_auth_token=HF_TOKEN)

print('pipeline loaded')
start_time = time.time()

for filename in os.listdir(data_dir):
    if filename.endswith('.wav'):

        input_file_path = os.path.join(data_dir, filename)
        output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.rttm')

        print(f'starting diarization of {filename}.')

        # apply the pipeline to an audio file
        diarization = pipeline(
            input_file_path,
            min_speakers = 3
        )

        # dump the diarization output to disk using RTTM format
        with open(output_file_path, "w") as rttm:
            diarization.write_rttm(rttm)
        print(f'output written to {output_file_path}')

print(f'time taken: {time.time() - start_time} seconds')
