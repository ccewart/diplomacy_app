import tkinter as tk


class App:
    def __init__(self, master):
        self.master = master
        self.create_board()

    def create_board(self):
        pixel = tk.PhotoImage(width=1, height=1)
        phase_btn = tk.Label(self.master, text="Build", image=pixel, height=20, width=100, compound="c").grid(row=0,
                                                                                                           column=1)
        btn1 = tk.Button(self.master, text="Clyde", anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=1,
                                                                                                           column=0)
        btn2 = tk.Button(self.master, text="Edinburgh", anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=1,
                                                                                                               column=1)
        btn3 = tk.Button(self.master, text="Yorkshire", anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=2,
                                                                                                               column=0)
        btn4 = tk.Button(self.master, text="Liverpool", anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=2,
                                                                                                               column=1)
        btn5 = tk.Button(self.master, text="Norwegian Sea", anchor="n", image=pixel, height=100, width=100, compound="c").grid(
            row=1, column=2)
        btn6 = tk.Button(self.master, text="North Sea", anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=2,
                                                                                                               column=2)


root = tk.Tk()
root.title("Diplomacy")
app = App(root)
root.mainloop()
