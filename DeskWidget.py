import tkinter as Tk
import subprocess as sp
import os as os
import configparser as cp
from functools import partial
from ahk import AHK

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
        try:
            self.res3x = config['Resolution Three']['width']
            self.res3y = config['Resolution Three']['height']
        except:
            self.options = 2
        
        key1 = config['HotKey']['key1']
        key2 = config['HotKey']['key2']
        self.key = self.__assignkey(key1) + key2
        self.ahk.add_hotkey(self.key, callback=partial(self.resolution_changer,
                                                            flip=True))
        self.ahk.start_hotkeys()  # start the hotkey process thread
        self.geometry("250x50")
        self.title(f"{config['Title']['Title']}")
        self.resizable(1,1)
        self.columnconfigure(index=0, weight=1)
        self.columnconfigure(index=1, weight=1)
        if self.options == 3:
            self.columnconfigure(index=2, weight=1)
        
        self.res1 = Tk.Button(self,command=partial(self.resolution_changer,
                                                   option=0))
        self.res1.configure(text=f"{self.res1x}x{self.res1y}")
        
        self.res2 = Tk.Button(self,command=partial(self.resolution_changer,
                                                   option=1))
        self.res2.configure(text=f"{self.res2x}x{self.res2y}")
        
        if self.options == 3:
            self.res3 = Tk.Button(self,command=partial(self.resolution_changer,
                                                      option=2))
            self.res3.configure(text=f"{self.res3x}x{self.res3y}")
        
        self.res1.configure(height=3)
        self.res1.grid(row=0, column=0, sticky='nsew')
        self.res2.grid(row=0, column=1, sticky='nsew')
        if self.options == 3:
            self.res3.grid(row=0, column=2, sticky='nsew')
        self.resolution_toggle = 0
        self.update()
        
    def resolution_changer(self, flip=False, option=0):
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
            self.title(f"{self.res1x}x{self.res1y}")
        elif self.resolution_toggle == 1:
            sp.call(f"./qres.exe /x {self.res2x} /y {self.res2y}")
            self.title(f"{self.res2x}x{self.res2y}")
        else:
            if self.options == 3:
                sp.call(f"./qres.exe /x {self.res3x} /y {self.res3y}")
                self.title(f"{self.res3x}x{self.res3y}")
    
    def __del__(self):
        pass
    
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

        
        
def main():
  app = Window()
  app.mainloop()

if __name__ == "__main__":
  main()