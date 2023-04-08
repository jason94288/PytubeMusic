import os
import numpy as np
import pandas as pd
from tqdm import tqdm
from utils import *

# ===
# Parameter
# ===
BASE_DIR = r'C:\Users\Jason\Downloads\pytube\PyTube'
SKIP_YT_ID = 0
SKIP_ID3 = 0

# ===
# Init
# ===
access_token = auth_process_kkbox()
try:
    local_df = pd.read_csv(os.path.join(BASE_DIR, 'data.csv'))
except:
    local_df = pd.DataFrame({'Status': [],
                             'Filename': [],
                             'YT_Title': [],
                             'YT_ID': [],
                             'Title': [],
                             'Artist': [],
                             'Album': [],
                             'Date': []})

# ===
# Check status
# ===
print('=== Checking Status ===')
all_files = os.listdir(BASE_DIR)

for index, row in local_df.iterrows():

    # Find lost files
    if row['Filename'] not in all_files:
        row['Status'] = 'Missing'

    # Reset Status
    if row['Status'] == 'Modified':
        local_df.loc[index, 'Status'] = ''
    if row['Status'] == 'New':
        local_df.loc[index, 'Status'] = ''
    if row['Status'] == 'Youtube':
        local_df.loc[index, 'Status'] = ''

for filename in tqdm(all_files):

    # Filter out not aduio files
    _, file_extension = os.path.splitext(filename)
    if file_extension != '.mp3' and file_extension != '.wav':
        # print("Skip: ", filename)
        continue

    # Record files not in CSV
    if not local_df['Filename'].astype(str).str.contains(filename).any():
        new_record = pd.DataFrame({'Filename': [filename], 'Status': ['New']})
        local_df = pd.concat([new_record, local_df], ignore_index=True)

# ===
# Parse ID3 tag
# ===
for index, row in tqdm(local_df.iterrows()):

    # Skip criteria
    if SKIP_ID3 == 1:
        continue

    if not pd.isna(row['Title']):
        continue

    # Get current ID3 tag
    title, artist, album, date, url= get_id3_tag(os.path.join(BASE_DIR, row['Filename']))

    if title:
        # Record ID3 Tag
        local_df.loc[index, 'Title'] = title
        local_df.loc[index, 'Artist'] = artist
        local_df.loc[index, 'Album'] = album
        local_df.loc[index, 'Date'] = date
        local_df.loc[index, 'YT_ID'] = url

    else:
        # Search for meta data
        file_name, _ = os.path.splitext(row['Filename'])
        title, album, date, artist = search_music_kkbox(file_name, access_token)
        yt_id, yt_title = search_music_youtube(file_name)

        local_df.loc[index, 'Title'] = title
        local_df.loc[index, 'Artist'] = artist
        local_df.loc[index, 'Album'] = album
        local_df.loc[index, 'Date'] = date
        local_df.loc[index, 'YT_ID'] = yt_id
        local_df.loc[index, 'YT_Title'] = yt_title

        # Record Status
        if pd.isna(row['Status']):
            local_df.loc[index, 'Status'] = 'Modified'

# ===
# Save Result
# ===
local_df.to_csv(os.path.join(BASE_DIR, 'data.csv'), index=False, encoding='utf_8_sig')
# local_df.to_excel(os.path.join(BASE_DIR, 'data.xlsx'), index=False)
