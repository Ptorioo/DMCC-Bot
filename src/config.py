import os
import time
import asyncio
import discord
import logging
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()

OWNERS = os.getenv("OWNERS")

TOKEN = os.getenv("TOKEN")

PREFIX = os.getenv("PREFIX")

GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

SPOTIFY_ID = os.getenv("SPOTIFY_ID")

SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN")

PADLET_LINK = os.getenv("PADLET_LINK")
