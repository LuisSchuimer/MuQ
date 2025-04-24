"""
For easy running add this to the "pyprojects.toml" file:
    vote = "python3 -m muq.backend.voting_sys"
and then run:
    rye run vote
"""

class Song():
    def __init__(self, name: str, popularity: int):
        self.id: str = "spotify:track:uri"
        self.name: str = name
        self.popularity: int = popularity
        self.votes: int = 0
        self.score: int = 0
    
    def vote(self): self.votes += 1
    
    def set_votes(self, votes: int): self.votes = votes
    
    def set_score(self): self.score = self.votes * self.popularity
    
    def get_votes(self) -> int: return self.votes
    
    def __str__(self) -> str: return f"Song: {self.name}, Popularity: {self.popularity}, Votes: {self.votes}, Score: {self.score}"

def voting(voting_pool: list) -> Song:
    for song in voting_pool:
        song.set_score()
    voting_pool.sort(key=lambda x: x.score, reverse=True)
    return voting_pool[0]

# Example usage
song1 = Song("Song1", 50)
song2 = Song("Song2", 70)
song3 = Song("Song3", 90)

song1.set_votes(10)
song2.set_votes(7)
song3.set_votes(5)

voting_pool = [song1, song2, song3]

print(voting(voting_pool))
