import os
import time
import asyncio
import discord
import logging
from discord.ext import commands, tasks
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

OWNERS = os.getenv("OWNERS")

GUILDS = os.getenv("GUILDS")

TOKEN = os.getenv("TOKEN")

PREFIX = os.getenv("PREFIX")

GENIUS_TOKEN = os.getenv("GENIUS_TOKEN")

SPOTIFY_ID = os.getenv("SPOTIFY_ID")

SPOTIFY_TOKEN = os.getenv("SPOTIFY_TOKEN")

PADLET_LINK = os.getenv("PADLET_LINK")

STREETVIEW_FOLDER = os.getenv("STREETVIEW_FOLDER")

STAFF_ROLE = os.getenv("STAFF_ROLE")

FORMER_STAFF_ROLE = os.getenv("FORMER_STAFF_ROLE")

MEMBER_ROLE = os.getenv("MEMBER_ROLE")

LIFE_MEMBER_ROLE = os.getenv("LIFE_MEMBER_ROLE")





sync_guilds = set(map(lambda x: discord.Object(int(x)), GUILDS.split(',')))