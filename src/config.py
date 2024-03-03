import os
import json
import time
import asyncio
import discord
import logging
from discord.ext import commands, tasks

config = os.environ.get('CONFIG_JSON')

if config:
    configJSON = json.loads(config)
else:
    with open('CONFIG.json', 'r') as j:
        configJSON = json.loads(j.read())

OWNERS = configJSON["owners"]

TOKEN = configJSON["token"]

PREFIX = configJSON["prefix"]

GENIUS_ACCESS_TOKEN = configJSON["genius-token"]

SPOTIFY_ID = configJSON["spotify-id"]

SPOTIFY_TOKEN = configJSON["spotify-token"]

PADLET_LINK = configJSON["padlet-link"]
