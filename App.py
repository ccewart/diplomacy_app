import tkinter as tk
from Game import *
from Orders import Order, CreateUnit, Move


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

        self.current_order = None

        self.print_phase_btn = tk.Button(self.parent, text="Print phase", command=self.print_phase, image=pixel,
                                         height=20, width=100, compound="c").grid(row=0, column=0)
        self.next_phase_btn = tk.Button(self.parent, text="Next phase", command=self.change_phase, image=pixel,
                                        height=20, width=100, compound="c").grid(row=0, column=2)
        self.print_orders_btn = tk.Button(self.parent, text="Print orders", command=self.print_orders, image=pixel,
                                          height=20, width=100, compound="c").grid(row=1, column=0)
        self.print_board_btn = tk.Button(self.parent, text="Print board", command=self.print_board, image=pixel,
                                         height=20, width=100, compound="c").grid(row=1, column=1)
        self.print_units_btn = tk.Button(self.parent, text="Print units", command=self.print_units, image=pixel,
                                         height=20, width=100, compound="c").grid(row=1, column=2)
        self.print_results_btn = tk.Button(self.parent, text="Print results", command=self.print_results, image=pixel,
                                           height=20, width=100, compound="c").grid(row=2, column=0)
        self.reset_results_btn = tk.Button(self.parent, text="Reset results", command=self.reset_results, image=pixel,
                                           height=20, width=100, compound="c").grid(row=2, column=1)


        self.phase_lbl = tk.Label(self.parent, text=self.game.get_phase, image=pixel, height=20, width=100, compound="c")
        self.phase_lbl.grid(row=0, column=1)

        self.btn1 = RegionButton(root, self.game, self.current_order, "Clyde").grid(row=3, column=0)
        self.btn2 = RegionButton(root, self.game, self.current_order, "Edinburgh").grid(row=3, column=1)
        self.btn3 = RegionButton(root, self.game, self.current_order, "Norwegian Sea").grid(row=3, column=2)
        self.btn4 = RegionButton(root, self.game, self.current_order, "Yorkshire").grid(row=4, column=0)
        self.btn5 = RegionButton(root, self.game, self.current_order, "Liverpool").grid(row=4, column=1)
        self.btn6 = RegionButton(root, self.game, self.current_order, "North Sea").grid(row=4, column=2)

    def change_phase(self):
        if self.game.get_phase == "build":
            self.game.collect_build_orders()
            self.game.game_map.resolve_builds(self.game.order_sheet)
            self.game.collect_results()
            self.game.game_map.reset_results()
            self.game.reset_order_sheet()
        if self.game.get_phase == "orders":
            pass
        self.game.next_phase()
        self.phase_lbl.configure(text=self.game.get_phase)

    def get_phase(self):
        return self.game.get_phase

    def print_phase(self):
        print(self.get_phase())

    def print_orders(self):
        print(self.game.order_sheet)
        for order in self.game.order_sheet:
            print(order.details())

    def print_board(self):
        self.game.game_map.print_extended_board()

    def print_units(self):
        for player in self.game.players:
            print(player.units)

    def print_results(self):
        print(self.game.game_map.results)

    def reset_results(self):
        self.game.game_map.reset_results()

class RegionButton(tk.Frame):
    def __init__(self, parent, game, current_order, name, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.game = game
        self.name = name
        self.army = False

        self.current_order = current_order

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

    def move_unit(self, name):
        print("current order:", self.current_order)
        if self.current_order is None:
            print("moving from:", self.name)
            self.current_order = Move(0, self.name)
        elif self.current_order.to is None:
            print("to:", self.name)
            self.current_order.to = self.name
            self.game.players[0].orders.append(self.current_order)
            self.current_order = None

    def click_button(self):
        if self.game.get_phase == "build":
            self.create_unit()
        elif self.game.get_phase == "orders":
            self.move_unit(self.name)


if __name__ == "__main__":
    root = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)
    army_img = tk.PhotoImage(file=r"army.png")
    game = Game(2)
    App(root, game).grid()
    root.mainloop()
