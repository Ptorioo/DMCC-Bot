import os
import json
import asyncio
import discord
from discord.ext import commands, tasks

CURRENT_DIR = os.path.dirname(__file__)

BASE_DIR = os.path.dirname(CURRENT_DIR)

COGS_DIR = os.path.join(CURRENT_DIR, 'cog')

CONFIG_FILE_PATH = os.path.join(CURRENT_DIR, '..', 'CONFIG.json')

with open(CONFIG_FILE_PATH) as f:
    configJSON = json.load(f)

OWNERS = configJSON["owners"]

TOKEN = configJSON["token"]

PREFIX = configJSON["prefix"]