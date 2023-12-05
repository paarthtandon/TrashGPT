import os
import shutil
from dotenv import load_dotenv
import pandas as pd
from pyannote.audio import Model, Inference
import torch
from pydub import AudioSegment
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt
import numpy as np
import json
from tqdm import tqdm
import random

load_dotenv()

HF_TOKEN = os.getenv('HF')
rttm_dir = '../data/rttm/'
wav_dir = '../data/wav/'
assignments_dir = '../data/assignments/'
garnt_dir = '../voice_cloning/source_samples/garnt/'
connor_dir = '../voice_cloning/source_samples/connor/'
joey_dir = '../voice_cloning/source_samples/joey/'

rttm_files = os.listdir(rttm_dir)
ref_files = []
for d in [garnt_dir, connor_dir, joey_dir]:
    fnames = os.listdir(d)
    for fname in fnames:
        ref_files.append(d + fname)

model = Model.from_pretrained("pyannote/embedding", use_auth_token=HF_TOKEN)
model.to(torch.device("cuda"))
inference = Inference(model, window="whole")

ref_embeds = {}
for fn in ref_files:
    ref_embeds[fn.split('/')[-1]] = inference(fn)

speakers = ['SPEAKER_00', 'SPEAKER_01', 'SPEAKER_02']
for rttm_fn in tqdm(rttm_files):
    rttm_path = rttm_dir + rttm_fn
    rttm = pd.read_csv(rttm_path, sep=' ', names=[
        "type", "file", "channel", "start", "duration", "NA1", "NA2", "speaker", "NA3", "NA4"
    ])
    audio = AudioSegment.from_file(wav_dir + rttm_path[:-4].split('/')[-1] + 'wav')
    os.makedirs('snips', exist_ok=True)
    
    speaker_sims = {}
    for speaker in speakers:
        rttm_s = rttm[rttm['speaker'] == speaker]
        rttm_s = rttm_s.sort_values('duration', ascending=False)
        if rttm_s.shape[0] >= 20:
            rttm_s = rttm_s.iloc[:10]
        
        starts = rttm_s['start'].tolist()
        durations = rttm_s['duration'].tolist()
        snippet_embeds = []
        for i, start in enumerate(starts):
            duration = durations[i]
            start = start * 1000
            duration = duration * 1000
            end = start + duration
            snippet = audio[start:end]
            snippet.export(f'snips/{speaker}_snippet_{i}.wav', format='wav')
            snippet_embeds.append(inference(f'snips/{speaker}_snippet_{i}.wav'))
    
        sims = {}
        for ref_fn, ref_embed in ref_embeds.items():
            name = ref_fn.split('_')[0]
            if name not in sims:
                sims[name] = []
            
            dists = cdist([ref_embed], snippet_embeds, metric="cosine")[0].tolist()
            sims[name].extend(dists)
        
        # names = []
        # means = []
        # errors = []

        # for name, distances in sims.items():
        #     names.append(name)
        #     means.append(np.mean(distances))
        #     errors.append(np.std(distances))

        # Plotting the bar graph with error bars
        # plt.figure(figsize=(10, 6))
        # plt.bar(names, means, yerr=errors, capsize=5)
        # plt.xlabel('Name Pairs')
        # plt.ylabel('Average Cosine Distance')
        # plt.title('Average Cosine Distance Between Name Pairs with Error Bars')
        # plt.xticks(rotation=45)
        # plt.tight_layout()
        # plt.savefig(f'{speaker}_bars.png')

        mean_sims = {}
        for name, s in sims.items():
            mean_sims[name] = np.mean(s)
        
        speaker_sims[speaker] = mean_sims
    shutil.rmtree('snips')

    assignments = {}
    available_speakers = ['SPEAKER_00', 'SPEAKER_01', 'SPEAKER_02']
    available_names = ['connor', 'garnt', 'joey']
    random.shuffle(available_names)
    for name in available_names:
        sims_per_speaker = {}
        for speaker, sims in speaker_sims.items():
            sims_per_speaker[speaker] = sims[name]
        top_sims = sorted(sims_per_speaker.items(), key=lambda x: x[1])
        top_sim = [sim[0] for sim in top_sims if sim[0] in available_speakers][0]
        available_speakers.remove(top_sim)
        assignments[name] = top_sim
    
    with open(f'{assignments_dir}/{rttm_path[:-4].split("/")[-1]}json', 'w') as file:
        json.dump(assignments, file)
