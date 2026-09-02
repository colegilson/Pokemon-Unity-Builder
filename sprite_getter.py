from dotenv import load_dotenv
import os
import requests
from PIL import Image
from io import BytesIO

load_dotenv()
BASEURL = "https://pokeapi.co/api/v2/pokemon/"

def main():
    for i in range(1, 387):
        response = requests.get(BASEURL+str(i)+"/").json()

        try:
            back_sprite_url = response["sprites"]['versions']['generation-iii']["firered-leafgreen"]["back_default"]
            front_sprite_url = response["sprites"]['versions']['generation-iii']["firered-leafgreen"]["front_default"]
            assert back_sprite_url != None

        except:
            back_sprite_url = response["sprites"]['versions']['generation-iii']["ruby-sapphire"]["back_default"]
            front_sprite_url = response["sprites"]['versions']['generation-iii']["ruby-sapphire"]["front_default"]
            
        back_sprite = Image.open(BytesIO(requests.get(back_sprite_url).content))
        front_sprite = Image.open(BytesIO(requests.get(front_sprite_url).content))
        
        dex_num = f"{(i):03d}"
        filename = f"{dex_num}.png"
        back_sprite.save(os.path.join(os.getenv("path_to_folder_back"), filename))
        front_sprite.save(os.path.join(os.getenv("path_to_folder_front"), filename))

if __name__ == main():
    main()