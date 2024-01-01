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
        config = cp.ConfigParser()
        config.read('./config.ini')
        self.res1x = config['Resolution One']['width']
        self.res1y = config['Resolution One']['height']
        self.res2x = config['Resolution Two']['width']
        self.res2y = config['Resolution Two']['height']
        self.res3x = config['Resolution Three']['width']
        self.res3y = config['Resolution Three']['height']
        
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
        self.columnconfigure(index=2, weight=1)
        
        self.res1 = Tk.Button(self,command=partial(self.resolution_changer,
                                                   resx=self.res1x, rexy=self.res1y))
        self.res1.configure(text=f"{self.res1x}x{self.res1y}")
        
        self.res2 = Tk.Button(self,command=partial(self.resolution_changer,
                                                   resx=self.res2x, rexy=self.res2y))
        self.res2.configure(text=f"{self.res2x}x{self.res2y}")
        
        self.res3 = Tk.Button(self,command=partial(self.resolution_changer,
                                                  resx=self.res3x, rexy=self.res3y))
        self.res3.configure(text=f"{self.res3x}x{self.res3y}")
        
        self.res1.configure(height=3)
        self.res1.grid(row=0, column=0, sticky='nsew')
        self.res2.grid(row=0, column=1, sticky='nsew')
        self.res3.grid(row=0, column=2, sticky='nsew')
        self.resolution_toggle = 0
        self.update()
        
    def test(self):
        print("hotkey")
        
    def resolution_changer(self, flip=False, resx=0, resy=0):
        if flip:
            print(self.resolution_toggle)
            if self.resolution_toggle % 3 == 0:
                sp.call(f"./qres.exe /x {self.res1x} /y {self.res1y}")
                self.title(f"{self.res1x}x{self.res1y}")
            elif self.resolution_toggle % 3 == 1:
                sp.call(f"./qres.exe /x {self.res2x} /y {self.res2y}")
                self.title(f"{self.res2x}x{self.res2y}")
            else:
                sp.call(f"./qres.exe /x {self.res3x} /y {self.res3y}")
                self.title(f"{self.res3x}x{self.res3y}")
            self.resolution_toggle += 1
            if self.resolution_toggle > 5:
                self.resolution_toggle = 0
        else:
            sp.call(f"./qres.exe /x {resx} /y {resy}")
            self.title(f"{resx}x{resy}")
            

    def resolution_one(self):
        sp.call(f"./qres.exe /x {self.res1x} /y {self.res1y}")
        self.resolution_toggle = False
        self.title(f"{self.res1x}x{self.res1y}")
        
    def resolution_two(self):
        sp.call(f"./qres.exe /x {self.res2x} /y {self.res2y} ")
        self.resolution_toggle = True
        self.title(f"{self.res2x}x{self.res2y}")
        
    def resolution_three(self):
        sp.call(f"./qres.exe /x {self.res3x} /y {self.res3y} ")
        self.resolution_toggle = True
        self.title(f"{self.res3x}x{self.res3y}")
        
    def toggle(self):
        print(self.resolution_toggle)
        if self.resolution_toggle % 3 == 0:
            self.resolution_toggle = False
            self.resolution_one()
        elif self.resolution_toggle % 3 == 1:
            self.resolution_toggle = True
            self.resolution_two()
        else:
            self.resolution_toggle = True
            self.resolution_three()
        self.resolution_toggle += 1
        if self.resolution_toggle > 5:
            self.resolution_toggle = 0
    
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