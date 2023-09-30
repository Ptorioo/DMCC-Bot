import requests
import io
from bs4 import BeautifulSoup

class Scraper():
    def __init__(self):
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}
        self.search_url = 'https://www.cprato.com/en/midi/search/'
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
