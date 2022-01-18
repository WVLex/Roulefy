from bs4 import BeautifulSoup
import requests


class Parser:

    song_list = {}

    def yandex_music(self, url):
        # url = 'https://music.yandex.com/users/leha333000/playlists/3'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'templates.parser')
        raw_list = soup.find_all('div', 'd-track__overflowable-wrapper deco-typo-secondary block-layout')
        for index, i in enumerate(raw_list):
            song = raw_list[index].contents[1].text.strip()
            artist = raw_list[index].contents[2].text
            self.song_list[song] = artist
        return self.song_list



# user1 = Parser()
# user1.yandex_music('https://music.yandex.com/users/leha333000/playlists/3')
pass
