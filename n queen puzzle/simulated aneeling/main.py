import tkinter as tk
from tkinter import Button, Entry, Frame, Label
import random
import math
import time

def objective_function(state):
    """Calculate the number of pairs of attacking queens (queens that attack each other)."""
    n = len(state)
    attacks = 0

    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                attacks += 1

    return attacks

def simulated_annealing(n_queens, schedule, initialState):
    """Solve the N-Queens problem using simulated annealing."""
    state = initialState
    start_time = time.time()  # Start measuring time

    current_attacks = objective_function(state)
    best_state = state
    best_attacks = current_attacks

    for temperature in schedule:
        new_state = state.copy()
        i, j = random.sample(range(n_queens), 2)
        new_state[i], new_state[j] = new_state[j], new_state[i]
        new_attacks = objective_function(new_state)

        if new_attacks < best_attacks:
            best_state = new_state
            best_attacks = new_attacks

        if new_attacks < current_attacks or random.random() < math.exp(-(new_attacks - current_attacks) / temperature):
            state = new_state
            current_attacks = new_attacks

    end_time = time.time()  # Stop measuring time

    print("Time taken:", end_time - start_time, "seconds")

    return best_state

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
        max_iterations = 10000
        initial_temperature = 2.0
        cooling_rate = 0.95  # Corrected cooling rate value
        temperature = initial_temperature
        schedule = []

        for _ in range(max_iterations):
            schedule.append(temperature)
            temperature *= cooling_rate

        solution = simulated_annealing(n_queens, schedule, initial_state)

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
