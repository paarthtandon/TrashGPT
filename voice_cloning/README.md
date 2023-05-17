# Voice Cloning

We used [tortoise-tts](https://github.com/neonbjb/tortoise-tts), a transformer based voice model, to generate our audio.

## Setup

1. Clone [tortoise-tts](https://github.com/neonbjb/tortoise-tts).
2. Follow setup instructions for [tortoise-tts](https://github.com/neonbjb/tortoise-tts).
3. Add each folder in `source_samples/` to `tortoise-tts/tortoise/voices/`.
4. Change the text in `create_tts_job.py` to the desired text and run it.
5. Run the generated `create_audio.bat` file.

## Parser

To ensure that each text segment is not too long, the parser breaks up each segment into a maximum of 200 characters. In our testing, this was the longest they could be and still be small enough to run locally on a RTX 3060 12GB.
