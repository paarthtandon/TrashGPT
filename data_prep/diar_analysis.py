import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

diar_dir = './speech_diarization/'
files = os.listdir(diar_dir)
files = [diar_dir + f for f in files]
dfs = [pd.read_csv(f, sep=' ', names=["type", "file", "channel", "start", "duration", "NA1", "NA2", "speaker", "NA3", "NA4"]).drop(columns=["type", "file", "channel", "NA1", "NA2", "NA3", "NA4"]) for f in files]

df = dfs[0]
df['end'] = df['start'] + df['duration']
intervals = pd.IntervalIndex.from_arrays(df['start'], df['end'], closed='left')
overlap_df = pd.DataFrame(columns=['start', 'duration', 'speaker', 'overlap_with'])

overlap_list = []

# iterate over intervals and check for overlaps
for i in range(len(intervals)):
    # check if interval overlaps with others
    overlaps = intervals.overlaps(intervals[i])
    if sum(overlaps) > 1:
        # get the original row data
        row = df.iloc[i].to_dict()
        # get overlapping speakers
        overlap_speakers = df[overlaps]['speaker'].tolist()
        # remove current speaker from the list
        overlap_speakers.remove(row['speaker'])
        # add overlapped speakers to the row
        row['overlap_with'] = overlap_speakers
        overlap_list.append(row)

# convert list of dictionaries to a dataframe
overlap_df = pd.DataFrame(overlap_list)

# assign a numeric id to each speaker
df['speaker_id'] = df['speaker'].astype('category').cat.codes

# add 'speaker_id' column to overlap_df
overlap_df['speaker_id'] = overlap_df['speaker'].apply(lambda x: df[df['speaker'] == x]['speaker_id'].iloc[0])

# merge df with overlap_df and identify which rows are only in df
merged_df = df.merge(overlap_df, indicator=True, how='outer')
non_overlap_df = merged_df[merged_df['_merge'] == 'left_only']

plt.figure(figsize=(12, 6))

# create scatter for non-overlapping speeches
plt.scatter(non_overlap_df['start_x'], non_overlap_df['speaker_id_x'], alpha=0.7)

# provide labels for the y-axis with speaker names
plt.yticks(np.arange(df['speaker_id'].min(), df['speaker_id'].max()+1), df['speaker'].unique())

plt.xlabel('Time (s)')
plt.ylabel('Speaker')
plt.title('Non-overlap instances over time')

plt.savefig('plot.png')