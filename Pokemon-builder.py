from dotenv import load_dotenv
import os

dex_num = 0
load_dotenv()

def dex_numbers() -> list:
    dex_numbers = []
    all_files = os.listdir(os.getenv("path_to_folder"))
    for file in all_files:
        dex_numbers.append(file[:3])
    return dex_numbers

if __name__ ==  '__main__':
    flag = True
    while flag:
        dex_values = dex_numbers()
        if dex_num == 0:
            dex_num = int(input("What is the Pokemon's dex number?\n"))
            dex_num = f"{dex_num:03d}"
        else:
            dex_num = int(dex_num) + 1
            dex_num = f"{dex_num:03d}"
            while str(dex_num) in dex_values:
                dex_num = int(dex_num) + 1
                dex_num = f"{dex_num:03d}"
            print(dex_num)
        pokemon_name = input("What is the Pokemon's name?\n")

        is_done = input("are there others? [y/n]\n")
        if is_done.lower().startswith("n"):
            flag = False


    
    # filename = f"{dex_num}-{pokemon_name}.asset"
