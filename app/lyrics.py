import json
import os
from subprocess import PIPE, Popen

import requests
from dotenv import load_dotenv
from zhconv import convert

load_dotenv()

SG_BASE_URL="https://api.shangui.cc"

config = {
    "sg_key": os.getenv("SG_KEY"),
    "sg_base_url": SG_BASE_URL,
}

base_params = {"key": str(config["sg_key"]), "type": "kg", "format": 1}


def exec_applescript(script):
    p = Popen(["osascript", "-e", script], stdout=PIPE).communicate()
    return json.loads(p[0])


def get_spotify_now_playing():
    spotify_now_playing_applescript = """
tell application "System Events"
  set processList to (name of every process)
end tell
if (processList contains "Spotify") is true then
  tell application "Spotify"
    set artistName to artist of current track
    set trackName to name of current track
    set albumName to album of current track
    return "{" & "\\\"artist\\\": \\\"" & artistName & "\\\", " & "\\\"track\\\": \\\"" & trackName & "\\\", \\\"album\\\": \\\"" & albumName & "\\\"}"
  end tell
end if"""

    return exec_applescript(spotify_now_playing_applescript)


def request_sg_song_info(song_title, artist_name):
    sg_base_url = config["sg_base_url"]
    search_url = sg_base_url + "/api/music/search"
    data = dict(
        list(base_params.items())
        + [("name", song_title), ("type", "kg"), ("page", 1), ("limit", 10)]
    )
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(search_url, params=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print('Error [request_sg_song_info]: ')
        print(err)
        return None


def request_sg_song_lyrics(song_id):
    gs_base_url = config["sg_base_url"]
    lyrics_url = gs_base_url + "/api/music/lrc"
    data = dict(list(base_params.items()) + [("id", song_id)])
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(lyrics_url, params=data, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        print('Error [request_sg_song_lyrics]: ')
        print(err)
        return None


def get_lyrics_from_sg(song_title, artist_name):
    song_info = request_sg_song_info(convert(song_title, 'zh-cn'), artist_name)
    if not song_info:
        return None

    remote_song_info = None

    # print("song_info: " + json.dumps(song_info, indent=2, ensure_ascii=False))

    for hit in song_info["data"]:
        if convert(artist_name.lower(), "zh-cn") in hit["artist"].lower():
            remote_song_info = hit
            break

    if remote_song_info:
        song_id = remote_song_info["id"]
        response = request_sg_song_lyrics(song_id)
        if response is not None:
            lyrics = response.get("data", "").strip("\r\n")
            return lyrics


def print_spotify_now_playing_lyrics():
    info = get_spotify_now_playing()
    lyrics = get_lyrics_from_sg(info["track"], info["artist"])
    print()
    print(info["track"] + " by " + info["artist"] + " from album " + info["album"])
    print()
    print(lyrics)
    print()
