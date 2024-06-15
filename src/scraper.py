from config import *
import io
import spotipy
import requests
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyClientCredentials


class Scraper:
    def __init__(self):
        self.midi_url = "https://www.cprato.com/en/midi/search/"
        self.GENIUS_API_BASE_URL = "https://api.genius.com"
        self.result = []
        self.keyLst = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
        self.mode = ["Minor", "Major"]

    async def scrapeInfo(self, ctx, query):
        self.result = []
        client_credentials_manager = SpotifyClientCredentials(
            client_id=SPOTIFY_ID, client_secret=SPOTIFY_TOKEN
        )
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        await ctx.send("Sending request...")
        track_info = sp.search(q=query, type="track")

        if track_info:
            await ctx.send("Successfully fetched result...")
            track = track_info["tracks"]["items"][0]
            audio_features = sp.audio_features([track["id"]])
            track_details = sp.track(track["id"])
            album_details = sp.album(track_details["album"]["id"])

            artist_name = ", ".join([artist["name"] for artist in track["artists"]])
            song_name = track["name"]
            cover_art_url = album_details["images"][0]["url"]

            key = (
                self.keyLst[audio_features[0]["key"]]
                + " "
                + self.mode[audio_features[0]["mode"]]
            )
            bpm = round(audio_features[0]["tempo"])
            m, s = divmod(round(audio_features[0]["duration_ms"] / 1000), 60)
            duration = f"{m}:{s:0>2d}"
            loudness = str(round(audio_features[0]["loudness"] * 10) / 10) + " dB"

            self.result.extend(
                [
                    artist_name,
                    song_name,
                    cover_art_url,
                    key,
                    bpm,
                    duration,
                    loudness
                ]
            )
            return self.result

        else:
            await ctx.send("No search results...")
            self.result.append(0)
            return self.result

    async def scrapeMIDI(self, ctx, query):
        self.result = []
        self.midi_url += query
        await ctx.send("Sending request...")
        response = requests.get(self.midi_url)

        if response.status_code == 200:
            await ctx.send(f"Successfully fetched website...")
            soup = BeautifulSoup(response.content, "html.parser")
            if soup.find("div", class_="col-md-4 rounded mt-4"):
                for com in soup.find_all("td"):
                    if com.find("a", class_="btn btn-success px-3 py-3"):
                        self.result.append(com.find("a").get("href"))
                    else:
                        self.result.append(com.text.strip())
            else:
                self.result.append(0)
                return self.result

        else:
            await ctx.send("Failed to fetch website...")
            self.result.append(response.status_code)
            return self.result

        download_url = "https://www.cprato.com" + self.result[2]
        download_url = download_url.replace("/download/", "/file/")
        response_file = requests.get(download_url, stream=True)

        buffer = io.BytesIO()
        buffer.write(response_file.content)
        buffer.seek(0)

        self.result.append(buffer)
        return self.result

    async def scrapeLyrics(self, ctx, query):
        self.result = []
        headers = {"Authorization": f"Bearer {GENIUS_TOKEN}"}

        await ctx.send("Sending request...")
        response = requests.get(
            f"{self.GENIUS_API_BASE_URL}/search?q={query}", headers=headers
        )

        if response.status_code == 200:
            response.raise_for_status()
            data = response.json()

            try:
                song = data["response"]["hits"][0]["result"]
                lyrics_url = song["url"]
                artist = song["artist_names"]
                title = song["title"]
                img = song["song_art_image_thumbnail_url"]

                self.result.extend([artist, title, img])

                lyrics_page = requests.get(lyrics_url)

                if lyrics_page.status_code == 200:
                    await ctx.send(f"Successfully fetched website...")
                    lyrics_page.raise_for_status()
                    soup = BeautifulSoup(lyrics_page.text, "html.parser")

                    for br in soup.find_all("br"):
                        br.replace_with("\n")

                    for com in soup.find_all(
                        True,
                        {
                            "class": [
                                "ReferentFragmentdesktop__Highlight-sc-110r0d9-1 jAzSMw",
                                "Lyrics__Container-sc-1ynbvzw-1 kUgSbL",
                            ]
                        },
                    ):
                        self.result.append(com.text.strip())

                else:
                    await ctx.send("Failed to fetch website...")
                    self.result.append(lyrics_page.status_code)
                    return self.result
            except:
                await ctx.send("Failed to find search result...")
                self.result.append(0)
            return self.result

        else:
            await ctx.send("Failed to fetch website...")
            self.result.append(response.status_code)
            return self.result
