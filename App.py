import tkinter as tk


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        parent.title("Diplomacy")

        self.phase_btn = tk.Button(self.parent, text="Next phase", command=self.change_phase, image=pixel, height=20,
                                   width=100, compound="c").grid(row=0, column=2)
        self.phase_lbl = tk.Label(self.parent, text="Build", image=pixel, height=20, width=100, compound="c").grid(
            row=0, column=1)
        self.btn1 = tk.Button(self.parent, text="Clyde", anchor="n", image=pixel, height=100, width=100,
                              compound="c").grid(row=1, column=0)
        self.btn2 = tk.Button(self.parent, text="Edinburgh", anchor="n", image=pixel, height=100, width=100,
                              compound="c").grid(row=1, column=1)
        self.btn3 = tk.Button(self.parent, text="Yorkshire", anchor="n", image=pixel, height=100, width=100,
                              compound="c").grid(row=2, column=0)
        self.btn4 = tk.Button(self.parent, text="Liverpool", anchor="n", image=pixel, height=100, width=100,
                              compound="c").grid(row=2, column=1)
        self.btn5 = tk.Button(self.parent, text="Norwegian Sea", anchor="n", image=pixel, height=100, width=100,
                              compound="c").grid(row=1, column=2)
        self.btn6 = tk.Button(self.parent, text="North Sea", anchor="n", image=pixel, height=100, width=100,
                              compound="c").grid(row=2, column=2)

    def change_phase(self):
        self.phase_lbl = tk.Label(self.parent, text="Orders", image=pixel, height=20, width=100, compound="c").grid(
            row=0,
            column=1)


if __name__ == "__main__":
    root = tk.Tk()
    pixel = tk.PhotoImage(width=1, height=1)
    App(root).grid()
    root.mainloop()
