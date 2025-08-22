class Song:
    """
    "uri": elem["uri"],
    "cover_url": elem["album"]["images"][2]["url"],
    "name": elem["name"],
    "artist": _get_artists(elem["artists"]),
    "explicit": elem["explicit"],
    "duration": _format_time(elem["duration_ms"]),
    """
    def __init__(self, uri: str, cover_url: str, name: str, artist: str, duration: int):
        self.uri = uri
        self.cover_url = cover_url
        self.name = name
        self.artist = artist
        self.duration = duration
        self.votes = 0
        self.voted_for_next_song = False
    
    def add_vote(self):
        self.votes += 1
        return self.votes
    
    def set_votes(self, amount):
        self.votes = amount

vote_songs: list[Song] = [
    Song(uri="spotify:track:3A2AltRzjFIuGMCjac2kWe", cover_url="https://i.scdn.co/image/ab67616d00004851c32961ea5545854b259c2ab7", name="OKAY GARMIN VIDEO SPEICHERn BITTE", artist="Snake16", duration=46434),
]

vote_songs[0].set_votes(763)

def get_most_voted_song() -> Song:
    for item in vote_songs:
        if item.voted_for_next_song:
            vote_songs.remove(item)
    
    most_votes: Song = None
    most_votes_index: int = 0
    for count, item in enumerate(vote_songs):
        if not most_votes:
            most_votes = item
            most_votes_index = count
            continue
        if item.votes == most_votes.votes:
            if count < most_votes_index:
                most_votes = item
                most_votes_index = count
            continue
        elif item.votes > most_votes.votes:
            most_votes = item
            most_votes_index = count
    vote_songs[most_votes_index].voted_for_next_song = True
    return most_votes

def get_list_by_votes() -> list[Song]:
    list_by_votes = vote_songs
    n = len(list_by_votes)
    for i in range(n-1):
        for j in range(n-i-1):
            if list_by_votes[j].votes < list_by_votes[j+1].votes:
                list_by_votes[j], list_by_votes[j+1] = list_by_votes[j+1], list_by_votes[j]
    return list_by_votes

def append_song(uri: str, cover_url: str, name: str, artist: str, duration: str):
    vote_songs.append(Song(uri, cover_url, name, artist, duration))

if __name__ == "__main__":
    # Funktion testen
    vote_songs = [
        Song(uri="uri1", cover_url="cover1.jpg", name="Song A", artist="Artist 1", duration="3:45"),
        Song(uri="uri2", cover_url="cover2.jpg", name="Song B", artist="Artist 2", duration="4:20"),
        Song(uri="uri3", cover_url="cover3.jpg", name="Song C", artist="Artist 3", duration="2:50"),
        Song(uri="uri4", cover_url="cover4.jpg", name="Song D", artist="Artist 4", duration="3:30"),
        Song(uri="uri5", cover_url="cover5.jpg", name="Song E", artist="Artist 5", duration="5:00"),
    ]
    # Votes hinzufügen
    vote_songs[0].set_votes(5)  # Song A hat 5 Stimmen
    vote_songs[1].set_votes(3)  # Song B hat 3 Stimmen
    vote_songs[2].set_votes(5)  # Song C hat 5 Stimmen
    vote_songs[3].set_votes(2)  # Song D hat 2 Stimmen
    vote_songs[4].set_votes(4)  # Song E hat 4 Stimmen
    
    append_song("Aus rechtlichen Gründen runter genommen", "afd.nsdap", "Erika", "Hans H.", "18:88")
    vote_songs[5].set_votes(7)
    
    ss = get_list_by_votes(vote_songs)
    for luftwaffe in ss:
        print(f"{luftwaffe.name} by {luftwaffe.artist} with {luftwaffe.votes} votes.")
    """
    for i in range(6):
        most_voted_song = get_most_voted_song()
        print(f"Most voted song: {most_voted_song.name} by {most_voted_song.artist} with {most_voted_song.votes} votes.")
    """
