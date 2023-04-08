import os
import eyed3
from tqdm import tqdm

BASE_DIR = r'C:\Users\Jason\Downloads\pyTube\PyTube'

all_files = os.listdir(BASE_DIR)
for filename in tqdm(all_files):
    audiofile = eyed3.load(os.path.join(BASE_DIR, filename))
    title = audiofile.tag.title
    artist = audiofile.tag.artist

    if artist is not None:
        file_name = artist.strip() + '-' + title.strip() + '.mp3'
    else:
        file_name = title.strip() + '.mp3'
    new_name = os.path.join(BASE_DIR, file_name)
    os.rename(os.path.join(BASE_DIR, filename), new_name)