import tkinter as tk
from Game import *
from Orders import Order, CreateUnit

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
        self.print_orders_btn = tk.Button(self.parent, text="Print orders", command=self.print_orders, image=pixel,
                                         height=20, width=100, compound="c").grid(row=1, column=0)
        self.print_board_btn = tk.Button(self.parent, text="Print board", command=self.print_board, image=pixel,
                                         height=20, width=100, compound="c").grid(row=1, column=1)
        self.next_phase_btn = tk.Button(self.parent, text="Next phase", command=self.change_phase, image=pixel,
                                        height=20, width=100, compound="c").grid(row=0, column=2)

        self.phase_lbl = tk.Label(self.parent, text=self.game.get_phase, image=pixel, height=20, width=100, compound="c")
        self.phase_lbl.grid(row=0, column=1)

        self.btn1 = RegionButton(root, self.game, "Clyde").grid(row=2, column=0)
        self.btn2 = RegionButton(root, self.game, "Edinburgh").grid(row=2, column=1)
        self.btn3 = RegionButton(root, self.game, "Norwegian Sea").grid(row=2, column=2)
        self.btn4 = RegionButton(root, self.game, "Yorkshire").grid(row=3, column=0)
        self.btn5 = RegionButton(root, self.game, "Liverpool").grid(row=3, column=1)
        self.btn6 = RegionButton(root, self.game, "North Sea").grid(row=3, column=2)

    def change_phase(self):
        if self.game.get_phase == "build":
            self.game.collect_build_orders()
            self.game.game_map.resolve_builds(self.game.order_sheet)
        self.game.next_phase()
        self.phase_lbl.configure(text=self.game.get_phase)

    def get_phase(self):
        return self.game.get_phase

    def print_phase(self):
        print(self.get_phase())

    def print_orders(self):
        print(game.order_sheet)

    def print_board(self):
        self.game.game_map.print_extended_board()


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
            order = CreateUnit(0, self.name)
            self.game.players[0].orders.append(order)
        else:
            self.btn.configure(image=pixel)
            self.army = False

    def move_unit(self):
        pass

    def click_button(self):
        if self.game.get_phase == "build":
            self.create_unit()
        elif self.game.get_phase == "orders":
            self.move_unit()


if __name__ == "__main__":
    root = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)
    army_img = tk.PhotoImage(file=r"army.png")
    game = Game(2)
    App(root, game).grid()
    root.mainloop()
