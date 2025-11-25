import os
from dotenv import load_dotenv

load_dotenv()

# Telegram API
API_ID = int(os.getenv("API_ID", 24569721))  
API_HASH = os.getenv("API_HASH", "b0081b01a3f015d9c76f5ed9e7b20271")

# Bot Token / String Session
BOT_TOKEN = os.getenv("BOT_TOKEN", "")
STRING1 = os.getenv("STRING_SESSION", None)

# Database
MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://pusers:adcreation@adcreation.k8oapou.mongodb.net/?appName=ADCREATION")

# Owner / Admin
OWNER_ID = int(os.getenv("OWNER_ID", 7803657513))
OWNER_USERNAME = os.getenv("OWNER_USERNAME", "WTF_NoHope")

# Support / Updates
SUPPORT_GRP = os.getenv("SUPPORT_GRP", "AnanyaBotSupport")
UPDATE_CHNL = os.getenv("UPDATE_CHNL", "AnanyaBots")
