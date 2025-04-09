import base64
import requests
from dotenv import dotenv_values
from typing import Tuple

env = dotenv_values()

client_id = env.get("CLIENT_ID")
client_secret = env.get("CLIENT_SECRET")
redirect_uri = "http://localhost:8000/callback"

print(client_id)
print(client_secret)

def authenticate() -> str:
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": "user-modify-playback-state",
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
