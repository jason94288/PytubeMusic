from fileinput import filename
import os

import pandas as pd
from tqdm import tqdm
from utils import *

BASE_DIR = r'C:\Users\Jason\Downloads\PyTube'
CSV_PATH = r'C:\Users\Jason\Downloads\PyTube.csv'

access_token = auth_process_kkbox()
fout = open(CSV_PATH, 'w', encoding='UTF-8')
for file_name in tqdm(os.listdir(BASE_DIR)):
    old_file_name = file_name.replace(",", ".")
    file_name = file_name.rstrip(".mp3")
    file_name = file_name.rstrip(".wma")
    file_name = file_name.replace("-", " ")

    songname, abumn_name, release_date, artists = search_music_kkbox(file_name, access_token)
    try:
        new_name = artists.split(";")[0] + " - " + songname + ".mp3"
    except:
        new_name = ''
    # For Spotify
    # fout.write(
    #     "%s, %s, %s, %s, %s, %s" %
    #     (old_file_name, songname, artists[0],
    #      abumn_name, release_date, '; '.join(artists)))

    # For KKBOX
    fout.write(
        "%s,%s,%s,%s,%s,%s" %
        (old_file_name, new_name, songname, artists, abumn_name, release_date))

    fout.write('\n')
fout.close()
