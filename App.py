import tkinter as tk
from Game import *
from Orders import Order, CreateUnit, Move


class App(tk.Frame):
    def __init__(self, parent, game, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title("Diplomacy")
        self.coords = {"Clyde": (100, 100),
                       "Edinburgh": (250, 100),
                       "Norwegian Sea": (400, 100),
                       "Yorkshire": (100, 250),
                       "Liverpool": (250, 250),
                       "North Sea": (400, 250)}

        self.game = game
        self.game.next_phase()
        self.game.next_phase()
        self.game.next_phase()
        self.game.next_phase()

        self.canvas = tk.Canvas(self, width=400, height=350)

        #canvas.create_oval(10, 10, 80, 80, outline="#f11", fill="#1f1", width=2)

        self.print_move_orders = tk.Button(self.parent, text="Print move orders", command=self.print_move_orders, image=pixel,
                                           height=20, width=100, compound="c").grid(row=0, column=0)
        self.next_phase_btn = tk.Button(self.parent, text="Next phase", command=self.change_phase, image=pixel,
                                        height=20, width=100, compound="c").grid(row=0, column=2)
        self.print_orders_btn = tk.Button(self.parent, text="Print orders", command=self.print_orders, image=pixel,
                                          height=20, width=100, compound="c").grid(row=1, column=0)
        self.print_board_btn = tk.Button(self.parent, text="Print board", command=self.print_board, image=pixel,
                                         height=20, width=100, compound="c").grid(row=1, column=1)
        self.print_units_btn = tk.Button(self.parent, text="Print units", command=self.print_units, image=pixel,
                                         height=20, width=100, compound="c").grid(row=1, column=2)

        self.phase_lbl = tk.Label(self.parent, text=self.game.get_phase, image=pixel, height=20, width=100, compound="c")
        self.phase_lbl.grid(row=0, column=1)

        self.btn1 = RegionButton(root, self.game, "Clyde", self)
        self.btn2 = RegionButton(root, self.game, "Edinburgh", self)
        self.btn3 = RegionButton(root, self.game, "Norwegian Sea", self)
        self.btn4 = RegionButton(root, self.game, "Yorkshire", self)
        self.btn5 = RegionButton(root, self.game, "Liverpool", self)
        self.btn6 = RegionButton(root, self.game, "North Sea", self)

        self.buttons = [self.btn1, self.btn2, self.btn3, self.btn4, self.btn5, self.btn6]

        self.window1 = self.canvas.create_window(100, 100, window=self.btn1)
        self.window2 = self.canvas.create_window(250, 100, window=self.btn2)
        self.window3 = self.canvas.create_window(400, 100, window=self.btn3)
        self.window4 = self.canvas.create_window(100, 250, window=self.btn4)
        self.window5 = self.canvas.create_window(250, 250, window=self.btn5)
        self.window6 = self.canvas.create_window(400, 250, window=self.btn6)

        #oval1 = self.canvas.create_oval(25, 25, 175, 175, outline="#f11", fill="#1f1", width=2)
        #oval2 = self.canvas.create_oval(50, 50, 200, 200, outline="#f11", fill="OrangeRed2", width=2)

        self.canvas.pack()

    def draw_line(self, order):
        x0, y0 = self.coords[order.region]
        x1, y1 = self.coords[order.to]
        line = self.canvas.create_line(x0, y0, x1, y1, fill="OrangeRed2", width=5)
        self.canvas.tag_raise(line)
        self.canvas.tag_lower(self.window1)

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

    def print_move_orders(self):
        for player in self.game.players:
            for unit in player.units:
                print(unit.orders)


class RegionButton(tk.Frame):
    def __init__(self, parent, game, name, app, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.game = game
        self.name = name
        self.app = app
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
            self.app.draw_line(current_order)
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
