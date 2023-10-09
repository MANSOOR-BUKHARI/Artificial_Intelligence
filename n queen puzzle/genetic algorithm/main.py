import tkinter as tk
from tkinter import Button, Entry, Frame, Label
import numpy as np
import random

def objective_function(board):
    """Calculate the number of pairs of attacking queens (queens that attack each other)."""
    n = len(board)
    attacks = 0

    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == j - i:
                attacks += 1

    return attacks

def initialize_population(population_size, n):
    """Initialize a population of board configurations."""
    population = [list(np.random.permutation(n)) for _ in range(population_size)]
    return population

def select_parents(population, fitness_scores):
    """Select two parents from the population based on fitness scores."""
    idx1, idx2 = np.random.choice(len(population), 2, replace=False, p=[s / sum(fitness_scores) for s in fitness_scores])
    return population[idx1], population[idx2]

def crossover(parent1, parent2):
    """Perform one-point crossover to create two offspring from two parents."""
    n = len(parent1)
    crossover_point = random.randint(1, n - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    return offspring1, offspring2

def mutate(board):
    """Randomly swap two positions in the board configuration."""
    n = len(board)
    idx1, idx2 = random.sample(range(n), 2)
    board[idx1], board[idx2] = board[idx2], board[idx1]

def genetic_algorithm(n, population_size, max_generations):
    population = initialize_population(population_size, n)
    for generation in range(max_generations):
        fitness_scores = [1 / (1 + objective_function(board)) for board in population]
        new_population = []

        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitness_scores)
            offspring1, offspring2 = crossover(parent1, parent2)
            mutate(offspring1)
            mutate(offspring2)
            new_population.extend([offspring1, offspring2])

        population = new_population

        best_board = min(population, key=lambda x: objective_function(x))
        if objective_function(best_board) == 0:
            return best_board

    return None  # No solution found within the maximum number of generations


def create_chessboard(root, n_queens, solution):
    chessboard_frame = Frame(root)
    chessboard_frame.pack()

    for row in range(n_queens):
        for col in range(n_queens):
            color = "black" if (row + col) % 2 == 0 else "white"
            button_text = "♛" if solution[col] == row else ""
            button = Button(chessboard_frame, text=button_text, fg="red", width=2, height=1, bg=color)
            button.grid(row=row, column=col, padx=1, pady=1)

def solve():
    try:
        n_queens = int(num_queens_entry.get())
        result_label3.config(text=f"")       
        initial_state = list(map(int, initial_positions_entry.get().split()))
        if len(initial_state) != n_queens:
            initial_state = list(range(n_queens))

        # Clear any existing chessboard frames
        for widget in frame3.winfo_children():
            widget.destroy()

        # Create a frame for the initial board
        frame3_left = Frame(frame3)
        frame3_left.grid(row=0, column=0, padx=10, pady=10)

        # Display a message indicating it's the initial board
        initial_message = Label(frame3_left, text="Initial Board", font=("Helvetica", 16))
        initial_message.pack()

        create_chessboard(frame3_left, n_queens, initial_state)

        # Define the annealing schedule (decreasing temperature)
        # Define the genetic algorithm parameters
        population_size = 100
        max_generations = 1000

        # Solve the N-Queens problem using a Genetic Algorithm
        solution = genetic_algorithm(n_queens, population_size, max_generations)

        # Create a frame for the final board
        frame3_right = Frame(frame3)
        frame3_right.grid(row=0, column=1, padx=10, pady=10)

        # Display a message indicating it's the optimal solution
        optimal_message = Label(frame3_right, text="Optimal Solution", font=("Helvetica", 16))
        optimal_message.pack()

        # Create and display the final chessboard
        create_chessboard(frame3_right, n_queens, solution)
        result_label3.config(text=f"")
    except Exception as e:
        result_label3.config(text=f"Error: {str(e)}")

# Create the main application window
tk = tk.Tk()
tk.title("n-Queen Solver")
tk.geometry('1500x1500')
frame = Frame(tk)
frame.pack()

label = Label(frame, text="N- Queen Solver", font=('Arial', 10, 'bold'))
label.pack()

frame1 = Frame(tk)
frame1.pack()

label1 = Label(frame1, bg='black', fg='white', borderwidth=5, text="Enter Number of Queens:", font=('Arial', 8, 'bold'), width=20)
label1.grid(column=0, row=0, padx=5, pady=2)

num_queens_entry = Entry(frame1, fg='black', bg='white', width=22, borderwidth=5, font=('Arial', 8, 'bold'))
num_queens_entry.grid(row=0, column=1, padx=5, pady=2)

label2 = Label(frame1, bg='black', fg='white', borderwidth=5, text="Enter initial Positions(Opt):", font=('Arial', 8, 'bold'), width=20)
label2.grid(column=0, row=1, padx=5, pady=2)

initial_positions_entry = Entry(frame1, width=22, font=('Arial', 8, 'bold'), borderwidth=5, fg='black', bg='white')
initial_positions_entry.grid(row=1, column=1, padx=5, pady=2)

frame2 = Frame(tk)
frame2.pack()

solve_button = Button(frame2, bg='black', fg='red', width=37, borderwidth=5, text="Submit",
                   font=("Helvetica", 10,'bold'),command=solve)
solve_button.grid(row=0, column=0,columnspan=1)
# Bind the button's hover event to change its text to "Submit" when hovered
def on_hover(event):
    solve_button.config(text="Submit")
    solve_button['bg'] = 'black'
    solve_button['fg'] = 'white'


def on_leave(event):
    solve_button['bg'] = 'white'
    solve_button['fg'] = 'black'

solve_button.bind("<Enter>", on_hover)
solve_button.bind("<Leave>", on_leave)



#frame 3 
# Create a frame for displaying both boards side by side
frame3 = Frame(tk)
frame3.pack()

result_label3 = Label(tk, text="", font=("Helvetica", 16))
result_label3.pack()

tk.mainloop()
