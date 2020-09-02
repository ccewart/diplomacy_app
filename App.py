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
        self.print_move_orders = tk.Button(self.parent, text="Print move orders", command=self.print_move_orders, image=pixel,
                                           height=20, width=100, compound="c").grid(row=2, column=1)
        self.reset_results_btn = tk.Button(self.parent, text="Reset results", command=self.reset_results, image=pixel,
                                           height=20, width=100, compound="c").grid(row=2, column=2)

        self.phase_lbl = tk.Label(self.parent, text=self.game.get_phase, image=pixel, height=20, width=100, compound="c")
        self.phase_lbl.grid(row=0, column=1)

        self.btn1 = RegionButton(root, self.game, "Clyde")
        self.btn1.grid(row=3, column=0)
        self.btn2 = RegionButton(root, self.game, "Edinburgh")
        self.btn2.grid(row=3, column=1)
        self.btn3 = RegionButton(root, self.game, "Norwegian Sea")
        self.btn3.grid(row=3, column=2)
        self.btn4 = RegionButton(root, self.game, "Yorkshire")
        self.btn4.grid(row=4, column=0)
        self.btn5 = RegionButton(root, self.game, "Liverpool")
        self.btn5.grid(row=4, column=1)
        self.btn6 = RegionButton(root, self.game, "North Sea")
        self.btn6.grid(row=4, column=2)
        self.buttons = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6]

    def change_phase(self):
        if self.game.get_phase == "build":
            self.game.collect_build_orders()
            self.game.game_map.resolve_builds(self.game.order_sheet)
            self.game.collect_results()
            self.game.game_map.reset_results()
            self.game.reset_order_sheet()
        if self.game.get_phase == "orders":
            self.game.game_map.resolve_orders(game.players)
            self.update_region_buttons()
            self.game.reset_order_sheet()
        self.game.next_phase()
        self.phase_lbl.configure(text=self.game.get_phase)

    def update_region_buttons(self):
        for region_button in self.buttons:
            region_button.update_unit_image()

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

    def print_move_orders(self):
        for player in self.game.players:
            for unit in player.units:
                print(unit.orders)

    def reset_results(self):
        self.game.game_map.reset_results()


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

    def update_unit_image(self):
        if game.game_map.regions[self.name].unit is not None:
            self.btn.configure(image=army_img)
        else:
            self.btn.configure(image=pixel)

    def move_unit(self, name):
        global current_order
        if current_order is None:
            current_order = Move(0, self.name)
            print("moving from:", self.name)
        elif current_order.to is None:
            print("moving to:", self.name)
            current_order.to = self.name
            self.give_order_to_unit(current_order)
            current_order = None

    def give_order_to_unit(self, order):
        for player in self.game.players:
            for unit in player.units:
                if unit.region == order.region:
                    unit.orders = order

    def click_button(self):
        if self.game.get_phase == "build":
            self.create_unit()
        elif self.game.get_phase == "orders":
            self.move_unit(self.name)


if __name__ == "__main__":
    root = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)
    army_img = tk.PhotoImage(file=r"army.png")
    current_order = None
    game = Game(2)
    App(root, game).grid()
    root.mainloop()
