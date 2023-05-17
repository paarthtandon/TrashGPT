# TrashGPT

Welcome to our repository. This project was completed for CS 685 (Spring 2023). The goal of this project is to generate clips of the Trash Taste Podcast. Each folder specifies one aspect of the data pipeline.

## Setup

There are many different subroutines in this repository, and I would recommend only installing the packages needed for that subroutine to avoid package conflicts.

1. Install Python 3.10.X
2. Setup a [virtual environment](https://docs.python.org/3/tutorial/venv.html): `python -m venv .venv`
3. Activate virtual environment. Command is platform dependent.
4. Install [PyTorch](https://pytorch.org/). Make sure to use the command on their site. It is platform dependent.
5. Install other requirements as seen in the README of the pipeline component you are running.

## Pipeline

1. Data download
    - Create directory `raw_data/`, move into the directory.
    - Run `yt-dlp.exe --yes-playlist --write-sub --write-auto-sub --sub-lang "en.*" --sub-format json3 -f m4a https://www.youtube.com/playlist?list=PLUHmmIt9sU6i4JlDABqLeWybD_ZrJf9LB`
2. Data preprocessing (look in `data_prep/`)
    - Speech diarization
    - Speaker naming tool
    - Dataset formulation
3. Training the models and generating transcripts (look in `modeling/`)
    - Training and generation code for GPT2-Small, GPT2-Med, Bloom 560M, and LLaMA 7B
4. Voice cloning and audio performance generation (look in `voice_cloning/`)
    - Transcript parser
    - TTS with voice cloning using [tortoise-tts](https://github.com/neonbjb/tortoise-tts)

## Results

- Sample text generations are in `test/`
- [Evaluation](https://docs.google.com/spreadsheets/d/1jtsw4g0nGK2sbywgND0AkrXzY3MM4u4L0yGolVhIMPU/edit?usp=sharing)
- [LLaMA 7B Clip](https://youtu.be/rR67-ePpWF4)
- [Bloom 560M Clip](https://youtu.be/DJM6BLNaWhI)
- [GPT2-Medium Clip](https://youtu.be/DnMJ3biSkKQ)

## Other Documents

- [Proposal](https://www.overleaf.com/project/63ebb492e3b98236eca9357b)
- [Final Report](https://www.overleaf.com/6268427319fsgdzvcrfsyq)
- [Dataset Playlist](https://youtube.com/playlist?list=PLUHmmIt9sU6i4JlDABqLeWybD_ZrJf9LB)
