import tkinter as tk
import tkinter.simpledialog

import active_encounter as encounter
from verticalscrollwin import VerticalScrolledFrame


class EnemyManagerWindow(tk.Tk):
    def __init__(self, 
                input_dict: dict,
                enc_state: encounter.EncounterStorage):
        self.enemy_name = input_dict['enemy_name']
        self.hp_max = input_dict['max_health']
        self.ac = input_dict['ac']
        self.enc_state = enc_state
        super().__init__()
        self._setup()
        if 'units' in input_dict:
            for unit_hp in input_dict['units']:
                self._create_enemy_widget(unit_hp)
        # Event for on window close
        self.protocol("WM_DELETE_WINDOW", self._on_destroy)
        
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

        # Scrolling frame for individual enemies
        self.enemyFrame = VerticalScrolledFrame(self)
        self.enemyFrame.grid(row=0, column=1, padx=(10, 10), pady=(5,5), sticky='nsew')
        self.enemyFrame.update_idletasks()  # Ensure geometry info is updated
        self.enemyFrame.config(width=150, height=200)
        # Prevent frame from resizing to fit its contents
        self.enemyFrame.pack_propagate(False)
        self.enemyFrame.config(bd=2, relief='groove')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def start(self):
        self.mainloop()
        
    def _on_destroy(self):
        # Update old state info
        self.enc_state.enemyStatus[self.enemy_name] = self._serialize()
        self.destroy()

    def _update_enemy_selection(self, amt: int):
        old_val = self.enemyNum.get()
        # Check bound
        if old_val + amt < 0:
            return
        self.enemyNum.set(old_val + amt)
        if old_val < self.enemyNum.get():
            self._create_enemy_widget()
        else:
            self._remove_enemy_widget()

    def _create_enemy_widget(self, 
                             cur_hp: int = None):
        enemy_widget = tk.Frame(master=self.enemyFrame.interior)
        enemyHealth = tk.IntVar(master=enemy_widget, value=cur_hp if cur_hp != None else self.hp_max)
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
        
    def _remove_enemy_widget(self):
        children = self.enemyFrame.interior.winfo_children()
        # Check if there's an enemy with 0 HP
        for u_idx in range(len(self._get_unit_health())):
            if self._get_unit_health()[u_idx] == 0:
                 break
        # Remove child at u_idx
        children[u_idx].destroy()
        
    def _get_unit_health(self):
        return [self.enemyFrame.interior.winfo_children()[i].winfo_children()[0].cget('text') 
              for i in range(len(self.enemyFrame.interior.winfo_children()))]

    def _serialize(self):
        this_status = {
            "enemy_name": self.enemy_name,
            "ac": self.ac,
            "max_health": self.hp_max,
            "units": self._get_unit_health()
        }
        return this_status
    