import tkinter as tk


class PageOne(tk.Frame):
    def __init__(self, parent, switch_to_page_one):
        super().__init__(parent)
        self.parent = parent