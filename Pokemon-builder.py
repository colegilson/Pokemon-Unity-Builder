import os
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Union
from dotenv import load_dotenv
from enum import Enum
import os

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
    """
    Collect a list of all the pokédex numbers of the Pokémon already created
    """
    dex_numbers = []
    try:
        all_files = os.listdir(os.getenv("path_to_folder"))
    except:
        return []
    for file in all_files:
        dex_numbers.append(file[:3])
    return dex_numbers

def find_next(cur_dex_num: int, dex_values: list) -> int:
    """
    Gets the next unused Pokédex number from your given directory
    """
    while str(cur_dex_num) in dex_values:
        cur_dex_num = int(cur_dex_num) + 1
        cur_dex_num = f"{cur_dex_num:03d}"
    return cur_dex_num

def reset_entries() -> None:
    """
    Resets the entries to their placeholder values, except it increments the Dex number to the next unused value
    """
    cur_dex_num = dex.get()
    new_dex = find_next(cur_dex_num, dex_numbers())
    dex.delete(0, tk.END)
    dex.insert(0, new_dex)

    name.delete(0, tk.END)
    add_placeholder(name, "Charmander")

    type_a_entry.delete(0, tk.END)
    type_b_entry.delete(0, tk.END)
    
    catch.delete(0, tk.END)
    add_placeholder(catch, 45)

    exp.delete(0, tk.END)
    add_placeholder(exp, 62)

    growth.delete(0, tk.END)
    hitpoints.delete(0, tk.END)
    add_placeholder(hitpoints, 39)

    attack.delete(0, tk.END)
    add_placeholder(attack, 52)

    defence.delete(0, tk.END)
    add_placeholder(defence, 43)

    special_attack.delete(0, tk.END)
    add_placeholder(special_attack, 60)

    special_defence.delete(0, tk.END)
    add_placeholder(special_defence, 50)

    speed.delete(0, tk.END)
    add_placeholder(speed, 65)

    bst_label.config(text="Base Stat Total: 0")

def add_placeholder(entry: ttk.Entry, placeholder: Union[str, int]) -> None:
    """
    Adds placeholder text to field to guide user to using correct format
    """
    entry.insert(0, placeholder)
    entry.config(foreground="grey")

    def on_focus_in(event: None) -> None:
        """
        Activates when a given entry is the focus of the tab
        """
        if str(entry.cget("foreground")) == "grey":
            entry.delete(0, tk.END)
            entry.config(foreground="black")

    def on_focus_out(event: None) -> None:
        """
        Activates when a given entry is no longer the focus of the tab
        """
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(foreground="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

def update_bst(*args) -> None:
    """
    Update base stat total (BST) text at the bottom of the window
    """
    try:
        stats = [int(hitpoints.get()), int(attack.get()), int(defence.get()),
        int(special_attack.get()), int(special_defence.get()), int(speed.get())]
        bst_label.config(text=f"Base Stat Total: {sum(stats)}")
    except ValueError:
        bst_label.config(text="Base Stat Total: 0")

def save_pokemon() -> None:
    """
    Saves the Pokémon information to your desired destination
    """
    # format pokédex number
    dex_values = dex_numbers()
    dex_num = f"{int(dex.get()):03d}"

    # check if pokémon already exists
    if dex_num in dex_values:
        if not messagebox.askyesno("Overwrite?", f"A saved Pokémon with Pokédex number {dex_num} already exists. Would you like to overwrite the existing file?"):
            return

    pokemon_name = name.get().capitalize()
    type_a = TYPES[str(type_a_entry.get())].value
    type_b = TYPES[type_b_entry.get()].value
    catch_rate = catch.get()
    exp_yield = exp.get()
    growth_rate = GROWTH_RATES[growth.get()].value

    stats = {
        "hitpoints": hitpoints.get(),
        "attack": attack.get(),
        "defence": defence.get(),
        "specialAttack": special_attack.get(),
        "specialDefence": special_defence.get(),
        "speed": speed.get()
    }

    filename = f"{dex_num}-{pokemon_name}.asset"
    filepath = os.path.join(os.getenv("path_to_folder"), filename)

    with open(filepath, "w") as file:
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
  hitpoints: {stats['hitpoints']}
  attack: {stats['attack']}
  defence: {stats['defence']}
  specialAttack: {stats['specialAttack']}
  specialDefence: {stats['specialDefence']}
  speed: {stats['speed']}""")
                
    messagebox.showinfo("Saved", f"Saved {filename} successfully!")

    # increment dex number and clear fields
    reset_entries()

# implement GUI using tkinter
root = tk.Tk()
root.title("Pokémon Asset Creator")

frame = ttk.Frame(root, padding=10)
frame.grid(row=0, column=0, sticky="nsew", padx=(32,32))

# entries
entry_labels = ["Dex Number:", "Name:", "Primary Type:", "Secondary Type:", "Catch Rate:", "EXP Yield:",
"HP:", "Attack:", "Defence:", "Sp. Attack:", "Sp. Defence:", "Speed:"]

ttk.Label(frame, text="Dex Number:").grid(row=0, column=0, sticky="e")
dex = ttk.Entry(frame, width=20)
dex.grid(row=0, column=1)
add_placeholder(dex, 4)

ttk.Label(frame, text="Name:").grid(row=1, column=0, sticky="e")
name = ttk.Entry(frame, width=20)
name.grid(row=1, column=1)
add_placeholder(name, "Charmander")

ttk.Label(frame, text="Primary Type:").grid(row=2, column=0, sticky="e")
type_a_entry = ttk.Combobox(frame, values=[t.name for t in TYPES], width=17, state="readonly")
type_a_entry.set("FIRE")
type_a_entry.grid(row=2, column=1, padx=(0,1))

ttk.Label(frame, text="Secondary Type:").grid(row=3, column=0, sticky="e")
type_b_entry = ttk.Combobox(frame, values=[t.name for t in TYPES], width=17, state="readonly")
type_b_entry.set("NONE")
type_b_entry.grid(row=3, column=1, padx=(0,1))

ttk.Label(frame, text="Catch Rate:").grid(row=4, column=0, sticky="e")
catch = ttk.Entry(frame, width=20)
catch.grid(row=4, column=1)
add_placeholder(catch, 45)

ttk.Label(frame, text="EXP Yield:").grid(row=5, column=0, sticky="e")
exp = ttk.Entry(frame, width=20)
exp.grid(row=5, column=1)
add_placeholder(exp, 62)

ttk.Label(frame, text="Growth Rate:").grid(row=6, column=0, sticky="e")
growth = ttk.Combobox(frame, values=[g.name for g in GROWTH_RATES], width=17, state="readonly")
growth.set("FAST")
growth.grid(row=6, column=1, padx=(0,1))

# base stats
ttk.Label(frame, text="hitpoints:").grid(row=7, column=0, sticky="e")
hitpoints = ttk.Entry(frame, width=20)
hitpoints.grid(row=7, column=1)
add_placeholder(hitpoints, 39)

ttk.Label(frame, text="Attack:").grid(row=8, column=0, sticky="e")
attack = ttk.Entry(frame, width=20)
attack.grid(row=8, column=1)
add_placeholder(attack, 52)

ttk.Label(frame, text="Defence:").grid(row=9, column=0, sticky="e")
defence = ttk.Entry(frame, width=20)
defence.grid(row=9, column=1)
add_placeholder(defence, 43)

ttk.Label(frame, text="Special Attack:").grid(row=10, column=0, sticky="e")
special_attack = ttk.Entry(frame, width=20)
special_attack.grid(row=10, column=1)
add_placeholder(special_attack, 60)

ttk.Label(frame, text="Special Defence:").grid(row=11, column=0, sticky="e")
special_defence = ttk.Entry(frame, width=20)
special_defence.grid(row=11, column=1)
add_placeholder(special_defence, 50)

ttk.Label(frame, text="Speed:").grid(row=12, column=0, sticky="e")
speed = ttk.Entry(frame, width=20)
speed.grid(row=12, column=1)
add_placeholder(speed, 65)

# base stat total value (adds the sum of the stats)
bst_label = ttk.Label(frame, text="Base Stat Total: 0")
bst_label.grid(row=13, column=0, columnspan=2, pady=5)

# attach a trace to update BST whenever a stat changes
for e in [hitpoints, attack, defence, special_attack, special_defence, speed]:
    e.bind("<KeyRelease>", update_bst)

# save button
save_btn = ttk.Button(frame, text="Save Pokémon", command=save_pokemon)
save_btn.grid(row=14, column=0, columnspan=2, pady=10)

# save button shortcut
root.bind("<Return>", lambda event: save_pokemon())

# close window shortcut
def close_window(event=None) -> None:
    """
    closes the window via a shortcut
    """
    root.destroy()

root.bind("<Control-w>", close_window)

root.mainloop()
