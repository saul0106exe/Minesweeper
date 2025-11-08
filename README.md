# Minesweeper 💣

A classic implementation of the Minesweeper game built with Python and the standard `tkinter` library.

This project is a simple, self-contained desktop application that mimics the logic and core gameplay of the original Windows Minesweeper.

## ✨ Features

Based on the provided code, this game includes:

* **10x10 Grid:** A standard 10x10 board for gameplay.
* **10 Mines:** The board is randomly populated with 10 mines on every new game.
* **Left-Click:** Reveals a cell.
    * If you click a mine, the game ends, and all mines are revealed.
    * If you click a numbered cell, the number (count of adjacent mines) is displayed.
    * If you click an empty cell (0 adjacent mines), it automatically reveals all adjacent empty cells (a "flood fill").
* **Right-Click:** Toggles a flag on and off. This allows you to mark suspected mine locations.
* **"New Game" Button:** A button to reset the board and start a new game at any time.
* **Win/Loss Status:** A label updates to "Game Over!" or "You Win!" to inform you of the game's state.

## 📋 Requirements

* **Python 3.x**
* **`tkinter` library:** This library is included by default with most Python installations, so you typically do not need to install anything extra.

## 🚀 How to Run

1.  **Save the Code:** Save all the provided code snippets into a single Python file (e.g., `game.py`).
2.  **Open your Terminal:** Open a command prompt or terminal window.
3.  **Navigate to the File:** Use the `cd` command to move into the directory where you saved the file.
    ```bash
    cd path/to/your/project
    ```
4.  **Run the Game:** Execute the Python script.
    ```bash
    python game.py
    ```
    The game window should pop up and be ready to play.

## 🎮 How to Play

* **Objective:** The goal is to reveal all cells on the board that do **not** contain a mine.
* **Left-Click** a cell to reveal what's underneath.
* **Right-Click** a cell to place a flag (🚩) where you suspect a mine is. Right-click again to remove the flag.
* **Numbers:** A number on a cell indicates the exact number of mines in the 8 cells immediately surrounding it.
* **You Win** when you have revealed all cells except for the 10 mines.
* **You Lose** if you click on a mine.
* Click the **"New Game"** button to try again!
