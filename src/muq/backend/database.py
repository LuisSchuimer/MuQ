from peewee import (
    Model,
    TextField,
    SqliteDatabase,
    BooleanField
)
from uuid import uuid4

db = SqliteDatabase("songs.db")

class song(Model):
    """
    Model for the song table in the database.
    """
    song_id = TextField(primary_key=True)
    song_name = TextField()
    song_artist = TextField()
    song_cover_url = TextField()
    track_id = TextField()
    user_id = TextField()
    already_played = BooleanField()

    class Meta:
        database = db


class Database:
    def __init__(self):
        self.db = db

        self.db.connect()
        self.db.create_tables([song])
    
    def add_song(self, user_id: str, track_id: str, song_name: str, song_artist: str, song_cover_url: str) -> None:
        """
        Add a song to the queue.
        """
        return (True, song.create(
            song_id=str(uuid4()),
            user_id=user_id,
            track_id=track_id,
            already_played=False,
            song_name=song_name,
            song_artist=song_artist,
            song_cover_url=song_cover_url
        ))

    def get_songs_by_user_id(self, user_id: str) -> list[dict[str, str]]:
        """
        Get all songs by user id.
        """
        # return songs sorted by timestamp descending (newest first)
        songs = (song.select().where(song.user_id == user_id))
        return [
            {
                "song_id": item.song_id,
                "already_played": item.already_played,
                "user_id": item.user_id,
                "track_id": item.track_id,
                "song_name": item.song_name,
                "song_artist": item.song_artist,
                "song_cover_url": item.song_cover_url
            }
            for item in songs
        ]
    
    def get_user_ids_by_track_id(self, track_id: str) -> dict[str, str]:
        """
        Get all user ids by track id.
        """
        # return songs sorted by timestamp descending (newest first)
        songs = (song.select().where(song.track_id == track_id))
        user_ids = [item.user_id for item in songs]
        return user_ids
    
    def delete_song(self, song_id: str) -> bool:
        try:
            song.delete().where(song.song_id == song_id).execute()
            return True
        except song.DoesNotExist: return False
    
    def song_played(self, song_id: str) -> bool:
        """
        Mark the song with given song_id as already played.
        Returns True if the update affected a row, False otherwise.
        """
        try:
            updated = song.update(already_played=True) \
                        .where(song.song_id == song_id) \
                        .execute()
            return bool(updated)
        except Exception as e:
            print(f"Error marking song as played: {e}")
            return False

    def song_exists(self, track_id: str) -> bool:
        """
        Check if a song exists in the queue.
        """
        try:
            song.get(song.track_id == track_id)
            return True
        except song.DoesNotExist:
            return False
