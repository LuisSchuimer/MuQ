from flask import (
    Flask,
    render_template,
    request,
    Response,
    jsonify
)
from json import dumps
from muq.backend.main import *
from http import HTTPStatus
from dotenv import dotenv_values
from muq.backend.song_validation import fetch_lyrics

auth_code: str = ""
auth_link = authenticate()
env = dotenv_values()

print(f"You need to authenticate your Spotify: {auth_link}")

SERVER_PASS = env.get("SERVER_PASS")

app = Flask(__name__)


@app.route("/", methods=["GET"])
def main():
    return render_template("index.html")

@app.route("/pause", methods=["POST"])
def pause():
    response = send_pause(auth_code)
    if response[0]: return "", HTTPStatus.OK
    else: return "", HTTPStatus.BAD_REQUEST

@app.route("/play", methods=["POST"])
def play():
    response = send_play(auth_code)
    if response[0]: return "", HTTPStatus.OK
    else: return "", HTTPStatus.BAD_REQUEST

@app.route("/test")
def test():
    res = get_queue(auth_code)
    return res, HTTPStatus.OK

@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html", current_state=get_state(auth_code))

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

@app.route('/state/listen', methods=['GET'])
def listen():
    def stream():
        last_send_data: str = ""
        while True:
            new_data = dumps({
                "state_data": get_state(auth_code),
                "queue_data": get_queue(auth_code)
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

@app.route("/callback")
def auth_callback():
    global auth_code
    auth_code = get_access_token(request.args.get("code"))
    return "", HTTPStatus.OK



if __name__ == "__main__":
    app.run("0.0.0.0", 8000)