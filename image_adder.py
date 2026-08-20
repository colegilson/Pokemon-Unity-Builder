from dotenv import load_dotenv
from enum import Enum
import os
import requests
import json
from PIL import Image
from io import BytesIO

load_dotenv()
BASEURL = "https://pokeapi.co/api/v2/pokemon/"

class DIRECTION(Enum):
    FRONT = 0
    BACK = 1

def main():
    for i in range(1, 387):
        response = requests.get(BASEURL+str(i)+"/").json()

        back_sprite_url = response["sprites"]["back_default"]
        front_sprite_url = response["sprites"]["front_default"]
        back_sprite = Image.open(BytesIO(requests.get(back_sprite_url).content))
        front_sprite = Image.open(BytesIO(requests.get(front_sprite_url).content))

        print(back_sprite)
        print(front_sprite)
        dex_num = f"{(i):03d}"
        filename = f"{dex_num}.png"
        back_sprite.save(os.path.join(os.getenv("path_to_folder_back"), filename))
        front_sprite.save(os.path.join(os.getenv("path_to_folder_front"), filename))

if __name__ == main():
    main()