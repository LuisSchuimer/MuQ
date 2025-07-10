import base64
import requests
from muq.config import CONFIG
from typing import Tuple
from json import loads
from datetime import datetime
from muq.backend.database import Database

# Error codes for returns in this format: dict[bool, int] (codes for int)
# Song already in queue: 100
# API error: 500
# Call okay: 200

client_id = CONFIG.CLIENT_ID
client_secret = CONFIG.CLIENT_SECRET
redirect_uri = "http://127.0.0.1:8000/callback"

auth_code: str = ""
auth_token: str = ""
refresh_token: str = ""

db = Database()

class res:
    def __init__(self, data: any = None, error: any = None, success: bool = True, fix: any = None):
        self.success = success
        self.data = data
        self.error = error
        self.fix = fix
    
    def __str__(self):
        if self.data: return f"{self.data}"
        else: return f"{self.error}"

    def fix_error(self):
        if self.fix: return self.fix()
        else: return None

time = datetime.now().replace(microsecond=0)
state = None # last state data
queue = None # last queue data
state_time = None # State time in ms
queue_time = None # qeue time in ms

def get_access_token_from_response(response: requests.Response):
    global auth_token, refresh_token
    if response.status_code == 200:
        auth_token = response.json().get("access_token")
        if not refresh_token: refresh_token = response.json().get("refresh_token")
        return True
    else:
        print("Failed to obtain access token:", response.text)
        return None
    
def response_handler(response: requests.Response):
    match response.status_code:
        case 200:
            return res(
                success=True,
                data=response,
                error=None
            )
        case 401:
            return res(
                success=False,
                data=response,
                error=401,
                fix=request_refreshed_access_token
            )
        case 429:
            return res(
                success=False,
                data=response,
                error=429,
            )
        case 403:
            return res(
                success=False,
                data=response,
                error=403
            )

    return res(
                success=False,
                data=None,
                error=None
            )

def _format_time(milliseconds: int, only_minutes: bool = False) -> str | int:
    """
    Convert milliseconds to 'M:SS' format, or return minutes if only_minutes=True.
    """
    total_sec = round(milliseconds / 1000)
    minutes = total_sec // 60
    seconds = total_sec % 60
    if only_minutes:
        return minutes
    return f"{minutes}:{seconds:02d}"

def _get_artists(data: any) -> str:
    artists = ""
    try:
        for elem in data:
            artists += f"{elem['name']}, "
    except Exception as e:
        print(f"Error processing artists: {e}")
    return artists.rstrip(", ")

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
    
def request_access_token(authorization_code: str) -> str | None:
    global auth_code, auth_token, refresh_token
    auth_code = authorization_code
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

    get_access_token_from_response(requests.post(url, data=payload, headers=headers))


def request_refreshed_access_token():
    url = "https://accounts.spotify.com/api/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    auth_string = f"{client_id}:{client_secret}"
    b64_auth_string = base64.b64encode(auth_string.encode()).decode()

    headers = {
        "Authorization": f"Basic {b64_auth_string}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    get_access_token_from_response(requests.post(url, data=payload, headers=headers))


def send_pause() -> Tuple[bool, str]:
    request_refreshed_access_token()
    url = "https://api.spotify.com/v1/me/player/pause"
    response = requests.put(url, headers={
        "Authorization": f"Bearer {auth_token}",
    })
    response = response_handler(requests.put(url, headers={
        "Authorization": f"Bearer {auth_token}",
    }))
    
    if not response.success and response.fix: 
        response.fix_error(); return False
    elif response.success: return True
    

def send_play() -> Tuple[bool, str]:
    url = "https://api.spotify.com/v1/me/player/play"
    response = response_handler(requests.put(url, headers={
        "Authorization": f"Bearer {auth_token}",
    }))

    if not response.success and response.fix: 
        response.fix_error(); return False
    elif response.success: return True

def get_state() -> list[dict] | None:
    global state_time, state
    current_time = datetime.now()
    if state_time is None or (current_time - state_time).total_seconds() >= 1:
        url = "https://api.spotify.com/v1/me/player"
        response = response_handler(requests.get(url, headers={
            "Authorization": f"Bearer {auth_token}",
            "market": "DE"
        }))
        if not response.success and response.fix: 
            response.fix_error(); return None
        elif not response.success: return None

        data = loads(response.data.text)
        try:
            state = {
                "uri": data["item"]["uri"],
                "state": data["is_playing"],
                "song_url": data["item"]["external_urls"]["spotify"],
                "song_name": data["item"]["name"],
                "artist": _get_artists(data["item"]["artists"]),
                "album": data["item"]["album"]["name"],
                "progress": _format_time(data["progress_ms"]),
                "duration": _format_time(data["item"]["duration_ms"]),
                "progress_ms": data["progress_ms"],
                "duration_ms": data["item"]["duration_ms"],
                "cover": data["item"]["album"]["images"][2]["url"],
            }
        except:
            return None
        state_time = current_time
    return state

def get_queue() -> list[dict]:
    global queue_time, queue
    current_time = datetime.now()
    if queue_time is None or (current_time - queue_time).total_seconds() >= 1:
        url = "https://api.spotify.com/v1/me/player/queue"
        response = response_handler(requests.get(url, headers={
            "Authorization": f"Bearer {auth_token}",
            "market": "DE"
        }))
        state_data = get_state()

        if not response.success and response.fix: 
            response.fix_error(); return queue
        elif not response.success or not state_data: return queue

        data = loads(response.data.text)
        new_queue = []
        ms_till_song = int(state_data["duration_ms"]) - int(state_data["progress_ms"])
        for count, elem in enumerate(data["queue"]):
            if count + 1 < 10: num_in_queue = f"0{count + 1}"
            else: num_in_queue = count + 1

            new_queue.append({
                "titel": elem["name"],
                "cover_url": elem["album"]["images"][2]["url"],
                "length": _format_time(elem["duration_ms"]),
                "artist": _get_artists(elem["artists"]),
                "num_in_queue": num_in_queue,
                "sp_url": elem["external_urls"]["spotify"],
                "sp_id": elem["uri"],
                "time_till_song": _format_time(ms_till_song),
                "user_ids": db.get_user_ids_by_track_id(elem["uri"]),
            })
            ms_till_song += elem["duration_ms"]

        queue = new_queue
        queue_time = current_time
    return queue

def search(title: str) -> list[dict]:
    url = f"https://api.spotify.com/v1/search?q={title}&type=track&market=DE&limit=10&offset=0"

    response = response_handler(requests.get(url, headers={
        "Authorization": f"Bearer {auth_token}",
    }))

    if not response.success and response.fix: 
            response.fix_error(); return None
    elif not response.success: return None
    
    data = loads(response.data.text)
    results = []
    for elem in data["tracks"]["items"]:
        results.append({
            "uri": elem["uri"],
            "cover_url": elem["album"]["images"][2]["url"],
            "name": elem["name"],
            "artist": _get_artists(elem["artists"]),
            "explicit": elem["explicit"],
            "duration": _format_time(elem["duration_ms"]),
        })


    return results

def add_to_queue(song_uri: str, user_id: str, song_name: str, song_artist: str, song_cover_url: str) -> Tuple[bool, int]:
    songs = db.get_songs_by_user_id(user_id)

    for song in songs:
        # Check if song was already added by the same user
        if song["track_id"] == song_uri and song["user_id"] == user_id and not song["already_played"]:
            # If yes, don't add anything
            return (True, 100)

    res = db.add_song(user_id, song_uri, song_name, song_artist, song_cover_url)

    for item in queue:
        if item["sp_id"] == song_uri: return (False, 100)

    url = f"https://api.spotify.com/v1/me/player/queue?uri={song_uri}"
    response = response_handler(requests.post(url, headers={
        "Authorization": f"Bearer {auth_token}"
    }))

    if response.success and res[0]: return (True, 200)

def get_songs_added_by_user(user_id: str) -> list[dict]:
    """
    Get all songs added by a user.
    """
    songs = db.get_songs_by_user_id(user_id)

    for song in songs:
        in_queue = False
        for item in queue:
            if song["track_id"] == item["sp_id"]: in_queue = True
        if not in_queue and not song["already_played"]: db.song_played(song["song_id"])

    return {
        "data": songs,
        "user_id": user_id
    }
