import requests
from bs4 import BeautifulSoup
import re

current_song: tuple = {"song_name": "", "artist_name": ""}
last_result: dict = ""

def fetch_lyrics(artist_name: str, song_name: str):
    global current_lyrics, current_song
    # Clean up song and artist names
    song_name = re.sub(r'[\W_]+', '', song_name).lower()
    artist_name = re.sub(r'[\W_]+', '', artist_name).lower()

    #! Reimplement
    if current_song["song_name"] == song_name and current_song["artist_name"] == artist_name: 
        return last_result
    else: 
        current_song["song_name"] = song_name
        current_song["artist_name"] = artist_name


    # Try the full song name first
    def try_fetch_lyrics(song_name):
        try:
            url = f"https://www.azlyrics.com/lyrics/{artist_name}/{song_name}.html"
            res = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36"
            })
            if res.status_code == 200:
                soup = BeautifulSoup(res.content, 'lxml')
                lyrics = soup.find("div", class_="col-xs-12 col-lg-8 text-center").find_next("div", class_=None).text
                # Replace newlines with <br> tags to maintain line breaks on frontend
                formatted_lyrics = lyrics.replace("\n", "<br>")
                return {"lyrics": formatted_lyrics}
        except: pass
        return None
    try:
        res = try_fetch_lyrics(song_name)
        if res: return res
    except: pass

    # Try with progressively shorter versions of the song name
    for i in range(1, len(song_name) + 1):
        # Substring from the start to the i-th character
        alt_song_name = song_name[:i]
        result = try_fetch_lyrics(alt_song_name)
        if result:
            current_song = song_name
            current_lyrics = result
            return result  # If lyrics are found, return them immediately

    # If no lyrics found after trying all combinations, return an error
    return {"Error": "Not found after trying all variations"}

if __name__ == "__main__":
    # Example call
    print(fetch_lyrics("Danzig", "Mother"))