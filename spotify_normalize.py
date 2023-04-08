import os
from tqdm import tqdm
from pydub import AudioSegment, effects
from multiprocessing import Pool

BASE_DIR = r'C:\Users\Jason\Downloads\Pytube'
OUT_DIR = r'C:\Users\Jason\Downloads\Pytube_music'
ERROR_LOG = r'C:\Users\Jason\Downloads\error.log'
ERROR_SONG = []

def normalize_sound(file_name):
    try:
        artist, songname = file_name.rstrip(".mp3").split('-')
        artist, songname = artist.strip(), songname.strip()

        rawsound = AudioSegment.from_file(os.path.join(BASE_DIR, file_name))
        normalizedsound = effects.normalize(rawsound)
        normalizedsound.export(os.path.join(OUT_DIR, file_name), format="mp3")
    except:
        ERROR_SONG.append(file_name)
        print(file_name)
        pass

def main():
    song_lists = []
    for file in os.listdir(BASE_DIR):
        if file.endswith(".mp3"):
            song_lists.append(file)
    
    with Pool(4) as pool:
        r = list(tqdm(pool.imap(normalize_sound, song_lists), total=len(song_lists)))
        pool.close()
        pool.join()

    f = open(ERROR_LOG, "w")
    f.write(str(len(ERROR_SONG)))
    for i in ERROR_SONG:
        f.write(i)
    f.close()


if __name__ == '__main__':
    main()