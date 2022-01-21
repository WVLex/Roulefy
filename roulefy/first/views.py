from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.http.request import QueryDict
from pathlib import Path
from . import main
import requests
import base64
import json


# Главная страница
def index(request):
    template = Path.cwd() / 'templates' / 'index.html'
    return render(request, template)


def create(request):
    template = Path.cwd() / 'templates' / 'create.html'
    return render(request, template)


def join(request):
    template = Path.cwd() / 'templates' / 'join.html'
    return render(request, template)


def login(request):
    sp = main.Spotify()
    redir = sp.redirect_to_authorization()
    return redirect(redir)


def id(request):
    current_url = request.get_full_path()
    raw_url = current_url.split('/')[2][3:]
    parse_url = QueryDict(raw_url)
    id_and_secret = text_to_base64(f'{main.Spotify.client_id}:{main.Spotify.client_secret}')
    headers = {'Authorization': f'Basic {id_and_secret}',
               'Content-Type': 'application/x-www-form-urlencoded'}
    auth_data = {'grant_type': 'authorization_code',
                 'code': parse_url['code'],
                 'redirect_uri': main.Spotify.redirect_uri}
    post_request = requests.post(url=f'https://accounts.spotify.com/api/token',
                                 headers=headers,
                                 data=auth_data)
    response_json = json.loads(post_request.text)

    authorize_headers = {'Accept': 'application/json',
                         'Content-Type': 'application/json'}
    authorize_data = {'Authorization': f'Bearer {response_json["access_token"]}'}
    get_saved_tracks = requests.get('https://api.spotify.com/v1/me/tracks?limit=30',
                                    headers=authorize_headers,
                                    data=authorize_data)
    response_with_songs = json.loads(get_saved_tracks.text)

    return HttpResponse(f'Authentication complete with code {post_request.status_code}\n{post_request.text}')


# Сторонние функции


def text_to_base64(text):
    bytes_url_encoded = text.encode('ascii')
    base64_url_encoded = base64.b64encode(bytes_url_encoded)
    base64_url_decoded = base64_url_encoded.decode("ascii")
    return base64_url_decoded


def get_artist(json_data, global_index):
    return [json_data['items'][global_index]['track']['artists'][index]['name'] for index, element in
               enumerate(json_data['items'][2]['track']['artists'])]


def get_track_name(json_data, global_index):
    return json_data['items'][global_index]['track']['name']


def get_track_number(json_data, global_index):
    return json_data['items'][global_index]['track']['track_number'] - 1


def get_image_url(json_data, global_index):
    return json_data['items'][global_index]['track']['album']['images'][0]['url']