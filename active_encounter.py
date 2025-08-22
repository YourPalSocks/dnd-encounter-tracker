from tkinter import filedialog

# Small class to store current encounter state
class EncounterStorage:
    def __init__(self):
        self.characters = [] # Displayed on left side
        self.combatants = [] # Displayed on right side
        self.enemyStatus = {} # Status recorded by enemy manager
        self.cur_combat = 0

    def next_turn(self):
        if (self.cur_combat + 1 >= len(self.combatants)):
            self.cur_combat = 0
        else:
            self.cur_combat += 1
        return self.combatants[self.cur_combat]
    
    def add_character(self, char):
        self.characters.append(char)

    def add_combatant(self, char: str, init: int):
        self.combatants.append({'Name': char, "Initiative": init})
        # Sort combatants by initiative
        self.combatants = sorted(self.combatants, key=lambda x:x['Initiative'], reverse=True)

    def remove_combatant(self, idx: int):
        c = self.combatants.pop(idx)
        self.combatants = sorted(self.combatants, key=lambda x:x['Initiative'], reverse=True)
        if c['Name'] in self.enemyStatus:
            self.enemyStatus.pop(c['Name'])
        
    def clear_characters(self):
        self.characters = []
        
    def clear_combatants(self):
        self.combatants = []
        self.enemyStatus = {}
        self.cur_combat = 0

    def save_state(self, f: str):
        # Prepare contents for saving. Save character list to file
        sv =  ','.join(self.characters)
        with open(f, mode='w') as file:
            file.write(sv)
    
    def load_state(self, f: str):
        with open(f, mode='r') as file:
            self.characters = file.readline().split(',')
    