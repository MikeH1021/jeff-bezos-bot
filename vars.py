import os
from dotenv import load_dotenv

load_dotenv()

# Authentication Tokens
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')

# Blink Authentication
BLINK_USERNAME = os.getenv('BLINK_USERNAME')
BLINK_PASSWORD = os.getenv('BLINK_PASSWORD')

GUILD_ID = 933259754174824468
LOG_CH_ID = 935281079298965594