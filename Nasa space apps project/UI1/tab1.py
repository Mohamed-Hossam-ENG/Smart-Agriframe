import tkinter as tk

from tkinter import ttk

class Tab1_ui(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        parent.add(self, text="Tab 1")
        label = tk.Label(self, text="Welcome to Tab 1!")
        label.pack(pady=10)
