from pydub import AudioSegment
import pandas as pd
import os
import pathlib
import random as rand
import pyaudio
import wave

read_dir = '../speech_diarization/'
write_dir = '../annotated_w_names/'


def reload(fileName):
    return pd.read_csv(read_dir + fileName, sep=' ', names=["type", "file", "channel", "start", "duration", "NA1", "NA2", "speaker", "NA3", "NA4"])


def printInstruction():
    print('Please enter the following commands to use the tool')
    print('1. audio: to listen to a random snippet of the audio for the current speaker')
    print('2. label: to label the current speaker')
    print('3. next: to move on to the next speaker')
    print('4. quit/exit: to quit the program')


def fileNotEditted(fileName):
    file = pd.read_csv(read_dir + fileName, sep=' ', names=[
                       "type", "file", "channel", "start", "duration", "NA1", "NA2", "speaker", "NA3", "NA4"])
    speaker = file['speaker'].unique()
    for element in speaker:
        if element[0:7] != 'SPEAKER':
            return None
    return file


def analyzeInput(pdFile, audiofile, speaker):
    setofcommands = ['audio', 'label', 'next', 'quit', 'exit']
    while True:
        try:
            userInput = input('Enter a command: ')
            if userInput not in setofcommands:
                print('Please enter a valid command')
                continue
            break
        except:
            print('Please enter a valid command')
    userInput = userInput.lower()
    print('==========================================================================')
    if userInput == 'quit':
        print('Quitting the program')
        exit(0)
    if userInput == 'exit':
        print('Quitting the program')
        exit(0)
    if userInput == 'next':
        return
    if userInput == 'label':
        label = input('Enter a label for the speaker: ')
        print(f'Labeling {speaker} as {label}, are you sure?')
        while True:
            try:
                confirm = input('Enter yes or no: ')
                break
            except:
                print('Please enter yes or no')
        if confirm == 'yes':
            pdFile['speaker'] = pdFile['speaker'].replace(speaker, label)
            pdFile.to_csv(write_dir + filename, sep=' ',
                          index=False, header=False)
            print('Labeling complete')
            return
        else:
            label = input('Enter a label for the speaker: ')
            print(f'Labeling {speaker} as {label}, are you sure?')
            while True:
                try:
                    confirm = input('Enter yes or no: ')
                    break
                except:
                    print('Please enter yes or no')
            if confirm == 'yes':
                pdFile['speaker'] = pdFile['speaker'].replace(speaker, label)
                pdFile.to_csv(write_dir + filename, sep=' ',
                              index=False, header=False)
                print('Labeling complete')
                return
            else:
                print('Labeling canceled')
                analyzeInput(pdFile, audiofile, speaker)
    if userInput == 'audio':
        pdFile = pdFile[pdFile['speaker'] == speaker]
        duration = pdFile.loc[pdFile['duration'] > 10, 'duration'].values
        start = pdFile.loc[pdFile['duration'] > 10, 'start'].values
        # only use duration if it is longer than 10 seconds
        try:
            randindex = rand.randint(0, len(duration) - 1)
        except:
            print('No audio for this speaker with a duration greater than 10 seconds')
            duration = pdFile['duration'].values
            start = pdFile['start'].values
            randindex = rand.randint(0, len(start) - 1)
        start = start[randindex]
        duration = duration[randindex]
        start = start * 1000
        duration = duration * 1000
        end = start + duration
        snippet = audiofile[start:end]
        snippet.export('snippet.wav', format='wav')
        os.system('snippet.wav')
        chunk = 1024
        wf = wave.open('snippet.wav', 'rb')
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(chunk)
        while data:
            stream.write(data)
            data = wf.readframes(chunk)
        stream.stop_stream()
        stream.close()
        p.terminate()
        analyzeInput(pdFile, audiofile, speaker)


print('Welcome to the Speech Diarization Tool')
# change the path below to the folder where you have the speech-diarization folder
pathtodata = pathlib.Path('../data/')
filesinlib = os.listdir(pathtodata)
for filename in filesinlib:
    file = fileNotEditted(filename)
    if file is not None:
        print(f'Working on: {filename}')
        audio = AudioSegment.from_file('data/' + filename[:-4] + 'wav')
        speakers = file['speaker'].unique()
        speakers.sort()
        for speaker in speakers:
            print(f'Working on: {speaker}')
            printInstruction()
            analyzeInput(file, audio, speaker)
            file = reload(filename)
