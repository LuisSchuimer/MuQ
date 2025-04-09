import requests
from bs4 import BeautifulSoup
import re

def fetch_lyrics(artist_name: str, song_name: str):
    try:
        song_name = re.sub(r'[\W_]+', '', song_name).lower()
        artist_name = re.sub(r'[\W_]+', '', artist_name).lower()
        url = "https://www.azlyrics.com/lyrics/{aname}/{sname}.html".format(aname=artist_name, sname=song_name)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'lxml')
        lyrics = soup.find("div", class_="col-xs-12 col-lg-8 text-center").find_next("div", class_=None).text

        try:
            lyrics = lyrics.strip().replace("\n", " ")
            return {"lyrics": lyrics}
        except Exception as e:
            print(e)
            return {"Error": "Not found"}
        
    except Exception as e:
        print(e)
        return {"Error": e}
    
if __name__ == "__main__":
    print(fetch_lyrics("Ed Sheeran", "Perfect"))