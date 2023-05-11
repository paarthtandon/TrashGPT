# TrashGPT

## Setup

1. Install Python 3.10.x
2. Setup a [virtual environment](https://docs.python.org/3/tutorial/venv.html): `python -m venv .venv`
3. Activate virtual environment. Command is platform dependent.
4. Install [PyTorch](https://pytorch.org/). Make sure to use the command on their site. It is platform dependent.
5. Install other requirements: `pip install -r requirements.txt`

## Data Download

1. Create directory `./data/`, move into the directory.
2. Run `yt-dlp.exe --yes-playlist --write-sub --write-auto-sub --sub-lang "en.*" --sub-format json3 -f m4a https://www.youtube.com/playlist?list=PLUHmmIt9sU6i4JlDABqLeWybD_ZrJf9LB`

## Documents

- [Proposal](https://www.overleaf.com/project/63ebb492e3b98236eca9357b) (March 8th)
- [Final Report](https://www.overleaf.com/6268427319fsgdzvcrfsyq) (May 17th)
- [Playlist](https://youtube.com/playlist?list=PLUHmmIt9sU6i4JlDABqLeWybD_ZrJf9LB)
