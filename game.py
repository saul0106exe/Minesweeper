import tkinter as tk
import random
from tkinter import messagebox
from config import DIFFICULTY, COLORS, FONT_BUTTON, FONT_LABEL, MINE_CHAR, FLAG_CHAR, MINES_COUNTER_CHAR

class MinesweeperGUI:
    def __init__(self, master):
        self.master = master
        self.master.config(bg="#f0f0f0")
        
        self.difficulty = "easy"
        self.width = DIFFICULTY[self.difficulty]["size"][0]
        self.height = DIFFICULTY[self.difficulty]["size"][1]
        self.mines = DIFFICULTY[self.difficulty]["mines"]

        self.board_frame = tk.Frame(self.master, bd=2, relief=tk.SUNKEN)
        self.board_frame.pack(padx=10, pady=10)

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.control_frame = tk.Frame(self.master, bg="#f0f0f0", pady=5)
        self.control_frame.pack(fill=tk.X)

        for level, settings in DIFFICULTY.items():
            btn = tk.Button(
                self.control_frame,
                text=level.capitalize(),
                font=FONT_BUTTON,
                command=lambda l=level: self.start_new_game(difficulty=l)
            )
            btn.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(self.control_frame, text="", font=FONT_LABEL, bg="#f0f0f0")
        self.status_label.pack(side=tk.RIGHT, padx=10)
    
    def start_new_game(self, difficulty="easy"):
        self.difficulty = difficulty
        self.width = DIFFICULTY[difficulty]["size"][0]
        self.height = DIFFICULTY[difficulty]["size"][1]
        self.mines = DIFFICULTY[difficulty]["mines"]
        self.master.resizable(True, True) 
        self.new_game()
        self.master.update_idletasks() 
        self.master.resizable(False, False) 

    def new_game(self):
        self.game_over = False
        self.cells_revealed = 0
        self.first_click = True
        self.status_label.config(text="")

        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.cell_state = [['hidden' for _ in range(self.width)] for _ in range(self.height)]

        self._create_board_buttons()

    def _place_mines(self, first_x, first_y):
        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != "M" and not (abs(x - first_x) <= 1 and abs(y - first_y) <= 1):
                self.board[y][x] = "M"
                mines_placed += 1

    def _calculate_numbers(self, first_x, first_y):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == "M":
                    continue
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height and self.board[ny][nx] == "M":
                            count += 1
                self.board[y][x] = count

    def _create_board_buttons(self):
        for y in range(self.height):
            for x in range(self.width):
                button = tk.Button(
                    self.board_frame,
                    width=3, height=1,
                    font=FONT_BUTTON,
                    bg=COLORS["button_bg"],
                    command=lambda x=x, y=y: self.on_click(x, y)
                )
                button.bind("<Button-3>", lambda e, x=x, y=y: self.on_right_click(x, y))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def on_click(self, x, y):
        if self.first_click:
            self.first_click = False
            self._place_mines(x, y)
            self._calculate_numbers(x, y)
            self._update_all_button_text()

        if self.game_over or self.cell_state[y][x] != 'hidden':
            return

        self.cell_state[y][x] = 'revealed'
        self.buttons[y][x].config(relief=tk.SUNKEN, bg=COLORS["revealed_bg"])
        self.cells_revealed += 1

        if self.board[y][x] == "M":
            self.buttons[y][x].config(text=MINE_CHAR, bg=COLORS["mine_bg"], fg="white")
            self.end_game(won=False)
        else:
            if self.board[y][x] > 0:
                num = self.board[y][x]
                self.buttons[y][x].config(text=str(num), fg=COLORS["number_colors"].get(num, "black"))
            else:
                self.reveal_neighbors(x, y)
            self.check_win()

    def _update_all_button_text(self):
        pass

    def on_right_click(self, x, y):
        if self.game_over or self.cell_state[y][x] == 'revealed':
            return

        if self.cell_state[y][x] == 'hidden':
            self.cell_state[y][x] = 'flagged'
            self.buttons[y][x].config(text=FLAG_CHAR, bg=COLORS["flag_bg"], fg="black")
        elif self.cell_state[y][x] == 'flagged':
            self.cell_state[y][x] = 'hidden'
            self.buttons[y][x].config(text='', bg=COLORS["button_bg"])

    def reveal_neighbors(self, x, y):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    self.on_click(nx, ny)

    def reveal_all_mines(self, won=False):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == "M":
                    if self.cell_state[y][x] != 'flagged':
                        bg_color = COLORS["mine_bg"] if not won else COLORS["button_bg"]
                        self.buttons[y][x].config(text=MINE_CHAR, bg=bg_color, relief=tk.SUNKEN)

    def check_win(self):
        if self.width * self.height - self.cells_revealed == self.mines:
            self.game_over = True
            self.end_game(won=True)

    def end_game(self, won):
        if self.game_over:
            return
        self.game_over = True
        self.reveal_all_mines(won)
        if won:
            self.status_label.config(text="You Win!")
            messagebox.showinfo("Minesweeper", "Congratulations, You Win!")
        else:
            self.status_label.config(text="Game Over!")
            messagebox.showerror("Minesweeper", "Game Over!")
