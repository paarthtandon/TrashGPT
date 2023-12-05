import os
from dotenv import load_dotenv
import time
import torch
from pyannote.audio import Pipeline
from concurrent.futures import ProcessPoolExecutor

# Global variable for the model, unique to each process
global_pipeline = None

def init_process(hf_token):
    global global_pipeline
    print(f'Initializing process {os.getpid()}')
    global_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=hf_token)
    global_pipeline.to(torch.device("cuda"))
    print(f'Process {os.getpid()} initialized')

def process_file(filename, data_dir, output_dir):
    global global_pipeline

    rttm_file = os.path.splitext(filename)[0] + '.rttm'
    if filename.endswith('.wav') and rttm_file not in os.listdir(data_dir):
        input_file_path = os.path.join(data_dir, filename)
        output_file_path = os.path.join(output_dir, os.path.splitext(filename)[0] + '.rttm')

        print(f'Process {os.getpid()} starting diarization of {filename}')
        # apply the pipeline to an audio file
        diarization = global_pipeline(input_file_path, min_speakers=3, max_speakers=3)

        # dump the diarization output to disk using RTTM format
        with open(output_file_path, "w") as rttm:
            diarization.write_rttm(rttm)
        print(f'Process {os.getpid()} completed diarization of {filename}')

def main():
    load_dotenv()
    HF_TOKEN = os.getenv('HF')
    data_dir = '../data/wav/'
    output_dir = '../data/rttm/'

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print('Starting parallel diarization process')
    start_time = time.time()

    data_files = [f for f in os.listdir(data_dir) if f.endswith('.wav')]

    with ProcessPoolExecutor(max_workers=2, initializer=init_process, initargs=(HF_TOKEN,)) as executor:
        executor.map(process_file, data_files, [data_dir]*len(data_files), [output_dir]*len(data_files))

    print(f'Time taken: {time.time() - start_time} seconds')

if __name__ == "__main__":
    main()
