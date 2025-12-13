from dotenv import load_dotenv
import os
import base64
from requests import post
from requests import get
import json
import urllib

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"q={artist_name}&type=artist&limit=1"
    query_url = url + "?" + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists.")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def search_for_song(token, track, artist, year):
    q = f"track:{track} artist:{artist} year:{year}"
    q = urllib.parse.quote(q)
    url = f"https://api.spotify.com/v1/search?q={q}&type=track&market=US&limit=1&offset=0"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    if len(json_result) == 0:
        print("This song is not in the Spotify database.")
        return None
    return json_result

def get_song_features(token, id):
    url = f"https://api.spotify.com/v1/audio-features/{id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    if len(json_result) == 0:
        print("Audio features for this song are not available.")
        return None
    return json_result


token = get_token()
result = search_for_song(token, "Mr. Brightside", "The Killers", 2004)
id = result['tracks']['items'][0]['id']
result = get_song_features(token, id)
print(result)


