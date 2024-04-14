import time 

from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw 

from config import PROFILE_PATH, FONT_PATH, UPLOAD_PATH

TEXT_1_POS = (350, 100)
TEXT_2_POS = (341, 288)
TEXT_3_POS = (390, 375)
TEXT_4_POS = (367, 550)


def generate_profile_img(
        username: int, 
        days_in_market: int,
        total_purchases: int, 
        total_amount: int 
) -> str:
    img = Image.open(PROFILE_PATH)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(FONT_PATH, 40)

    texts = {
        username: TEXT_1_POS, 
        str(total_purchases) + (" раза" if 
            int(str(total_purchases)[-1]) <= 4 
            and int(str(total_purchases)[-1]) != 0 else " раз"): TEXT_2_POS, 
        str(total_amount)+"₽": TEXT_3_POS, 
        str(days_in_market) + (" дня" if 
            int(str(days_in_market)[-1]) <= 4 
            and int(str(days_in_market)[-1]) != 0 else " дней"): TEXT_4_POS
    }

    for text, pos in texts.items():
        fill = (255, 255, 255)
        draw.text(xy=pos, text=text, fill=fill, font=font)

    path = UPLOAD_PATH + f"{int(time.time())}.jpg"
    img.save(path)

    return path 