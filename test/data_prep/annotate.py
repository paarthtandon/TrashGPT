import json
import os
import time
import pandas as pd
import numpy as np
import tqdm

rttm_dir = '../speech_diarization/'
transcript_dir = '../transcripts/'
annotated_dir = '../annotated/'

rttm_header = ['Type', 'File ID', 'Channel ID', 'start_ms', 'duration_ms', 'Orthography Field', 'Speaker Type', 'Speaker Name', 'Confidence Score', 'Signal Lookahead Time']
event_header = ['start_ms', 'duration_ms', 'text']

if not os.path.exists(annotated_dir):
    os.makedirs(annotated_dir)

start_time = time.time()

transcript_files = os.listdir(transcript_dir)
for transcript_file in tqdm.tqdm(transcript_files):
    rttm_file = transcript_file.split('.')[0] + '.rttm'
    annotated_file = os.path.splitext(transcript_file)[0] + '.txt'

    rttm = pd.read_csv(rttm_dir + rttm_file, delimiter=' ', names=rttm_header)
    rttm = rttm.drop(columns=['Type', 'Channel ID', 'Orthography Field', 'Speaker Type', 'Confidence Score', 'Signal Lookahead Time'])

    rttm['start_ms'] = rttm['start_ms'] * 1000
    rttm['duration_ms'] = rttm['duration_ms'] * 1000

    transcript = json.load(open(transcript_dir + transcript_file, 'r'))['events']
    transcript = [t for t in transcript if 'segs' in t]
    transcript = [t for t in transcript if 'tStartMs' in t]
    transcript = [t for t in transcript if 'dDurationMs' in t]

    trans_prep = []
    for event in transcript:
        seg_text = ''.join([seg['utf8'] for seg in event['segs']])
        if seg_text == '\n':
            continue
        trans_prep.append([event['tStartMs'], event['dDurationMs'], seg_text])
    
    events = pd.DataFrame(trans_prep, columns=event_header)

    events['end_ms'] = events['start_ms'] + events['duration_ms']
    rttm['end_ms'] = rttm['start_ms'] + rttm['duration_ms']

    out = ''
    for i in range(events.shape[0]):
        event = events.iloc[i]
        rttm['start_distance'] = np.abs(rttm['start_ms'] - event['start_ms'])
        rttm['end_distance'] = np.abs(rttm['end_ms'] - event['end_ms'])

        rttm.sort_values('start_distance', inplace=True)
        first_speaker = rttm.iloc[0]
        first_dist = rttm.iloc[0]['start_distance']

        rttm.sort_values('end_distance', inplace=True)
        last_speaker = rttm.iloc[0]
        last_dist = rttm.iloc[0]['end_distance']

        speaker = first_speaker['Speaker Name'] if first_dist < last_dist else last_speaker['Speaker Name']

        out += f'<{speaker}> {event["text"]} </{speaker}>\n'

    with open(annotated_dir + annotated_file, 'w') as human:
        human.write(out)

print("--- %s seconds ---" % (time.time() - start_time))
