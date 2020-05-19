import tkinter as tk


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title("Diplomacy")

        self.next_phase_btn = tk.Button(self.parent, text="Next phase", command=self.change_phase, image=pixel, height=20,
                                   width=100, compound="c").grid(row=0, column=2)
        self.phase_lbl = tk.Label(self.parent, text="Build", image=pixel, height=20, width=100, compound="c")
        self.phase_lbl.grid(row=0, column=1)
        self.btn1 = tk.Button(self.parent, text="Clyde", command=lambda row=1, column=0 : self.create_unit(row, column),
                              anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=1, column=0)
        self.btn2 = tk.Button(self.parent, text="Edinburgh", command=lambda row=1, column=1 : self.create_unit(row, column),
                              anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=1, column=1)
        self.btn3 = tk.Button(self.parent, text="Yorkshire", command=lambda row=2, column=0 : self.create_unit(row, column),
                              anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=2, column=0)
        self.btn4 = tk.Button(self.parent, text="Liverpool", command=lambda row=2, column=1 : self.create_unit(row, column),
                              anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=2, column=1)
        self.btn5 = tk.Button(self.parent, text="Norwegian Sea", command=lambda row=1, column=2 : self.create_unit(row, column),
                              anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=1, column=2)
        self.btn6 = tk.Button(self.parent, text="North Sea", command=lambda row=2, column=2 : self.create_unit(row, column),
                              anchor="n", image=pixel, height=100, width=100, compound="c").grid(row=2, column=2)

    def create_unit(self, r, c):
        widget = self.parent.grid_slaves(row=r, column=c)[0]
        widget.configure(image=army_img)

    def change_phase(self):
        self.phase_lbl.configure(text="Orders")


if __name__ == "__main__":
    root = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)
    army_img = tk.PhotoImage(file=r"C:\Users\charl\Desktop\army.png")
    App(root).grid()
    root.mainloop()
