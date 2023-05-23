import tkinter as tk
from tkinter import messagebox

# создаем меню
window = tk.Tk()
window.title("Sudoku Solver")

# цвет фона
window.configure(bg="#99ccff")

# создаем ячейки для судоку
entries = [[tk.Entry(window, width=5, bg="#d9d9d9", fg="black", highlightbackground="black", highlightcolor="black", highlightthickness=2, bd=0, relief=tk.SOLID) for _ in range(9)] for _ in range(9)]
for i in range(9):
    for j in range(9):
        entries[i][j].grid(row=i, column=j, padx=2, pady=2)  # пробелы

# устанавливаем мин сайз
for j in range(9):
    window.grid_columnconfigure(j, minsize=40)

def solve_sudoku():
    # записываем значения
    board = [[int(entries[i][j].get()) if entries[i][j].get() else 0 for j in range(9)] for i in range(9)]

    # проверка на выполнимость судоку
    if is_complete(board):
        messagebox.showinfo("Sudoku Solver", "Sudoku puzzle is already complete!")  # если выполнимо
        return

    # проверка на наличие дубликатов в строках и столбцах
    if has_duplicates(board):
        messagebox.showerror("Sudoku Solver", "Cannot solve the Sudoku puzzle!")
        return

    # решаем
    solved = solve_sudoku_algorithm(board)

    # выводим невозможность выполнения алгоритма
    if solved:
        for i in range(9):
            for j in range(9):
                entries[i][j].delete(0, tk.END)
                entries[i][j].insert(tk.END, board[i][j])
        messagebox.showinfo("Sudoku Solver", "Sudoku puzzle solved successfully!")
    else:
        messagebox.showerror("Sudoku Solver", "Cannot solve the Sudoku puzzle!")


def clear_cells(): #очистка судоку
    for i in range(9):
        for j in range(9):
            entries[i][j].delete(0, tk.END)

def is_complete(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return False
    return True

def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None, None

def is_valid(board, row, col, num):
    # проверяем строки на уникальность
    for c in range(9):
        if c != col and board[row][c] == num:
            return False

    # проверяем в колонне на уникальность
    for r in range(9):
        if r != row and board[r][col] == num:
            return False

    # проверяем 3 на 3 квадраты
    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for r in range(start_row, start_row + 3):
        for c in range(start_col, start_col + 3):
            if (r != row or c != col) and board[r][c] == num:
                return False

    # проверка пересечений
    for r in range(9):
        if r != row and board[r][col] == num:
            return False
    for c in range(9):
        if c != col and board[row][c] == num:
            return False

    return True

def has_duplicates(board):
    # Проверка дубликатов в строках
    for row in range(9):
        seen = set()
        for col in range(9):
            num = board[row][col]
            if num != 0:
                if num in seen:
                    return True
                seen.add(num)

    # Проверка дубликатов в столбцах
    for col in range(9):
        seen = set()
        for row in range(9):
            num = board[row][col]
            if num != 0:
                if num in seen:
                    return True
                seen.add(num)

    return False

def solve_sudoku_algorithm(board):
    row, col = find_empty_cell(board)
    if row is None and col is None:
        return True

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num
            if solve_sudoku_algorithm(board):
                return True
            board[row][col] = 0

    return False

# создаем кнопку решения
solve_button = tk.Button(window, text="Solve", command=solve_sudoku, bg="green", highlightbackground="#99ccff", highlightcolor="#99ccff", highlightthickness=2, bd=0, relief=tk.SOLID)
solve_button.grid(row=9, column=4, columnspan=1, sticky="nsew")  # Use sticky="nsew" for the solve button

# создаем кнопку очистки
clear_button = tk.Button(window, text="Clear", command=clear_cells, bg="green", highlightbackground="#99ccff", highlightcolor="#99ccff", highlightthickness=2, bd=0, relief=tk.SOLID)
clear_button.grid(row=9, column=8, columnspan=1, sticky="nsew")  # Use sticky="nsew" for the clear button

for i in range(9):
    window.grid_rowconfigure(i, weight=1)

# запуск
window.mainloop()
