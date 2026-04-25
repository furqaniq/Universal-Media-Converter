"""Entry point for the Universal Media Converter desktop application."""

import sys
import os
import tkinter as tk

# Monkey-patch tkinter.Tk to use TkinterDnD BEFORE customtkinter imports it
from tkinterdnd2 import TkinterDnD
tk.Tk = TkinterDnD.Tk

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.app import App


def main():
    app = App()
    app.run()


if __name__ == "__main__":
    main()
