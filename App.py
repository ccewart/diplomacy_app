import tkinter as tk
from Game import *


class App(tk.Frame):
    def __init__(self, parent, game, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title("Diplomacy")

        self.game = game
        self.game.next_phase()
        self.game.next_phase()
        self.game.next_phase()
        self.game.next_phase()

        self.print_phase_btn = tk.Button(self.parent, text="Print phase", command=self.print_phase, image=pixel,
                                         height=20, width=100, compound="c").grid(row=0, column=0)
        self.next_phase_btn = tk.Button(self.parent, text="Next phase", command=self.change_phase, image=pixel,
                                        height=20, width=100, compound="c").grid(row=0, column=2)

        self.phase_lbl = tk.Label(self.parent, text=self.game.get_phase, image=pixel, height=20, width=100, compound="c")
        self.phase_lbl.grid(row=0, column=1)

        self.btn1 = RegionButton(root, self.game, "Clyde").grid(row=1, column=0)
        self.btn2 = RegionButton(root, self.game, "Edinburgh").grid(row=1, column=1)
        self.btn3 = RegionButton(root, self.game, "Norwegian Sea").grid(row=1, column=2)
        self.btn4 = RegionButton(root, self.game, "Yorkshire").grid(row=2, column=0)
        self.btn5 = RegionButton(root, self.game, "Liverpool").grid(row=2, column=1)
        self.btn6 = RegionButton(root, self.game, "North Sea").grid(row=2, column=2)

    def change_phase(self):
        self.game.next_phase()
        self.phase_lbl.configure(text=self.game.get_phase)

    def get_phase(self):
        return self.game.get_phase

    def print_phase(self):
        print(self.get_phase())


class RegionButton(tk.Frame):
    def __init__(self, parent, game, name, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.game = game
        self.name = name
        self.army = False
        self.btn = tk.Button(self, command=self.click_button, image=pixel, height=100, width=100, compound="c")
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

    def move_unit(self):
        pass

    def click_button(self):
        if self.game.get_phase == "build":
            print("building unit")
            self.create_unit()
        elif self.game.get_phase == "orders":
            print("moving unit")
            self.move_unit()


if __name__ == "__main__":
    root = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)
    army_img = tk.PhotoImage(file=r"army.png")
    game = Game(2)
    App(root, game).grid()
    root.mainloop()
