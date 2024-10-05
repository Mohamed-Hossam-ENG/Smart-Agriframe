import tkinter as tk

from tkinter import ttk

class Tab2_ui(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.add(self, text="Tab 2")
        label = tk.Label(self, text="This is Tab 2.")
        label.pack(pady=10)
