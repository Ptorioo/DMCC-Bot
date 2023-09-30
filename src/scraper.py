from config import *
import requests
import io
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
        self.search_url = 'https://www.cprato.com/en/midi/search/'
        self.GENIUS_API_BASE_URL = "https://api.genius.com"
        self.result = []

    async def scrapeInfo(self, ctx, query):        
        self.result = []
        self.search_url += query
        await ctx.send('Sending request...')
        response = requests.get(self.search_url, headers = self.headers)

        if response.status_code == 200:
            await ctx.send('Successfully fetched website...')
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.find('div', class_='col-md-4 rounded mt-4'):
                for com in soup.find_all('td'):
                    if com.find('img'):
                        self.result.append(com.find('img').get('src'))
                    else:
                        self.result.append(com.text.strip())
            else:
                self.result.append(0)
            return self.result
        else:
            await ctx.send('Failed to fetch website...')
            self.result.append(response.status_code)
            return self.result
    
    async def scrapeMIDI(self, ctx, query):
        self.result = []
        self.search_url += query
        await ctx.send('Sending request...')
        response = requests.get(self.search_url, headers = self.headers)

        if response.status_code == 200:
            await ctx.send(f'Successfully fetched website...')
            soup = BeautifulSoup(response.content, 'html.parser')
            if soup.find('div', class_='col-md-4 rounded mt-4'):
                for com in soup.find_all('td'):
                    if com.find('a', class_='btn btn-success px-3 py-3'):
                        self.result.append(com.find('a').get('href'))
                    else:
                        self.result.append(com.text.strip())
            else:
                self.result.append(0)
                return self.result

        else:
            await ctx.send('Failed to fetch website...')
            self.result.append(response.status_code)
            return self.result
        
        download_url = 'https://www.cprato.com' + self.result[2]
        download_url = download_url.replace("/download/", "/file/")
        response_file = requests.get(download_url, stream=True)

        buffer = io.BytesIO()
        buffer.write(response_file.content)
        buffer.seek(0)

        self.result.append(buffer)
        return self.result
    
    async def scrapeLyrics(self, ctx, query):
        self.result = []
        headers = {
            "Authorization": f"Bearer {GENIUS_ACCESS_TOKEN}"
        }

        await ctx.send('Sending request...')
        response = requests.get(f"{self.GENIUS_API_BASE_URL}/search?q={query}", headers=headers)

        if response.status_code == 200:
            
            response.raise_for_status()
            data = response.json()
            
            try:
                song = data["response"]["hits"][0]["result"]
                lyrics_url = song['url']
                artist = song['artist_names']
                title = song['title']
                img = song['song_art_image_thumbnail_url']

                self.result.extend([artist, title, img])

                lyrics_page = requests.get(lyrics_url)

                if lyrics_page.status_code == 200:
                    await ctx.send(f'Successfully fetched website...')
                    lyrics_page.raise_for_status()
                    soup = BeautifulSoup(lyrics_page.text, 'html.parser')

                    for br in soup.find_all("br"):
                        br.replace_with("\n")
                
                    for com in soup.find_all(True, {'class':['ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw', 'Lyrics__Container-sc-1ynbvzw-1 kUgSbL']}):
                        self.result.append(com.text.strip())
            
                else:
                    await ctx.send('Failed to fetch website...')
                    self.result.append(lyrics_page.status_code)
                    return self.result
            except:
                await ctx.send('Failed to find search result...')
                self.result.append(0)
            return self.result
        
        else:
            await ctx.send('Failed to fetch website...')
            self.result.append(response.status_code)
            return self.result

