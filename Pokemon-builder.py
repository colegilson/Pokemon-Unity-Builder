from dotenv import load_dotenv
from enum import Enum
import os

dex_num = 0
load_dotenv()

class TYPES(Enum):
    NONE = 0
    NORMAL = 1
    FIRE = 2
    WATER = 3
    ELECTRIC = 4
    GRASS = 5
    ICE = 6
    FIGHTING = 7
    POISON = 8
    GROUND = 9
    FLYING = 10
    PSYCHIC = 11
    BUG = 12
    ROCK = 13
    GHOST = 14
    DRAGON = 15
    DARK = 16
    STEEL = 17

class GROWTH_RATES(Enum):
    FAST = 0
    MEDIUM_FAST = 1
    MEDIUM_SLOW = 2
    SLOW = 3

def dex_numbers() -> list:
    dex_numbers = []
    all_files = os.listdir(os.getenv("path_to_folder"))
    for file in all_files:
        dex_numbers.append(file[:3])
    return dex_numbers

def find_next(cur_dex_num: int, dex_values: list) -> int:
    while str(cur_dex_num) in dex_values:
        cur_dex_num = int(cur_dex_num) + 1
        cur_dex_num = f"{cur_dex_num:03d}"
    return cur_dex_num

if __name__ ==  '__main__':
    flag = True
    while flag:
        dex_values = dex_numbers()
        
        if dex_num == 0:
            dex_num = int(input("What is the Pokemon's dex number?\n"))
            dex_num = f"{dex_num:03d}"
            
            if str(dex_num) in dex_values:
                overwrite = input("This dex number exists and a file already exists for this mon, do you want to write over this file? [y/n]\n")
            
                if overwrite.lower().startswith("n"):
                    dex_num = find_next(dex_num, dex_values)
        
        else:
            dex_num = find_next(dex_num, dex_values) 
            
        print(f"Give information for Pokemon with Pokedex number {dex_num} please")
        pokemon_name = input("What is this Pokemon's name?\n").lower().capitalize()
        type_a = input("What is the primary type?\n").upper()
        type_b = input("What is the primary type? ('none' for no secondary typing)\n").upper()
        
        for cur_type in TYPES:
            if type(type_a) is str and type_a in str(cur_type.name):
                type_a = cur_type.value
            elif type(type_b) is str and type_b in str(cur_type.name):
                type_b = cur_type.value
            elif type(type_a) is int and type(type_b) is int:
                break
                
        catch_rate = input("What is the catchrate? 1-255\n")
        exp_yield = input("How much exp do they yield?\n").upper()
        growth_rate = input("What is the Pokemon growth speed? (fast, medium_fast, medium_slow, slow)\n").upper()

        finding_growth_rate = True
        while finding_growth_rate:
            for rate in GROWTH_RATES:
                if growth_rate == str(rate.name):
                    growth_rate = rate.value
                    finding_growth_rate = False
                    break
            if finding_growth_rate:
                raise Exception("could not find growth rate")
        
        print("The following inputs are the BSTs of the Pokemon")
        
        hitpoints = int(input("What is the hitpoints?\n"))
        attack = int(input("What is the attack?\n"))
        defence = int(input("What is the defence?\n"))
        special_attack = int(input("What is the special attack?\n"))
        special_defence = int(input("What is the special defence\n"))
        speed = int(input("What is the speed?\n"))
        
        filename = f"{dex_num}-{pokemon_name}.asset"
        filename = os.path.join(os.getenv("path_to_folder"), filename)
        file = open(filename, "w")

        file.write(f"""%YAML 1.1
%TAG !u! tag:unity3d.com,2011:
--- !u!114 &11400000
MonoBehaviour:
  m_ObjectHideFlags: 0
  m_CorrespondingSourceObject: {{fileID: 0}}
  m_PrefabInstance: {{fileID: 0}}
  m_PrefabAsset: {{fileID: 0}}
  m_GameObject: {{fileID: 0}}
  m_Enabled: 1
  m_EditorHideFlags: 0
  m_Script: {{fileID: {os.getenv("file_id")}, guid: {os.getenv("guid")}, type: 3}}
  m_Name: {dex_num}-{pokemon_name}
  m_EditorClassIdentifier: 
  pokemonName: {pokemon_name}
  description: 
  frontSprite: {{fileID: 0}}
  backSprite: {{fileID: 0}}
  typeA: {type_a}
  typeB: {type_b}
  learnableMoves: []
  catchRate: {catch_rate}
  expYield: {exp_yield}
  growthRate: {growth_rate}
  hitpoints: {hitpoints}
  attack: {attack}
  defence: {defence}
  specialAttack: {special_attack}
  specialDefence: {special_defence}
  speed: {speed}""")

        file.close()

        is_done = input("are there others you'd like to add? [y/n]\n")
        if is_done.lower().startswith("n"):
            flag = False