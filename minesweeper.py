!pip install qiskit --quiet # not needed if running on google

import numpy as np
import math
import qiskit as qk
from qiskit import *
from qiskit.visualization import plot_histogram
from google.colab import widgets
from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual, Button, Layout
import ipywidgets
import pandas as pd
import random
import requests
from IPython.display import clear_output

import qiskit as qk
from qiskit import *
from qiskit.visualization import plot_histogram
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import math
import numpy as np
import random
import requests

class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.board = [[0 for _ in range(width)] for _ in range(height)]
        self.visible_board = [["" for _ in range(width)] for _ in range(height)]
        self.mines = set()
        self.is_game_over = False
    def prep_bell_state(self):
        self.qc = QuantumCircuit(10,10)
        i = 0
        while i < 10:
            if (i%2) == 0:
              self.qc.h(i)
            else:
              self.qc.x(i)
            i += 1
        self.qc.cnot(0,1)
        self.qc.cnot(2,3)
        self.qc.cnot(4,5)
        self.qc.cnot(6,7)
        self.qc.cnot(8,9)
    def place_mines(self, start_x, start_y):
        num_placed = 0
        while num_placed < self.num_mines:
            # Create a quantum circuit with 1 qubit
            circuit = qk.QuantumCircuit(1, 1)
            circuit.h(0)  # Apply a Hadamard gate to create a superposition
            circuit.measure(0, 0)  # Measure the qubit

            # Simulate the circuit to obtain the random bit
            simulator = qk.Aer.get_backend('qasm_simulator')
            result = qk.execute(circuit, simulator, shots=1).result()
            random_bit = int(result.get_counts(circuit).get("1", 0))  # Get the count for outcome '1'

            # Use the random bit to place a mine randomly on the board
            if random_bit:
                x = random.randint(0, self.width - 1)
                y = random.randint(0, self.height - 1)
                if (x, y) != (start_x, start_y) and (x, y) not in self.mines:
                    self.mines.add((x, y))
                    num_placed += 1

    def count_adjacent_mines(self, x, y):
        count = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if (nx, ny) in self.mines:
                        count += 1
        return count

    def reveal(self, x, y):
        if (x, y) in self.mines:
            place = self.mines.index(x, y)
            result = self.qc.measure(place)
            self.visible_board[x][y] = "X"
            if result == 1:
                self.is_game_over = True
            else:
                print("Lucky save! Keep going.")
                self.print_board(show_all=True)

        else:
            count = self.count_adjacent_mines(x, y)
            self.visible_board[x][y] = str(count)
            if count == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.visible_board[nx][ny] == "-":
                                self.reveal(nx, ny)

    def handle_click(self, x, y):
        if not self.is_game_over:
            self.reveal(x, y)
            self.update_board()

            if self.is_game_over:
                self.reveal_mines()
                messagebox.showinfo("Game Over", "You hit a mine! Game Over.")

    def update_board(self):
        for i in range(self.height):
            for j in range(self.width):
                self.buttons[i][j].configure(text=self.visible_board[i][j])

    def create_buttons(self):
        self.buttons = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                button = tk.Button(
                    self.root,
                    text="-",
                    width=4,
                    command=lambda x=i, y=j: self.handle_click(x, y)
                )
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def create_window(self):
        self.root = tk.Tk()
        self.root.title("Minesweeper")
        self.create_buttons()

    def reveal(self, x, y):
        if (x, y) in self.mines:
            place = self.mines.index(x, y)
            result = self.qc.measure(place)
            self.visible_board[x][y] = "X"
            if result == 1:
              self.is_game_over = True
            else:
              print("Lucky save! Keep going.")
              self.print_board(show_all=True)
        else:
            count = self.count_adjacent_mines(x, y)
            self.visible_board[x][y] = str(count)
            if count == 0:
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        nx, ny = x + dx, y + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if self.visible_board[nx][ny] == "-":
                                self.reveal(nx, ny)

    def reveal_mines(self):
        for x, y in self.mines:
            if self.visible_board[x][y] != "X":
                self.visible_board[x][y] = "M"

    def play(self):
        self.create_window()
        start_x = random.randint(0, self.width - 1)
        start_y = random.randint(0, self.height - 1)
        self.place_mines(start_x, start_y)
        tk.mainloop()

# Usage example
width = 8
height = 8
num_mines = 10

game = Minesweeper(width, height, num_mines)
game.play()
