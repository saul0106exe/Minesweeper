import tkinter as tk
import random

class Minesweeper:
    def __init__(self, master):
        self.master = master
        self.width = 10
        self.height = 8
        self.mines = 10

        self.master.title("Minesweeper")

        self.create_widgets()
        self.new_game()

    def create_widgets(self):
        self.board_frame = tk.Frame(self.master)
        self.board_frame.pack()

        self.control_frame = tk.Frame(self.master)
        self.control_frame.pack()

        easy_button = tk.Button(self.control_frame, text="Easy", command=lambda: self.start_new_game(10, 8, 10))
        easy_button.pack(side=tk.LEFT)

        normal_button = tk.Button(self.control_frame, text="Normal", command=lambda: self.start_new_game(18, 14, 40))
        normal_button.pack(side=tk.LEFT)

        hard_button = tk.Button(self.control_frame, text="Hard", command=lambda: self.start_new_game(24, 20, 99))
        hard_button.pack(side=tk.LEFT)

        self.status_label = tk.Label(self.control_frame, text="")
        self.status_label.pack(side=tk.LEFT)

    def start_new_game(self, width, height, mines):
        self.width = width
        self.height = height
        self.mines = mines
        self.new_game()

    def new_game(self):
        self.game_over = False
        self.cells_revealed = 0
        self.status_label.config(text="")

        for widget in self.board_frame.winfo_children():
            widget.destroy()

        self.buttons = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.board = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.cell_state = [['hidden' for _ in range(self.width)] for _ in range(self.height)]

        mines_placed = 0
        while mines_placed < self.mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if self.board[y][x] != 'M':
                self.board[y][x] = 'M'
                mines_placed += 1

        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] != 'M':
                    count = 0
                    for dy in [-1, 0, 1]:
                        for dx in [-1, 0, 1]:
                            if 0 <= x + dx < self.width and 0 <= y + dy < self.height and self.board[y + dy][x + dx] == 'M':
                                count += 1
                    self.board[y][x] = count

        for y in range(self.height):
            for x in range(self.width):
                button = tk.Button(self.board_frame, width=2, height=1, command=lambda x=x, y=y: self.on_click(x, y))
                button.bind("<Button-3>", lambda e, x=x, y=y: self.on_right_click(x, y))
                button.grid(row=y, column=x)
                self.buttons[y][x] = button

    def on_click(self, x, y):
        if self.game_over:
            return

        if self.cell_state[y][x] == 'hidden':
            self.cell_state[y][x] = 'revealed'
            self.buttons[y][x].config(relief=tk.SUNKEN)
            self.cells_revealed += 1

            if self.board[y][x] == 'M':
                self.buttons[y][x].config(text='*', bg='red')
                self.game_over = True
                self.status_label.config(text="Game Over!")
                self.reveal_all_mines()
            elif self.board[y][x] == 0:
                self.buttons[y][x].config(text='')
                self.reveal_neighbors(x, y)
            else:
                self.buttons[y][x].config(text=str(self.board[y][x]))

            self.check_win()

    def on_right_click(self, x, y):
        if self.game_over:
            return

        if self.cell_state[y][x] == 'hidden':
            self.cell_state[y][x] = 'flagged'
            self.buttons[y][x].config(text='F', bg='yellow')
        elif self.cell_state[y][x] == 'flagged':
            self.cell_state[y][x] = 'hidden'
            self.buttons[y][x].config(text='', bg='SystemButtonFace')

    def reveal_neighbors(self, x, y):
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if 0 <= x + dx < self.width and 0 <= y + dy < self.height:
                    self.on_click(x + dx, y + dy)

    def reveal_all_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.board[y][x] == 'M':
                    self.buttons[y][x].config(text='*', bg='red')

    def check_win(self):
        if self.width * self.height - self.cells_revealed == self.mines:
            self.game_over = True
            self.status_label.config(text="You Win!")
            self.reveal_all_mines()

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()
