from flask import (
    Flask,
    render_template,
    request, 
    redirect
)
from muq.backend.main import *
from http import HTTPStatus

auth_code: str = ""

print(f"You need to authenticate your Spotify: {authenticate()}")

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("index.html")

@app.route("/pause")
def pause():
    response = send_pause(auth_code)
    if response[0]: 
        return redirect("/", 304)
    else: 
        return response[1], HTTPStatus.OK

@app.route("/play")
def play():
    response = send_play(auth_code)
    if response[0]: 
        return redirect("/", 304)
    else: 
        return response[1], HTTPStatus.OK

@app.route("/callback")
def auth_callback():
    global auth_code
    auth_code = get_access_token(request.args.get("code"))
    return "", HTTPStatus.OK



if __name__ == "__main__":
    app.run("0.0.0.0", 8000)