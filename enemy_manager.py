import tkinter as tk

class EnemyManagerWindow(tk.Tk):
    def __init__(self, enemy_name: str):
        self.enemy_name = enemy_name
        super().__init__()
        # Set up window
        self.geometry('450x250')
        self.title(f'{self.enemy_name} Manager')
        self.resizable(False, False)
        self.enemyNum = tk.IntVar(master=self, value=0)

        # Set up frames
        self.infoFrame = tk.Frame(master=self)
        # Set up information
        name_lbl = tk.Label(master=self.infoFrame, text=f'NAME: {self.enemy_name}')
        name_lbl.pack()
        ac_lbl = tk.Label(master=self.infoFrame, text='AC: 15')
        ac_lbl.pack(pady=(0,10))
        # Main buttons
        add_enemy_button = tk.Button(master=self.infoFrame, text='+', 
                                     command=lambda: self.enemyNum.set(self.enemyNum.get() + 1))
        add_enemy_button.pack(expand=True, fill=tk.X)
        self.enemyNumLbl = tk.Label(master=self.infoFrame, textvariable=self.enemyNum)
        self.enemyNumLbl.pack()
        remove_enemy_button = tk.Button(master=self.infoFrame, text='-', 
                                        command=lambda: self.enemyNum.set(self.enemyNum.get() - 1))
        remove_enemy_button.pack(expand=True, fill=tk.X)
        self.infoFrame.grid(row=0, column=0, padx=(10, 10), pady=(5,5), sticky='nsew')

        # Individual enemy frame
        self.enemyFrame = tk.Frame(master=self)
        self.enemyFrame.grid(row=0, column=1, padx=(10, 10), pady=(5,5), sticky='nsew')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.mainloop()


if __name__ == '__main__':
    EnemyManagerWindow("Goblin")