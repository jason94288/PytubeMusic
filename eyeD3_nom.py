import os
import eyed3
import numpy as np
import pandas as pd
from tqdm import tqdm

BASE_DIR = r'C:\Users\Jason\Downloads\pyTube\Youtube'
CSV_PATH = r'C:\Users\Jason\Downloads\checked.csv'

df = pd.read_csv(CSV_PATH)
df = df.replace(np.nan, '')

for index, row in df.iterrows():
    # Rename
    old_name = os.path.join(BASE_DIR, row['Filename'])

    try:
        audiofile = eyed3.load(old_name)
        audiofile.tag.title = str(row['Title'])
        audiofile.tag.artist = str(row['Artist'])
        audiofile.tag.album = str(row['Album'])
        audiofile.tag.publisher = str(row['YT_ID'])
        audiofile.tag.save()
        
        # audiofile = eyed3.load(old_name)
        # if audiofile.tag.title is None:
        #     audiofile.tag.title = str(row['Title'])
        # if audiofile.tag.artist is None:
        #     audiofile.tag.artist = str(row['Artist'])
        # if audiofile.tag.album is None:
        #     audiofile.tag.album = str(row['Album'])
        # # if audiofile.tag.year is None:
        # #     audiofile.tag.year = str(row['Date'])
        # audiofile.tag.save()
    except OSError:
        print("OSError:", row['Title'], row['Filename'])
        continue
    except AttributeError:
        # print("AttributeError:", row['Filename'])
        continue
    
    # try:
    #     file_name = str(row['Artist']).strip() + '-' + str(row['Title']).strip() + '.mp3'
    #     new_name = os.path.join(BASE_DIR, file_name)
    #     os.rename(old_name, new_name)
    #     df.loc[index, 'Filename'] = file_name
    # except:
    #     print("Reame Error:", row['Filename'])
    #     continue
# df.to_csv(os.path.join(BASE_DIR, 'data.csv'), index=False, encoding='utf_8_sig')