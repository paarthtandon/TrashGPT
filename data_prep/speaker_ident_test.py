import os
from dotenv import load_dotenv
from pyannote.audio import Pipeline
import time

load_dotenv()
HF_TOKEN = os.getenv('HF')
data_dir = '../data/'

pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization@2.1', use_auth_token=HF_TOKEN)

print('pipeline loaded')

start_time = time.time()

# apply the pipeline to an audio file
diarization = pipeline(
    data_dir + 'Animals_We_Could_Beat_in_a_Fight__Trash_Taste_91_ZWS2nFo7eEo.wav',
    min_speakers = 3
)

print('diarization complete')

# dump the diarization output to disk using RTTM format
with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)

print("--- %s seconds ---" % (time.time() - start_time))
