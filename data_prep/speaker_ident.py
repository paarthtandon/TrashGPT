import os
from dotenv import load_dotenv
from pyannote.audio import Pipeline

load_dotenv()
HF_TOKEN = os.getenv('HF')
data_dir = '../data/'

pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization@2.1', use_auth_token=HF_TOKEN)

print('pipeline loaded')

# apply the pipeline to an audio file
diarization = pipeline(
    data_dir + 'Animals We Could Beat in a Fight ｜ Trash Taste #91 [ZWS2nFo7eEo].wav' # ,
    # min_speakers = 3
)

print('diarization complete')

# dump the diarization output to disk using RTTM format
with open("audio.rttm", "w") as rttm:
    diarization.write_rttm(rttm)
