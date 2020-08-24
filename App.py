import tkinter as tk
from Game import *

class RegionButton(tk.Frame):
    def __init__(self, parent, name, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.army = False
        self.btn = tk.Button(self, command=self.create_unit, image=pixel, height=100, width=100, compound="c")
        self.btn.grid(row=1, column=0)
        self.lbl = tk.Label(self, text=name)
        self.lbl.grid(row=0, column=0)

    def create_unit(self):
        if not self.army:
            self.btn.configure(image=army_img)
            self.army = True
        else:
            self.btn.configure(image=pixel)
            self.army = False


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title("Diplomacy")

        self.next_phase_btn = tk.Button(self.parent, text="Next phase", command=self.change_phase, image=pixel,
                                        height=20, width=100, compound="c").grid(row=0, column=2)
        self.phase_lbl = tk.Label(self.parent, text="Build", image=pixel, height=20, width=100, compound="c")
        self.phase_lbl.grid(row=0, column=1)

        self.btn1 = RegionButton(root, "Clyde").grid(row=1, column=0)
        self.btn2 = RegionButton(root, "Edinburgh").grid(row=1, column=1)
        self.btn3 = RegionButton(root, "Norwegian Sea").grid(row=1, column=2)
        self.btn4 = RegionButton(root, "Yorkshire").grid(row=2, column=0)
        self.btn5 = RegionButton(root, "Liverpool").grid(row=2, column=1)
        self.btn6 = RegionButton(root, "North Sea").grid(row=2, column=2)

    def change_phase(self):
        self.phase_lbl.configure(text="Orders")


if __name__ == "__main__":
    root = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)
    army_img = tk.PhotoImage(file=r"army.png")
    App(root).grid()
    root.mainloop()
