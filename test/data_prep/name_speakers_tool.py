from pydub import AudioSegment
import pandas as pd
import os
import pathlib

audio_dir = '../test_raw_data/'
diar_dir = 'speech_diarization/'
trans_dir = 'annotated/'
write_dir = 'annotated_w_names/'


def reload(fileName):
    return pd.read_csv(diar_dir + fileName, sep=' ', names=["type", "file", "channel", "start", "duration", "NA1", "NA2", "speaker", "NA3", "NA4"])


def printInstruction():
    print('Please enter the following commands to use the tool')
    print('1. audio: to listen to a random snippet of the audio for the current speaker')
    print('2. label: to label the current speaker')
    print('3. next: to move on to the next speaker')
    print('4. quit/exit: to quit the program')


def fileNotEditted(fileName):
    file = pd.read_csv(diar_dir + fileName, sep=' ', names=[
                       "type", "file", "channel", "start", "duration", "NA1", "NA2", "speaker", "NA3", "NA4"])
    speaker = file['speaker'].unique()
    for element in speaker:
        if element[0:7] != 'SPEAKER':
            return None
    return file


def fileNotCreated(fileName):
    if os.path.exists(write_dir + fileName):
        return None
    file = pd.read_csv(diar_dir + fileName, sep=' ', names=[
                       "type", "file", "channel", "start", "duration", "NA1", "NA2", "speaker", "NA3", "NA4"])
    speaker = file['speaker'].unique()
    for element in speaker:
        if element[0:7] != 'SPEAKER':
            return None
    return file


def get_episode_name(filename):
    return filename.split('.')[0]


def name_transcripts(ep_name, speaker_num, speaker_name):
    transcripts = os.listdir(write_dir)
    transcripts = [t for t in transcripts if ep_name in t]
    for t in transcripts:
        out_file = open(write_dir + t, 'r', encoding='utf-8')
        trans = out_file.read()
        trans = trans.replace(speaker_num, speaker_name)
        out_file.close()

        out_file = open(write_dir + t, 'w', encoding='utf-8')
        out_file.write(trans)
        out_file.close()


def check_transcripts(ep_name):
    transcripts = os.listdir(write_dir)
    transcripts = [t for t in transcripts if ep_name in t]
    for t in transcripts:
        out_file = open(write_dir + t, 'r', encoding='utf-8')
        trans = out_file.read()
        out_file.close()
        if '<SPEAKER_' in trans:
            return True
    return False


def analyzeInput(pdFile, audiofile, speaker, ep_name):

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
            # pdFile['speaker'] = pdFile['speaker'].replace(speaker, label)
            # pdFile.to_csv(write_dir + filename, sep=' ',
            #               index=False, header=False)
            name_transcripts(ep_name, speaker, label)
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
                # pdFile['speaker'] = pdFile['speaker'].replace(speaker, label)
                # pdFile.to_csv(write_dir + filename, sep=' ',
                #               index=False, header=False)
                name_transcripts(ep_name, speaker, label)
                print('Labeling complete')
                return
            else:
                print('Labeling canceled')
                analyzeInput(pdFile, audiofile, speaker, ep_name)
    if userInput == 'audio':
        pdFile = pdFile[pdFile['speaker'] == speaker]
        # duration = pdFile.loc[pdFile['duration'] > 10, 'duration'].values
        # start = pdFile.loc[pdFile['duration'] > 10, 'start'].values

        # # only use duration if it is longer than 10 seconds
        # try:
        #     randindex = rand.randint(0, len(duration) - 1)
        # except:
        #     print('No audio for this speaker with a duration greater than 10 seconds')
        #     duration = pdFile['duration'].values
        #     start = pdFile['start'].values
        #     randindex = rand.randint(0, len(start) - 1)
        # start = start[randindex]
        # duration = duration[randindex]
        # start = start * 1000
        # duration = duration * 1000
        # end = start + duration
        # snippet = audiofile[start:end]
        # snippet.export('snippet.wav', format='wav')
        # os.system('snippet.wav')

        duration = pdFile.sort_values('duration', ascending=False)
        if duration.shape[0] >= 5:
            duration = duration.iloc[:5]
        else:
            duration = duration
        
        starts = duration['start'].tolist()
        durations = duration['duration'].tolist()
        for i, start in enumerate(starts):
            duration = durations[i]
            start = start * 1000
            duration = duration * 1000
            end = start + duration
            snippet = audiofile[start:end]
            snippet.export(f'snippet{i}.wav', format='wav')


        # chunk = 1024
        # wf = wave.open('snippet.wav', 'rb')
        # p = pyaudio.PyAudio()
        # stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
        #                 channels=wf.getnchannels(),
        #                 rate=wf.getframerate(),
        #                 output=True)
        # data = wf.readframes(chunk)
        # while data:
        #     stream.write(data)
        #     data = wf.readframes(chunk)
        # stream.stop_stream()
        # stream.close()
        # p.terminate()
        analyzeInput(pdFile, audiofile, speaker, ep_name)


print('Welcome to the Speech Diarization Naming Tool')
# change the path below to the folder where you have the speech-diarization folder
pathtodata = pathlib.Path(diar_dir)
filesinlib = os.listdir(pathtodata)
for i, filename in enumerate(filesinlib):
    ep_name = get_episode_name(filename)
    # file = fileNotEditted(filename)
    file = fileNotEditted(filename)
    if file is not None and check_transcripts(ep_name):
        print(f'Working on: {filename} {i}/{len(filesinlib)}')
        audio = AudioSegment.from_file(audio_dir + filename[:-4] + 'm4a')
        speakers = file['speaker'].unique()
        speakers.sort()
        for speaker in speakers:
            print(f'Working on: {speaker}')
            printInstruction()
            analyzeInput(file, audio, speaker, ep_name)
            file = reload(filename)
    else:
        print(f'Skipping: {filename}')
