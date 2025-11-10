import tkinter as tk
from game import MinesweeperGUI

if __name__ == "__main__":
    root = tk.Tk()
    root.minsize(300, 200)
    root.title("Minesweeper")
    game_gui = MinesweeperGUI(root)
    root.mainloop()