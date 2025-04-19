import base64
import requests
from muq.config import CONFIG
from typing import Tuple
from json import loads
from datetime import datetime

client_id = CONFIG.CLIENT_ID
client_secret = CONFIG.CLIENT_SECRET
redirect_uri = "http://localhost:8000/callback"

time = datetime.now().replace(microsecond=0)
state = None
queue = None
state_time = None
queue_time = None

print(client_id)
print(client_secret)

def format_time(milliseconds: int, only_minutes: bool = False) -> str | int:
    """
    Convert milliseconds to 'M:SS' format, or return minutes if only_minutes=True.
    """
    total_sec = round(milliseconds / 1000)
    minutes = total_sec // 60
    seconds = total_sec % 60
    if only_minutes:
        return minutes
    return f"{minutes}:{seconds:02d}"

def authenticate() -> str:
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-modify-playback-state user-read-playback-state",
    }
    base_url = "https://accounts.spotify.com/authorize?"
    # Construct the URL with query parameters
    authorization_url = requests.Request("GET", base_url, params=params).prepare().url

    return authorization_url

def get_access_token(authorization_code: str) -> str | None:
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri
    }
    auth_string = f"{client_id}:{client_secret}"
    b64_auth_string = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_string}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=payload, headers=headers)

    if response.status_code == 200:
        token = response.json().get("access_token")
        return token
    else:
        print("Failed to obtain access token:", response.text)
        return None

def send_pause(auth_code: str) -> Tuple[bool, str]:
    url = "https://api.spotify.com/v1/me/player/pause"
    response = requests.put(url, headers={
        "Authorization": f"Bearer {auth_code}",
    })
    if response.status_code == 200:
        return (True, "")
    elif response.status_code == 403:
        return (False, "No active playback device")

def send_play(auth_code: str) -> Tuple[bool, str]:
    url = "https://api.spotify.com/v1/me/player/play"
    response = requests.put(url, headers={
        "Authorization": f"Bearer {auth_code}",
    })
    if response.status_code == 200:
        return (True, "")
    elif response.status_code == 403:
        return (False, "Already playing")

def get_state(auth_code: str) -> list[dict]:
    global state_time, state
    current_time = datetime.now()
    if state_time is None or (current_time - state_time).total_seconds() >= 1:
        url = "https://api.spotify.com/v1/me/player"
        response = requests.get(url, headers={
            "Authorization": f"Bearer {auth_code}",
            "market": "DE"
        })
        try:
            data = loads(response.text)
            state = {
                "state": data["is_playing"],
                "song_url": data["item"]["external_urls"]["spotify"],
                "song_name": data["item"]["name"],
                "artist": get_artists(data["item"]["artists"]),
                "album": data["item"]["album"]["name"],
                "progress": format_time(data["progress_ms"]),
                "duration": format_time(data["item"]["duration_ms"]),
                "progress_ms": data["progress_ms"],
                "duration_ms": data["item"]["duration_ms"],
                "cover": data["item"]["album"]["images"][2]["url"],
            }
        except Exception as err:
            print(err)
            return {"state": None}
        state_time = current_time
    return state

def get_queue(auth_code: str) -> list[dict]:
    state_data = get_state(auth_code)
    current_time_till_next = int(state_data["duration_ms"]) - int(state_data["progress_ms"])
    global queue_time, queue
    current_time = datetime.now()
    if queue_time is None or (current_time - queue_time).total_seconds() >= 1:
        url = "https://api.spotify.com/v1/me/player/queue"
        response = requests.get(url, headers={
            "Authorization": f"Bearer {auth_code}",
            "market": "DE"
        })
        try:
            data = loads(response.text)
            new_queue = []
            ms_till_song = current_time_till_next
            for count, elem in enumerate(data["queue"]):
                if count + 1 < 10: num_in_queue = f"0{count + 1}"
                else: num_in_queue = count + 1
                new_queue.append({
                    "titel": elem["name"],
                    "cover_url": elem["album"]["images"][2]["url"],
                    "length": format_time(elem["duration_ms"]),
                    "artist": get_artists(elem["artists"]),
                    "num_in_queue": num_in_queue,
                    "sp_url": elem["external_urls"]["spotify"],
                    "sp_id": elem["uri"],
                    "time_till_song": format_time(ms_till_song)
                })
                ms_till_song += elem["duration_ms"]
            queue = new_queue
        except Exception as err:
            print(err)
            return queue
        queue_time = current_time
    return queue

def get_artists(data: any) -> str:
    artists = ""
    try:
        for elem in data:
            artists += f"{elem['name']}, "
    except Exception as e:
        print(f"Error processing artists: {e}")
    return artists.rstrip(", ")

def search(auth_code: str, title: str) -> list[dict]:
    url = f"https://api.spotify.com/v1/search?q={title}&type=track&market=DE&limit=10&offset=0"

    response = requests.get(url, headers={
        "Authorization": f"Bearer {auth_code}",
    })
    try:
        data = loads(response.text)
        results = []
        for elem in data["tracks"]["items"]:
            results.append({
                "uri": elem["uri"],
                "cover_url": elem["album"]["images"][2]["url"],
                "name": elem["name"],
                "artist": get_artists(elem["artists"]),
                "explicit": elem["explicit"],
                "duration": format_time(elem["duration_ms"]),
            })
    except Exception as err:
        print(err)

    return results

def add_to_queue(auth_code: str, song_uri: str) -> Tuple[bool, str]:
    url = f"https://api.spotify.com/v1/me/player/queue?uri={song_uri}"
    response = requests.post(url, headers={
        "Authorization": f"Bearer {auth_code}"
    })
    if response.status_code == 200:
        return (True, "")     
