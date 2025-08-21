import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog

import active_encounter as encounter
import enemy_manager

## Button Functions to communicate to active_encounter
def add_character(root: tk.Tk,
                  enc_state: encounter.EncounterStorage):
    char_n = simpledialog.askstring('Add Character', 'Enter character name')
    if char_n != '' or char_n != None:
        enc_state.add_character(char_n)
        # Update listbox
        lstbox: tk.Listbox = root.pack_slaves()[0].pack_slaves()[1]
        lstbox.delete(0, tk.END)
        idx = 0
        for char in enc_state.characters:
            lstbox.insert(idx, char)
            idx += 1

def remove_character(root: tk.Tk,
                     selected_idx: int,
                     enc_state: encounter.EncounterStorage):
    enc_state.characters.pop(selected_idx)
    # Update listbox
    lstbox: tk.Listbox = root.pack_slaves()[0].pack_slaves()[1]
    lstbox.delete(0, tk.END)
    idx = 0
    for char in enc_state.characters:
        lstbox.insert(idx, char)
        idx += 1

def add_to_combat(root: tk.Tk,
                  selected_idx: int,
                  enc_state: encounter.EncounterStorage):
    p = enc_state.characters[selected_idx]
    init = simpledialog.askinteger('Add to Combat', f'Enter Initiative for {p}')
    if init != None:
        enc_state.add_combatant(p, init)
        # Update combat box
        lstbox: tk.Listbox = root.pack_slaves()[2].pack_slaves()[1]
        lstbox.delete(0, tk.END)
        idx = 0
        for combat in enc_state.combatants:
            lstbox.insert(idx, combat['Name'])
            idx += 1
            # Highlight top combatant
            lstbox.itemconfig(0, bg='yellow')

def remove_from_combat(root: tk.Tk,
                       selected_idx: int,
                       enc_state: encounter.EncounterStorage):
    enc_state.remove_combatant(selected_idx)
    # Update combat box
    lstbox: tk.Listbox = root.pack_slaves()[2].pack_slaves()[1]
    lstbox.delete(0, tk.END)
    idx = 0
    for combat in enc_state.combatants:
        lstbox.insert(idx, combat['Name'])
        idx += 1
        # Highlight top combatant
        lstbox.itemconfig(0, bg='yellow')

def start_next_turn(root: tk.Tk,
                    enc_state: encounter.EncounterStorage):
    if len(enc_state.combatants) > 0:
        lstbox: tk.Listbox = root.pack_slaves()[2].pack_slaves()[1]
        next = enc_state.next_turn()
        # Update combat box
        lstbox.delete(0, tk.END)
        idx = 0
        # Re-build
        for combat in enc_state.combatants:
            lstbox.insert(idx, combat['Name'])
            # Check if current
            if combat['Name'] == next['Name']:
                lstbox.itemconfig(idx, bg='yellow')
            idx += 1

def display_selected_init(root: tk.Tk,
                          selected_idx: int,
                          enc_state: encounter.EncounterStorage):
    p = enc_state.combatants[selected_idx]
    messagebox.showinfo(f'{p['Name']}', f'Initiative for {p['Name']}: {p['Initiative']}')
    
def open_enemy_manager(root: tk.Tk,
                       selected_idx: int,
                       enc_state: encounter.EncounterStorage):
    selected = enc_state.combatants[selected_idx]
    # Check if current enemy has encounter storage information
    try:
        # Create from past state
        old_state = enc_state.enemyStatus[selected['Name']]
        enemy_manager.EnemyManagerWindow(old_state)        
    except:
        if messagebox.askyesno('Enemy Creation', f'Create new enemy for {selected['Name']}'):
            stats = simpledialog.askstring('Enter Enemy Stats', 'Enter Max HP,AC')
            stats = stats.split(',')
            state = {'enemy_name': selected['Name'],
                    'max_health': int(stats[0]),
                    'ac': int(stats[1])}
            enemy_manager.EnemyManagerWindow(state)

def clear_all(root: tk.Tk,
              enc_state: encounter.EncounterStorage):
    clear_characters(root, enc_state)
    clear_combat(root, enc_state)

def clear_characters(root: tk.Tk,
                     enc_state: encounter.EncounterStorage):
    lstbox: tk.Listbox = root.pack_slaves()[0].pack_slaves()[1]
    lstbox.delete(0, tk.END)
    enc_state.characters = []

def clear_combat(root: tk.Tk,
                 enc_state: encounter.EncounterStorage):
    if len(enc_state.combatants) > 1:
        lstbox: tk.Listbox = root.pack_slaves()[2].pack_slaves()[1]
        lstbox.delete(0, tk.END)
        enc_state.combatants = []

def save_chars(root: tk.Tk,
               enc_state: encounter.EncounterStorage):
    pth = filedialog.asksaveasfilename(defaultextension='.enc', filetypes=[("encounter file", "*.enc")])
    if pth != None or pth != '':
        enc_state.save_state(pth)

def load_chars(root: tk.Tk,
               enc_state: encounter.EncounterStorage):
    pth = filedialog.askopenfilename(defaultextension='.enc', filetypes=[("encounter file", "*.enc")])
    if pth != None or pth != '':
        enc_state.load_state(pth)
        # Update list
        lstbox: tk.Listbox = root.pack_slaves()[0].pack_slaves()[1]
        lstbox.delete(0, tk.END)
        idx = 0
        for char in enc_state.characters:
            lstbox.insert(idx, char)
            idx += 1


## Window setup and mainloop
VERSION = '1.1.1'
# Window setup
root = tk.Tk()
root.geometry('500x350')
root.resizable(False, False)
root.title(f'D&D Encounter Tracker -- {VERSION}')

# Menu
mainmenu = tk.Menu(root)
mainmenu.add_command(label='Open', command=lambda: load_chars(root, enc_state))
mainmenu.add_command(label='Save', command=lambda: save_chars(root, enc_state))
clear_menu = tk.Menu(mainmenu, tearoff=0)
clear_menu.add_command(label='All', command=lambda: clear_all(root, enc_state))
clear_menu.add_command(label='Characters', command=lambda: clear_characters(root, enc_state))
clear_menu.add_command(label='Combat', command=lambda: clear_combat(root, enc_state))
mainmenu.add_cascade(label='Clear', menu=clear_menu)
root.config(menu=mainmenu)
# Create data storage object
enc_state = encounter.EncounterStorage()

# Character panel
char_panel = tk.Frame(root, highlightbackground='black', highlightthickness=1, width=250)
char_lb = tk.Label(char_panel, text='Characters')
char_list = tk.Listbox(char_panel, selectmode=tk.SINGLE, justify='center', height=15)
char_list.bind('<Double-1>', func=lambda e: add_to_combat(root, char_list.curselection()[0], enc_state))
add_char = tk.Button(char_panel, text='Add', command=lambda: add_character(root, enc_state))
remove_char = tk.Button(char_panel, text='Remove', command=lambda: remove_character(root, char_list.curselection()[0], enc_state))
# Packing
char_panel.pack(side=tk.LEFT, expand=True, fill='both')
char_lb.pack()
char_list.pack(expand=True, fill='both')
add_char.pack(expand=True, fill='both')
remove_char.pack(expand=True, fill='both')

# Next Turn Button
next_turn = tk.Button(root, width=20, text='Next Turn', bg='light grey', 
                      command=lambda: start_next_turn(root, enc_state))
next_turn.pack(side=tk.LEFT, expand=True, fill='both')

# Combat Panels
combat_panel = tk.Frame(root, highlightbackground='black', highlightthickness=1, width=250)
combat_lb = tk.Label(combat_panel, text='Combat')
combat_list = tk.Listbox(combat_panel, selectmode=tk.NONE, justify='center', height=17)
combat_list.bind('<Double-1>', func=lambda e: display_selected_init(root, combat_list.curselection()[0], enc_state))
combat_list.bind('<Button-3>', func=lambda e: open_enemy_manager(root, combat_list.curselection()[0], enc_state))
remove_comb = tk.Button(combat_panel, text='Remove', height=0, command=lambda: remove_from_combat(root, combat_list.curselection()[0], enc_state))
# Packing
combat_panel.pack(side=tk.LEFT, expand=True, fill='both')
combat_lb.pack()
combat_list.pack(expand=True, fill='both')
remove_comb.pack(expand=True, fill='both')

# Main loop
root.mainloop()
