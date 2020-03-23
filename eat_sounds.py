import os
from pydub import AudioSegment
from pydub.playback import play
import random


BASE_MP3_PATH = "/home/pi/projects/eat/assets/mp3"

def get_list_files(category):
    if category not in ["farts","wisdom"]:
        return []
    files = [ BASE_MP3_PATH + "/" + category + "/" +
              x for x in  os.listdir(BASE_MP3_PATH + "/" + category) if x.endswith(".mp3")]
    return files

def select_audio_files(farts_max = 1):
    '''
        farts_max - integer representing max number of farts
    '''
    possible_farts = get_list_files("farts")
    selected_farts = []
    number_possible = len(possible_farts)
    index_max = number_possible - 1
    while len(selected_farts) < farts_max :
        selected_farts.append(possible_farts[random.randint(0, index_max)])
    # append wisdom here
    
    return selected_farts


def assemble_audio(selected_files):
    assembled_audio = AudioSegment.empty()
    for selected_file in selected_files:
        assembled_audio += AudioSegment.from_file(selected_file, "mp3")
    return assembled_audio


def dispense_wisdom(fart_max = random.randint(1,4)):
    selected_files = select_audio_files(fart_max)
    try:
        play(assemble_audio(selected_files))
    except ValueError:
        print(selected_files)
