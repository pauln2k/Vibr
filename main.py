from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import pprint

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    req_url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization" : "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(req_url, headers=headers, data=data)
    json_return = json.loads(result.content)
    token = json_return["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization" : "Bearer " + token}

def create_query(token, tags):
    url = "https://api.spotify.com/v1/search"
    auth_header = get_auth_header(token)
    query = f"?q={tags}&type=track&limit=3"

    query_url = url + query
    query_result = get(query_url, headers=auth_header)
    json_result = json.loads(query_result.content)
    top_song_list = []

    for i in range(0,3):
        song_name = json_result['tracks']['items'][i]['name']
        song_url = json_result['tracks']['items'][i]['external_urls']
        song_id = json_result['tracks']['items'][i]['id']
    
        song_dict = {"name" : song_name,
                    "url"  : song_url,
                    "id"   : song_id}
        top_song_list.append(song_dict)

    
    return top_song_list

token = get_token()
tag = ""
song_dict = create_query(token, tag)
print(song_dict)
