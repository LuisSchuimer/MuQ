import json

with open("src/muq/songs/test.json", "r") as f:
    data = json.load(f)

track_uri = data["is_playing"]
print(track_uri)
