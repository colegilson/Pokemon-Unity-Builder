from dotenv import load_dotenv
import os

load_dotenv()

def main():
    for i in range(1, 387):
        dex_num = f"{(i):03d}"
        update_asset_guids(dex_num)

def get_sprite_guids(pokedex_number:int) -> list[str]:
    front_sprites_path = os.getenv("path_to_folder_front")
    back_sprites_path = os.getenv("path_to_folder_back")

    dex_num = f"{(pokedex_number):03d}"
    filename = f"\{dex_num}.png.meta"

    file_path_front = front_sprites_path + filename
    file_path_back = back_sprites_path + filename

    with open(file_path_front, 'r') as file:
        front_sprite_guid = file.readlines()[1]
        front_sprite_guid = front_sprite_guid.split(" ")[1]
    with open(file_path_back, 'r') as file:
        back_sprite_guid = file.readlines()[1]
        back_sprite_guid = back_sprite_guid.split(" ")[1]

    return [front_sprite_guid[:-1], back_sprite_guid[:-1]] # removes newline character

def update_asset_guids(pokedex_number:str):
    sprite_guids = get_sprite_guids(int(pokedex_number))
    asset_path = os.getenv("path_to_folder_asset")
    for root, _, files in os.walk(asset_path):
        for file in files:
            if file.startswith(pokedex_number) and file.endswith(".asset"):
                # print(f"found {pokedex_number}!")
                # return
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()

                lines[16] = f'  frontSprite: {{fileID: {os.getenv("file_id_sprite")}, guid: {sprite_guids[0]}, type: 3}}\n'
                lines[17] = f'  backSprite: {{fileID: {os.getenv("file_id_sprite")}, guid: {sprite_guids[1]}, type: 3}}\n'

                with open(file_path, 'w') as f:
                    f.writelines(lines)
    return

if __name__ == main():
    main()