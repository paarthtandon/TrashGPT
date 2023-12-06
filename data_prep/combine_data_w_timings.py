import json
import os
import pandas as pd
import numpy as np
from concurrent.futures import ProcessPoolExecutor
import time

def process_transcript_file(transcript_file, rttm_dir, transcript_dir, assignment_dir, annotated_dir, rttm_header, event_header):
    rttm_file = os.path.splitext(transcript_file)[0][:-3] + '.rttm'
    assignment_file = os.path.splitext(transcript_file)[0][:-3] + '.json'
    annotated_file = os.path.splitext(transcript_file)[0][:-3] + '.txt'

    try:
        rttm = pd.read_csv(os.path.join(rttm_dir, rttm_file), delimiter=' ', names=rttm_header)
    except FileNotFoundError:
        return  # Skip if RTTM file not found

    rttm['start_ms'] *= 1000
    rttm['duration_ms'] *= 1000
    rttm = rttm[rttm['duration_ms'] > 500]

    try:
        with open(os.path.join(transcript_dir, transcript_file), 'r') as file:
            transcript = json.load(file)['events']
    except FileNotFoundError:
        return  # Skip if transcript file not found

    transcript = [t for t in transcript if 'segs' in t and 'tStartMs' in t and 'dDurationMs' in t]
    trans_prep = [[t['tStartMs'], t['dDurationMs'], ''.join([seg['utf8'] for seg in t['segs']]).replace('\n', ' ')] for t in transcript if ''.join([seg['utf8'] for seg in t['segs']]) != '\n']
    
    events = pd.DataFrame(trans_prep, columns=event_header)
    events['end_ms'] = events['start_ms'] + events['duration_ms']
    rttm['end_ms'] = rttm['start_ms'] + rttm['duration_ms']

    try:
        with open(os.path.join(assignment_dir, assignment_file), 'r') as file:
            assignments = json.load(file)
    except FileNotFoundError:
        return  # Skip if assignment file not found

    assignments = {v: k for k, v in assignments.items()}

    out = ''
    try:
        for _, event in events.iterrows():
            rttm['start_distance'] = np.abs(rttm['start_ms'] - event['start_ms'])
            rttm['end_distance'] = np.abs(rttm['end_ms'] - event['end_ms'])
            first_speaker = rttm.iloc[rttm['start_distance'].idxmin()]
            last_speaker = rttm.iloc[rttm['end_distance'].idxmin()]
            speaker = first_speaker['Speaker Name'] if first_speaker['start_distance'] < last_speaker['end_distance'] else last_speaker['Speaker Name']
            out += f'{event["start_ms"] / 1000 :09.3f} <{assignments[speaker]}>: {event["text"]}\n'
    except Exception as e:
        print(f"Error occurred: {e}")

    with open(os.path.join(annotated_dir, annotated_file), 'w') as human:
        human.write(out)

def main():
    rttm_dir = '../data/rttm/'
    transcript_dir = '../data/json/'
    assignment_dir = '../data/assignments/'
    annotated_dir = '../data/constructed/'

    rttm_header = ['Type', 'File ID', 'Channel ID', 'start_ms', 'duration_ms', 'Orthography Field', 'Speaker Type', 'Speaker Name', 'Confidence Score', 'Signal Lookahead Time']
    event_header = ['start_ms', 'duration_ms', 'text']

    if not os.path.exists(annotated_dir):
        os.makedirs(annotated_dir)

    start_time = time.time()

    transcript_files = os.listdir(transcript_dir)
    with ProcessPoolExecutor() as executor:  # Adjust max_workers as needed
        for transcript_file in transcript_files:
            executor.submit(process_transcript_file, transcript_file, rttm_dir, transcript_dir, assignment_dir, annotated_dir, rttm_header, event_header)

    print("--- %s seconds ---" % (time.time() - start_time))

if __name__ == "__main__":
    main()
