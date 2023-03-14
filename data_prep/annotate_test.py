import json
import pandas as pd

rttm_file = '../speech_diarization/Animals_We_Could_Beat_in_a_Fight__Trash_Taste_91_ZWS2nFo7eEo.rttm'
human_trans_file = '../data/Animals_We_Could_Beat_in_a_Fight__Trash_Taste_91_ZWS2nFo7eEo.en-ehkg1hFWq8A.json3'
auto_trans_file = '../data/Animals_We_Could_Beat_in_a_Fight__Trash_Taste_91_ZWS2nFo7eEo.en.json3'

rttm_header = ['Type', 'File ID', 'Channel ID', 'Turn Onset', 'Turn Duration', 'Orthography Field', 'Speaker Type', 'Speaker Name', 'Confidence Score', 'Signal Lookahead Time']
rttm = pd.read_csv(rttm_file, delimiter=' ', names=rttm_header)
rttm = rttm.drop(columns=['Type', 'Channel ID', 'Orthography Field', 'Speaker Type', 'Confidence Score', 'Signal Lookahead Time'])

# convert seconds to ms
rttm['Turn Onset'] = rttm['Turn Onset'] * 1000
rttm['Turn Duration'] = rttm['Turn Duration'] * 1000

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

event_header = ['start_ms', 'end_ms', 'text']
human_events = pd.DataFrame(human_trans_prep, columns=event_header)
auto_events = pd.DataFrame(auto_trans_prep, columns=event_header)

print(rttm.head(10))
print(human_events.head(10))
print(auto_events.head(10))
