from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http.request import QueryDict
from pathlib import Path
from . import main
import requests
import base64
import json
from .models import Users
import datetime


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
    sp = main.Spotify()
    sp.get_access_token(request)
    song_list = sp.get_saves_track()
    return HttpResponse(f'Получени следубщий список треков: {song_list}')