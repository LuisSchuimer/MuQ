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

print(client_id)
print(client_secret)

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

def get_access_token(authorization_code) -> str | None:
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

def send_pause(auth_code) -> Tuple[bool, str]:
    url = "https://api.spotify.com/v1/me/player/pause"
    response = requests.put(url, headers={
        "Authorization": f"Bearer {auth_code}",
    })
    if response.status_code == 200: 
        return (True, "")
    elif response.status_code == 403:
        return (False, "No active playback device")

def send_play(auth_code) -> Tuple[bool, str]:
    url = "https://api.spotify.com/v1/me/player/play"
    response = requests.put(url, headers={ 
        "Authorization": f"Bearer {auth_code}",
    })
    if response.status_code == 200: 
        return (True, "")
    elif response.status_code == 403:
        return (False, "Already playing")

def get_state(auth_code):
    global time, state
    if time != datetime.now().replace(microsecond=0):
        url = "https://api.spotify.com/v1/me/player"
        response = requests.get(url, headers={
            "Authorization": f"Bearer {auth_code}",
            "market": "DE"
        })
        try:
            data = loads(response.text)
            #print(response.text)
            state = {
                "state": data["is_playing"],
                "song_url": data["item"]["external_urls"]["spotify"],
                "song_name": data["item"]["name"], 
                "artist": data["item"]["artists"][0]["name"], 
                "album": data["item"]["album"]["name"],
                "progress": data["progress_ms"], 
                "duration": data["item"]["duration_ms"],
                "cover": data["item"]["album"]["images"][2]["url"],
            }
        except: return {"state": None}
    
    time = datetime.now().replace(microsecond=0)
    return state

def send_queue(auth_code, track_id) -> Tuple[bool, str]:
    url = "https://api.spotify.com/v1/me/player/queue"
    payload = {
        "uris": track_id
    }
    response = requests.post(url, json=payload, headers={
        "Authorization": f"Bearer {auth_code}",
    })
    if response.status_code == 204: 
        return (True, "")
    elif response.status_code == 403:
        return (False, "No active playback device")

