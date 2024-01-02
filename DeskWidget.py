import tkinter as Tk
import subprocess as sp
import os as os
import configparser as cp
from functools import partial
from ahk import AHK
import sys as sys

class Window(Tk.Tk):
    def __init__(self):
        super().__init__()
        self.ahk = AHK()
        self.options = 3
        config = cp.ConfigParser()
        config.read('./config.ini')
        self.res1x = config['Resolution One']['width']
        self.res1y = config['Resolution One']['height']
        self.res2x = config['Resolution Two']['width']
        self.res2y = config['Resolution Two']['height']
        self.windowx = config['Window']['width']
        self.windowy = config['Window']['height']
        
        try:
            self.res3x = config['Resolution Three']['width']
            self.res3y = config['Resolution Three']['height']
        except:
            self.options = 2
        
        key1 = config['HotKey']['key1']
        key2 = config['HotKey']['key2']
        self.key = self.__assignkey(key1) + key2
        self.ahk.add_hotkey(self.key, callback=partial(self.resolution_changer, True))
        self.ahk.start_hotkeys()  # start the hotkey process thread
        
        # get current screen position for inital placement
        self.screenx = self.winfo_screenwidth()
        self.screeny = self.winfo_screenheight()

        self.window = f"{self.windowx}x{self.windowy}+0+{(self.screeny-int(self.windowy)-3)}"
        self.geometry(self.window)
        self.wm_attributes('-topmost', True)
        self.overrideredirect(True)
        
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        if self.options == 3:
            self.columnconfigure(index=2, weight=1)
        
        # define button 1 
        self.res1 = Tk.Button(self,command=partial(self.resolution_changer,
                                                   option=0))
        self.res1.configure(text=f"{self.res1x}x{self.res1y}",
                            font=('arial',11, 'bold'),
                            relief='raised', height=2)
        self.res1.bind('<Button-3>', self.close)
        self.res1.bind('<Double-Button-1>', self.close)
        
        # define button 2 
        self.res2 = Tk.Button(self,command=partial(self.resolution_changer,
                                                   option=1))
        self.res2.configure(text=f"{self.res2x}x{self.res2y}",
                            font=('arial',11, 'bold'),
                            relief='raised', height=2)
        self.res2.bind('<Button-3>', self.close)
        self.res2.bind('<Double-Button-1>', self.close)
        
        # define button 3 
        if self.options == 3:
            self.res3 = Tk.Button(self,command=partial(self.resolution_changer,
                                                      option=2))
            self.res3.configure(text=f"{self.res3x}x{self.res3y}",
                            font=('arial',11, 'bold'),
                            relief='raised', height=2)
            self.res3.bind('<Button-3>', self.close)
            self.res3.bind('<Double-Button-1>', self.close)
        
        # place buttons in window
        self.res1.grid(row=0, column=0, sticky='nsew')
        self.res2.grid(row=0, column=1, sticky='nsew')
        if self.options == 3:
            self.res3.grid(row=0, column=2, sticky='nsew')
            
        # assign dummy value to toggle
        if str(self.screenx) == self.res1x:
            self.resolution_toggle = 0
        elif str(self.screenx) == self.res2x:
            self.resolution_toggle = 1
        else:
            self.resolution_toggle = 2
        
        #set button color for selected option
        self.selected_color = config['Window']['selected']
        self.resolution_changer(option=self.resolution_toggle)
        self.button_color()
        self.update()
    def button_color(self):
        if self.resolution_toggle == 0:
            self.res1.configure(background=self.selected_color, relief='sunken')
            self.res2.configure(background="#f0f0f0", relief='raised')
            self.res3.configure(background="#f0f0f0", relief='raised')
            self.window = f"{self.windowx}x{self.windowy}+0+{(int(self.res1y)-int(self.windowy)-3)}"
            self.geometry(self.window)
        elif self.resolution_toggle == 1:
            self.res2.configure(background=self.selected_color, relief='sunken')
            self.window = f"{self.windowx}x{self.windowy}+0+{(int(self.res2y)-int(self.windowy)-3)}"
            self.geometry(self.window)
            self.res1.configure(background="#f0f0f0", relief='raised')
            self.res3.configure(background="#f0f0f0", relief='raised')
        else:
            self.res3.configure(background=self.selected_color, relief='sunken')
            self.window = f"{self.windowx}x{self.windowy}+0+{(int(self.res3y)-int(self.windowy)-3)}"
            self.geometry(self.window)
            self.res1.configure(background="#f0f0f0", relief='raised')
            self.res2.configure(background="#f0f0f0", relief='raised')

    def resolution_changer(self, flip=False, option=0):
        self.lift()
        if flip:
            if self.options == 3:
                if self.resolution_toggle == 2:
                    self.resolution_toggle = 0
                else:
                    self.resolution_toggle += 1
            else:
                if self.resolution_toggle == 1:
                    self.resolution_toggle = 0
                else:
                    self.resolution_toggle = 1
        else:
            self.resolution_toggle = option
        if self.resolution_toggle == 0:
            sp.call(f"./qres.exe /x {self.res1x} /y {self.res1y}")
        elif self.resolution_toggle == 1:
            sp.call(f"./qres.exe /x {self.res2x} /y {self.res2y}")
        else:
            if self.options == 3:
                sp.call(f"./qres.exe /x {self.res3x} /y {self.res3y}")
        self.button_color()
    
    def close(self, event):
        self.ahk.stop_hotkeys()
        self.destroy()
        self.quit()
        sys.exit()
    
    def __assignkey(self, key):
        match key.lower():
            case 'alt':
                return '!'
            case 'alt_r':
                return '>!'
            case 'alt_l':
                return '<!'
            case 'ctrl':
                return '^'
            case 'ctrl_l':
                return '<^'
            case 'ctrl_r':
                return '>^'
            case 'shift':
                return '+'
            case 'shift_l':
                return '<+'
            case 'shift_r':
                return '>+'               
            case _:
                return ''
  
app = Window()
def keep_top():
    app.lift()
    app.after(2000,keep_top)
keep_top()
app.mainloop()


