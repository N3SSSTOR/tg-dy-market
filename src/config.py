import os 
import dotenv 

dotenv.load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME")