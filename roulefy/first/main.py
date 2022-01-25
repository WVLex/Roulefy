import json
import requests
import random
import string
from . import config
from django.http.request import QueryDict
import base64


class Spotify:
    scope = config.scope
    client_id = config.client_id
    client_secret = config.client_secret
    redirect_uri = config.redirect_uri

    def __init__(self):
        self.access_token = None

    def redirect_to_authorization(self):
        redir_uri = 'https://accounts.spotify.com/authorize?' + \
                    "response_type=code&" \
                    f"client_id={self.client_id}&" \
                    f'scope={self.scope}&' \
                    f"redirect_uri={self.redirect_uri}&" \
                    f"state={''.join(random.choice(string.ascii_letters) for i in range(16))}"
        return redir_uri

    def get_access_token(self, request):
        current_url = request.get_full_path()
        raw_url = current_url.split('/')[2][3:]
        parse_url = QueryDict(raw_url)
        id_and_secret = text_to_base64(f'{self.client_id}:{self.client_secret}')

        headers = {'Authorization': f'Basic {id_and_secret}',
                   'Content-Type': 'application/x-www-form-urlencoded'}
        auth_data = {'grant_type': 'authorization_code',
                     'code': parse_url['code'],
                     'redirect_uri': self.redirect_uri}

        post_request = requests.post(url=f'https://accounts.spotify.com/api/token',
                                     headers=headers,
                                     data=auth_data)
        response_json = json.loads(post_request.text)
        self.access_token = response_json["access_token"]

    def get_saves_track(self):
        authorize_headers = {'Accept': 'application/json',
                             'Content-Type': 'application/json',
                             'Authorization': f'Bearer {self.access_token}'}

        get_saved_tracks = requests.get('https://api.spotify.com/v1/me/tracks?limit=30',
                                        headers=authorize_headers)
        json_data = json.loads(get_saved_tracks.text)
        song_list = {get_track_name(json_data, index):
                         {'album_id': get_album_id(json_data, index),
                          'track_number': get_track_number(json_data, index),
                          'artist': get_artist(json_data, index),            # Список!!!
                          'username': get_username(self.access_token),
                          'image_url': get_image_url(json_data, index)} for index, element
                     in enumerate(get_list_of_tracks(json_data))}
        # {'Polaroid': {'album_id': 1, 'track_number': 0, 'artist': 'leangey', 'username': 'Leha', 'image_url': 'http'}}
        return song_list



def text_to_base64(text):
    bytes_url_encoded = text.encode('ascii')
    base64_url_encoded = base64.b64encode(bytes_url_encoded)
    base64_url_decoded = base64_url_encoded.decode("ascii")
    return base64_url_decoded


def get_artist(json_data, global_index):
    return [json_data['items'][global_index]['track']['artists'][index]['name'] for index, element in
            enumerate(json_data['items'][global_index]['track']['artists'])]


def get_track_name(json_data, global_index):
    return json_data['items'][global_index]['track']['name']


def get_track_number(json_data, global_index):
    return json_data['items'][global_index]['track']['track_number'] - 1


def get_image_url(json_data, global_index):
    return json_data['items'][global_index]['track']['album']['images'][0]['url']


def get_album_id(json_data, global_index):
    return json_data['items'][global_index]['track']['album']['id']


def get_username(access_token):
    headers = {'Accept': 'application/json',
               'Content-Type': 'application/json',
               'Authorization': f'Bearer {access_token}'}
    str_json_data = requests.get('https://api.spotify.com/v1/me',
                                 headers=headers).text
    json_data = json.loads(str_json_data)
    return json_data['display_name']


def get_list_of_tracks(json_data):
    return json_data['items']
# result = sp.search('провинициал Заточка')
# album_id = result['tracks']['items'][0]['album']['id']
# track_number = result['tracks']['items'][0]['track_number'] - 1
