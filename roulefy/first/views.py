from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.http.request import QueryDict
from pathlib import Path
from . import main
import requests
import base64


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
    raw_data = current_url.split('/')[2][3:]
    id_and_secret = text_to_base64(f'{main.Spotify.client_id}:{main.Spotify.client_secret}')
    headers = {'Authorization': f'Basic {id_and_secret}'}
    auth_data = {'grant_type': 'authorization_code'}
    post_request = requests.post(url=f'https://accounts.spotify.com/api/token',
                                 headers=headers,
                                 data=auth_data)

    return HttpResponse(f'Authentication complete with code {post_request.status_code}\n{post_request.text}')





# Сторонние функции

def text_to_base64(text):
    bytes_url_encoded = text.encode('ascii')
    base64_url_encoded = base64.b64encode(bytes_url_encoded)
    base64_url_decoded = base64_url_encoded.decode("ascii")
    return base64_url_decoded
