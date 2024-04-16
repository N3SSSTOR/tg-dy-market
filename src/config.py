import os 
import dotenv 

dotenv.load_dotenv()

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
MONGODB_CONNECTION_URL = os.getenv("MONGODB_CONNECTION_URL")
SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME")

AAIO_API_KEY = os.getenv("AAIO_API_KEY")
AAIO_SHOP_ID = os.getenv("AAIO_SHOP_ID")
AAIO_SECRET_KEY_1 = os.getenv("AAIO_SECRET_KEY_1")
AAIO_SECRET_KEY_2 = os.getenv("AAIO_SECRET_KEY_2")

ASSET_PATH = "assets/"
UPLOAD_PATH = "upload/"

LOGO_PATH = ASSET_PATH + "img/logo.jpg"
SUPPORT_PATH = ASSET_PATH + "img/support.jpg"
ABOUT_PATH = ASSET_PATH + "img/about.jpg"
CATALOG_PATH = ASSET_PATH + "img/catalog.jpg"
PROFILE_PATH = ASSET_PATH + "img/profile.jpg"
HOME_PATH = ASSET_PATH + "img/home.jpg"
FAQ_PATH = ASSET_PATH + "img/faq.jpg"

FONT_PATH = ASSET_PATH + "fonts/ordina.ttf"