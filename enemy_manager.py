import tkinter as tk
import tkinter.simpledialog

class EnemyManagerWindow(tk.Tk):
    def __init__(self, 
                input_dict: dict) :
        self.enemy_name = input_dict['enemy_name']
        self.hp_max = input_dict['max_health']
        self.ac = input_dict['ac']
        super().__init__()
        self._setup()
        
    def _setup(self):
        # Set up window
        self.geometry('400x250')
        self.title(f'{self.enemy_name} Manager')
        self.resizable(False, False)
        self.enemyNum = tk.IntVar(master=self, value=0)

        # Set up frames
        self.infoFrame = tk.Frame(master=self)
        # Set up information
        name_lbl = tk.Label(master=self.infoFrame, text=f'NAME: {self.enemy_name}')
        name_lbl.pack()
        ac_lbl = tk.Label(master=self.infoFrame, text=f'AC: {self.ac}')
        ac_lbl.pack(pady=(0,10))
        # Main buttons
        add_enemy_button = tk.Button(master=self.infoFrame, text='+', 
                                     command=lambda: self._update_enemy_selection(1))
        add_enemy_button.pack(expand=True, fill=tk.X)
        self.enemyNumLbl = tk.Label(master=self.infoFrame, textvariable=self.enemyNum)
        self.enemyNumLbl.pack()
        remove_enemy_button = tk.Button(master=self.infoFrame, text='-', 
                                        command=lambda: self._update_enemy_selection(-1))
        remove_enemy_button.pack(expand=True, fill=tk.X)
        self.infoFrame.grid(row=0, column=0, padx=(10, 10), pady=(5,5), sticky='nsew')

        # Frame for individual enemies
        # TODO: Scrollbar
        self.enemyFrame = tk.Frame(self)
        self.enemyFrame.grid(row=0, column=1, padx=(10, 10), pady=(5,5), sticky='nsew')
        self.enemyFrame.update_idletasks()  # Ensure geometry info is updated
        self.enemyFrame.config(width=150, height=200)
        # Prevent frame from resizing to fit its contents
        self.enemyFrame.pack_propagate(False)
        self.enemyFrame.config(bd=2, relief='groove')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.mainloop()

    def _update_enemy_selection(self, amt: int):
        old_val = self.enemyNum.get()
        # Check bound
        if old_val + amt < 0:
            return
        self.enemyNum.set(old_val + amt)
        if old_val < self.enemyNum.get():
            self._create_enemy_widget()
        else:
            pass
            # TODO: Remove

    def _create_enemy_widget(self):
        enemy_widget = tk.Frame(master=self.enemyFrame)
        enemyHealth = tk.IntVar(master=self, value=self.hp_max)
        # Embedded functions to update local tk.IntVar
        def __update_health(hp_var, amt, max):
            hp_var.set(hp_var.get() + amt)
            if hp_var.get() > max:
                hp_var.set(max)
            if hp_var.get() < 0:
                hp_var.set(0)
                
        def __update_health_popup(hp_var, max):
            res = tkinter.simpledialog.askinteger('Damage Input', 'Enter Damage Amt', initialvalue=0)
            __update_health(hp_var, res, max)
        # Create components
        cur_health = tk.Label(master=enemy_widget, textvariable=enemyHealth)
        cur_health.bind('<Double-1>', func=lambda e: __update_health_popup(enemyHealth, self.hp_max))
        btn_left = tk.Button(master=enemy_widget, text='-', command=lambda: __update_health(enemyHealth, -1, self.hp_max))
        btn_right = tk.Button(master=enemy_widget, text='+', command=lambda: __update_health(enemyHealth, 1, self.hp_max))
        # Configure
        btn_left.config(width=3)
        btn_right.config(width=3)
        # Pack
        btn_left.pack(side=tk.LEFT, padx=(0, 20))
        cur_health.pack(side=tk.LEFT)
        btn_right.pack(side=tk.LEFT, padx=(20, 0))
        enemy_widget.pack(pady=5)
    