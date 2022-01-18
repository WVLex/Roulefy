import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import requests
import random
import string


# Необходимые scopes:
# user-modify-playback-state    Для Включение нового трека
# user-read-playback-state      Для поиска девайсов воспроизведения
# user-read-private
# user-read-email               Для проверки премиума
# user-library-read
# TODO: 1) Прописать формирование списка треков для Spotify
# TODO: 2) Создать БД для хранения списка треков от каждого пользователя. Таблица должна содержать поля
#       номер комнаты(АИ)/имя пользователя/список треков. Строки с конкрентым номером комнаты должны очищаться
#       после завершения игры.
# TODO: 3) Создать сайт, на котором будет запущена игра.


class Spotify():
    scope = "user-library-read user-modify-playback-state user-read-playback-state user-read-private user-read-email"
    client_id = 'e0bd4b6f4d9241ffbbdde4c43b1cfc3f'
    client_secret = 'dd8e66f89d184bc784c0e698a51c49a9'
    redirect_uri = 'http://localhost:8000/game/id'

    def redirect_to_authorization(self):
        redir_uri = 'https://accounts.spotify.com/authorize?' + \
                "response_type=code&" \
                f"client_id={self.client_id}&" \
                f'scope={self.scope}&' \
                f"redirect_uri={self.redirect_uri}&" \
                f"state={''.join(random.choice(string.ascii_letters) for i in range(16))}"
        return redir_uri

    def get_liked_songs(self):
        pass





# result = sp.search('провинициал Заточка')
# album_id = result['tracks']['items'][0]['album']['id']
# track_number = result['tracks']['items'][0]['track_number'] - 1



