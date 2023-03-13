import os
from dotenv import load_dotenv
from pyannote.audio import Pipeline
import time
import sys

load_dotenv()
HF_TOKEN = os.getenv('HF')
print(HF_TOKEN)
data_dir = '../data/'
fileName = sys.argv[1]

pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization@2.1', use_auth_token=HF_TOKEN)

print('pipeline loaded')

start_time = time.time()

# apply the pipeline to an audio file
diarization = pipeline(
    data_dir + fileName,
    min_speakers = 3
)

print('diarization complete')

# dump the diarization output to disk using RTTM format
with open(f'{fileName}.rttm', "w") as rttm:
    diarization.write_rttm(rttm)

print("--- %s seconds ---" % (time.time() - start_time))
