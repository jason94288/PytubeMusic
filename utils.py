import re
import eyed3
import config
import requests
import urllib.parse
import urllib.request
# from moviepy.editor import *


def auth_process_kkbox():
    AUTH_URL = 'https://account.kkbox.com/oauth2/token'

    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': config.CLIENT_ID,
        'client_secret': config.CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    return auth_response_data['access_token']


def search_music_spotify(search_text, access_token):
    BASE_URL = 'https://api.spotify.com/v1/search?q='

    search_url = BASE_URL + urllib.parse.quote(search_text.encode('utf8')) + "&type=track&market=TW"
    search_response = requests.get(search_url, headers={"Authorization": f"Bearer {access_token}"})

    if search_response.status_code != 200:
        raise Exception('response error')

    search_response_data = search_response.json()
    try:
        item = search_response_data['tracks']['items'][0]
    except:
        return '', '', '', ['']

    release_date = item['album']['release_date']

    abumn_name = ''
    if(item['album']['album_type'] != 'single'):
        abumn_name = item['album']['name']

    artists = []
    for artist in item['artists']:
        artists.append(artist['name'])

    songname = item['name']

    return songname, abumn_name, release_date, artists


def search_music_kkbox(search_text, access_token):
    BASE_URL = 'https://api.kkbox.com/v1.1/search?q='

    search_url = BASE_URL + urllib.parse.quote(search_text.encode('utf8')) + "&type=track&territory=TW&limit=3"
    search_response = requests.get(search_url,headers={"Authorization": f"Bearer {access_token}"})

    if search_response.status_code != 200:
        # raise Exception('response error')
        return '', '', '', ['']

    search_response_data = search_response.json()
    try:
        item = search_response_data['tracks']['data'][0]
    except:
        return '', '', '', ['']

    release_date = item['album']['release_date']
    release_date = release_date[:4]

    abumn_name = ''
    abumn_name = item['album']['name']
    abumn_name = abumn_name.replace(",", ".")
    abumn_name = re.sub(r'\(.*\)', '', abumn_name)

    artist = ''
    artist = item['album']['artist']['name']
    artist = re.sub(r'\(.*', '', artist)
    artist = re.sub(r'\（.*', '', artist)
    artist = re.sub(r'\+.*', '', artist)
    artist = re.sub(r'\&.*', '', artist)
    artist = artist.strip()

    songname = item['name']
    songname = re.sub(r'\(.*', '', songname)
    songname = re.sub(r'\-.*', '', songname)
    songname = re.sub(r'Ft.*', '', songname)
    songname = re.sub(r'feat.*', '', songname)
    songname = songname.strip()

    return songname, abumn_name, release_date, artist


def search_music_youtube(search_text):

    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + urllib.parse.quote(search_text))
    yt_id = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    html = urllib.request.urlopen("https://www.youtube.com/watch?v=" + yt_id[0])
    yt_title = re.findall(r"<title>(.*?)</title>", html.read().decode())
    yt_title = re.sub(r'- YouTube', '', yt_title[0])
    yt_title = yt_title.strip()

    return yt_id[0], yt_title


def get_id3_tag(file_path):
    title = ''
    artist = ''
    album = ''
    date = ''
    url = ''

    try:
        audiofile = eyed3.load(file_path)
    except:
        pass
    try:
        title = audiofile.tag.title
    except:
        pass
    try:
        artist = audiofile.tag.artist
    except:
        pass
    try:
        album = audiofile.tag.album
    except:
        pass
    try:
        date = audiofile.tag.date
    except:
        pass
    try:
        url = audiofile.tag.publisher
    except:
        pass

    return title, artist, album, date, url

# def MP4ToMP3(mp4, mp3):
#     FILETOCONVERT = AudioFileClip(mp4)
#     FILETOCONVERT.write_audiofile(mp3)
#     FILETOCONVERT.close()