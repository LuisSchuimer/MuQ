from flask import (
    Flask,
    render_template,
    request,
    Response,
    jsonify,
    make_response
)
from json import dumps
from muq.config import CONFIG
from muq.backend.main import *
from http import HTTPStatus
from muq.backend.song_validation import fetch_lyrics
from uuid import uuid4

auth_link = authenticate()
voting_enabled = CONFIG.ENABLE_VOTING

print(f"You need to authenticate your Spotify: {auth_link}")

SERVER_PASS = CONFIG.SERVER_PASS

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    user_id = request.cookies.get("user_id")
    if user_id is None:
        user_id = str(uuid4())
        response = make_response(render_template("index.html"))
        response.set_cookie("user_id", user_id, max_age=60 * 60 * 24 * 30)
        return response
    return render_template("index.html")

@app.route("/pause", methods=["POST"])
def pause():
    response = send_pause()
    if response[0]: return "", HTTPStatus.OK
    else: return "", HTTPStatus.BAD_REQUEST

@app.route("/play", methods=["POST"])
def play():
    response = send_play()
    if response[0]: return "", HTTPStatus.OK
    else: return "", HTTPStatus.BAD_REQUEST

@app.route("/test")
def test():
    res = get_queue()
    return res, HTTPStatus.OK

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html", current_state=get_state())

@app.route("/search")
def make_search():
    query = request.args.get("query")
    return render_template(
        "components/song_card.html",
        results=search(query)
    )

@app.route("/add/queue", methods=["POST"])
def add_song_to_queue():
    user_id = request.cookies.get("user_id")
    if not user_id:
        return "", HTTPStatus.UNAUTHORIZED
    song_uri = request.args.get("song_uri")
    song_name = request.args.get("song_name")
    song_artist = request.args.get("song_artist")
    song_cover_url = request.args.get("song_cover")
    
    if not song_uri or not song_name or not song_artist or not song_cover_url:
        return "", HTTPStatus.BAD_REQUEST
    res = add_to_queue(song_uri, user_id, song_name, song_artist, song_cover_url)
    if res[0]: return "", HTTPStatus.OK
    else: return "", HTTPStatus.CONFLICT

def _format_sse(data, event=None) -> str:
    """
    Formats data as a valid SSE message with properly serialized JSON.
    """
    if isinstance(data, dict):
        data = dumps(data)  # Serialize to proper JSON format
    elif not isinstance(data, str):
        raise ValueError("Data must be a dictionary or string")

    msg = f'data: {data}\n\n'
    if event is not None:
        msg = f'event: {event}\n{msg}'
    return msg

@app.route('/data/listen', methods=['GET'])
def listen():
    def stream():
        last_send_data: str = ""
        while True:
            state_data = get_state()
            if voting_enabled: queue_data = get_voting_list()
            else: queue_data = get_queue()
            
            if not state_data: continue
            new_data = dumps({
                "voting_enabled": voting_enabled,
                "state_data": state_data,
                "queue_data": queue_data
            })
            if new_data != last_send_data:
                last_send_data = new_data; yield _format_sse(new_data)
    
    return Response(stream(), mimetype='text/event-stream')

@app.route("/lyrics", methods=["GET"])
def lyrics():
    artist = request.args.get("artist")
    song_name = request.args.get("songName")
    if artist and song_name:
        fetched_lyrics = fetch_lyrics(artist_name=artist, song_name=song_name)
        return jsonify(fetched_lyrics), HTTPStatus.OK
    else:
        return jsonify({"error": "Artist or song name missing"}), HTTPStatus.BAD_REQUEST
    
@app.route("/data/get_added")
def get_added():
    user_id = request.cookies.get("user_id")
    if not user_id:
        return "", HTTPStatus.UNAUTHORIZED
    return jsonify(get_songs_added_by_user(user_id)), HTTPStatus.OK

@app.route("/callback")
def auth_callback():
    request_access_token(request.args.get("code"))
    return "", HTTPStatus.OK



if __name__ == "__main__":
    app.run("0.0.0.0", 8000)