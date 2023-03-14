import json
import time
import pandas as pd
import numpy as np

start_time = time.time()

rttm_file = '../speech_diarization/Animals_We_Could_Beat_in_a_Fight__Trash_Taste_91_ZWS2nFo7eEo.rttm'
human_trans_file = '../data/Animals_We_Could_Beat_in_a_Fight__Trash_Taste_91_ZWS2nFo7eEo.en-ehkg1hFWq8A.json3'
auto_trans_file = '../data/Animals_We_Could_Beat_in_a_Fight__Trash_Taste_91_ZWS2nFo7eEo.en.json3'

rttm_header = ['Type', 'File ID', 'Channel ID', 'start_ms', 'duration_ms', 'Orthography Field', 'Speaker Type', 'Speaker Name', 'Confidence Score', 'Signal Lookahead Time']
rttm = pd.read_csv(rttm_file, delimiter=' ', names=rttm_header)
rttm = rttm.drop(columns=['Type', 'Channel ID', 'Orthography Field', 'Speaker Type', 'Confidence Score', 'Signal Lookahead Time'])

# convert seconds to ms
rttm['start_ms'] = rttm['start_ms'] * 1000
rttm['duration_ms'] = rttm['duration_ms'] * 1000

human_trans = json.load(open(human_trans_file, 'r'))['events']
auto_trans = json.load(open(auto_trans_file, 'r'))['events']

# filter events we don't want to consider
human_trans = [t for t in human_trans if 'segs' in t]
auto_trans = [t for t in auto_trans if 'segs' in t]
human_trans = [t for t in human_trans if 'tStartMs' in t]
auto_trans = [t for t in auto_trans if 'tStartMs' in t]
human_trans = [t for t in human_trans if 'dDurationMs' in t]
auto_trans = [t for t in auto_trans if 'dDurationMs' in t]

# interate over events to retain text in one string
human_trans_prep = []
auto_trans_prep = []

for event in human_trans:
    seg_text = ''.join([seg['utf8'] for seg in event['segs']])
    if seg_text == '\n':
        continue
    human_trans_prep.append([event['tStartMs'], event['dDurationMs'], seg_text])

for event in auto_trans:
    seg_text = ''.join([seg['utf8'] for seg in event['segs']])
    if seg_text == '\n':
        continue
    auto_trans_prep.append([event['tStartMs'], event['dDurationMs'], seg_text])

# load into DF
event_header = ['start_ms', 'duration_ms', 'text']
human_events = pd.DataFrame(human_trans_prep, columns=event_header)
auto_events = pd.DataFrame(auto_trans_prep, columns=event_header)

# get end time stamps
human_events['end_ms'] = human_events['start_ms'] + human_events['duration_ms']
auto_events['end_ms'] = auto_events['start_ms'] + auto_events['duration_ms']
rttm['end_ms'] = rttm['start_ms'] + rttm['duration_ms']

# create annotations
human_out = ''
auto_out = ''

for i in range(human_events.shape[0]):
    event = human_events.iloc[i]
    rttm['distance'] = np.sqrt((rttm['start_ms'] - event['start_ms']) ** 2 + (rttm['end_ms'] - event['end_ms']) ** 2)
    try:
        speaker = rttm[rttm['start_ms'] >= event['start_ms']].sort_values('distance').iloc[0]['Speaker Name']
    except:
        speaker = rttm.sort_values('distance').iloc[0]['Speaker Name']
    human_out += f'<{speaker}> {event["text"]} </{speaker}>\n'

for i in range(auto_events.shape[0]):
    event = auto_events.iloc[i]
    rttm['distance'] = np.sqrt((rttm['start_ms'] - event['start_ms']) ** 2 + (rttm['end_ms'] - event['end_ms']) ** 2)
    try:
        speaker = rttm[rttm['start_ms'] >= event['start_ms']].sort_values('distance').iloc[0]['Speaker Name']
    except:
        speaker = rttm.sort_values('distance').iloc[0]['Speaker Name']
    auto_out += f'<{speaker}> {event["text"]} </{speaker}>\n'

with open('test_annot_human.txt', 'w') as human:
    human.write(human_out)

with open('test_annot_auto.txt', 'w') as auto:
    auto.write(auto_out)

print("--- %s seconds ---" % (time.time() - start_time))
