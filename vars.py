import os
from dotenv import load_dotenv

load_dotenv()

# Authentication Tokens
CLIENT_TOKEN = os.getenv('CLIENT_TOKEN')

# Blink Authentication
BLINK_USERNAME = os.getenv('BLINK_USERNAME')
BLINK_PASSWORD = os.getenv('BLINK_PASSWORD')

# Tuya Authentication
TUYA_API_KEY = os.getenv('TUYA_API_KEY')
TUYA_API_SECRET = os.getenv('TUYA_API_SECRET')
TUYA_DEVICE_ID = os.getenv('TUYA_DEVICE_ID')

GUILD_ID = 933259754174824468
LOG_CH_ID = 933266727519809568
