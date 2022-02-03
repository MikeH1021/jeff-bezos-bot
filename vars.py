import os
from dotenv import load_dotenv

load_dotenv()

# Authentication Tokens
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')

# Blink Authentication
BLINK_USERNAME = os.getenv('BLINK_USERNAME')
BLINK_PASSWORD = os.getenv('BLINK_PASSWORD')

# Environment
PY_ENV = os.getenv('PY_ENV')

# Tuya Authentication
TUYA_API_KEY = os.getenv('TUYA_API_KEY')
TUYA_API_SECRET = os.getenv('TUYA_API_SECRET')
TUYA_DEVICE_ID = os.getenv('TUYA_DEVICE_ID')

MY_ID = 450704927879069696
KYLE_ID = 233262836506165252
GUILD_ID = 933259754174824468
KYLE_LOG_CH_ID = 933266710209908747
GROW_LOG_CH_ID = 933266727519809568
PEPPER_LOG_CH_ID = 938882597029830696
MUSHROOM_LOG_CH_ID = 938879469719003266
MOVIES_CH_ID = 937519245053530194

# Plex Downloader
# Radarr API Token
R_TOKEN = os.getenv('R_TOKEN')
# Radarr Host Url
R_HOST_URL = os.getenv('R_HOST_URL')
# Sonarr API Token
S_TOKEN = None
# Sonarr Host Url
S_HOST_URL = None
# IMDB API Key
IMDB_API_KEY = os.getenv('IMDB_API_KEY')
# Set your server name to be referenced in message responses
SERVER_NAME = 'Lil Nas-X'
# Set your discord name to be referenced in message responses
ADMIN_NAME = 'Mikeh1021#4070'
