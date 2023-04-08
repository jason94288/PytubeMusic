# Youtube Playlist Downloader
Use pytube to download videos from youtube playlists to mp3

**Warrnings**

This project is for educational use only.
Downloading YouTube videos without permission is a violation of YouTube's terms of service and could result in account termination or legal action.

## Built with

### Meta-data sources
- [KKBOX](https://docs-zhtw.kkbox.codes/)
- [Spotify](https://developer.spotify.com/documentation/web-api)

### Enviroments
- [Pytube](https://pytube.io/en/latest/): Python tools for download music from youtube
- [eyeD3](https://eyed3.readthedocs.io/en/latest/):  Python tool for working with audio files, specifically MP3 files containing ID3 metadata

## Usage
1. Prase local files
    ```shell
    python ./check_local.py
    ```
1. Upload output file (`data.csv`) to colab
1. Compare local files with youtube playlist (Run on colab)
    1. Download yputube playlist informations (Section `Download from YT playlist` from `Pytube.ipynb`)

## How It Works

### Program Processing Workflow
- Parse local file (`check_local.py`)
    - Check status
        - Record files not in local csv
        - Find lost files (Have record but no file)
        - Check Dulplicate
    - Parse ID3 tags & YT ID
        - Fill empty fields
        - Fill empty ID
    - Normalize file

- Download YT (`Pytube.ipynb`)
    - Check dulplicate YT ID
    - Render Download list (INPUT)
        - Get meta-data, YT-titile, YT-ID
        - Human verify
    - Download

### Standardized Filename Formats
- Filename
    - `Artist-Songname(Remark).extension`
- ID3 Tag
    - Artist
        - `Artist1`
        - `Artist1; Artist2; ...` (not available)
    - Title
        - `Songname (Remark)`

### DB columns
- Status:  Missing, Local (Pass for YT-ID), Modified (Add information)
- Filename
- YT_Title
- YT_ID
- Title
- Artists
- Albumn
- Date
- Remark

## Code informations
- Main Files
    - `check_local.py`: prasng local files to csv
    - `utils.py`: Utils for all files
    - `config.py`: Files to record API credentials
- Other tools
    - `eyeD3_norm.py`: prototype for `check_local.py` (can be removed)
    - `music_content.py`: prototype for `pytube.ipynb` (can be removed)
    - `Rename_file.py`: rename mp3 files base on ID3 tag
    - `spotify_normalize.py`: volumn normalize protype
        - rename needed

## To-Do
- volumn normolization
- write a android GUI for process local files
- a backend downloader is needed
- human verufying process still needed