import tkinter as tk
from tkinter import filedialog


last_cell = None


def make_blocked(event):
    global last_cell
    x = event.x // square_size
    y = event.y // square_size
    if (x, y) != last_cell:
        if map_grid[y][x] is None:
            map_grid[y][x] = canvas.create_rectangle(x * square_size, y * square_size,
                                                     (x + 1) * square_size, (y + 1) * square_size, fill='white', outline='black')
        else:
            current_color = canvas.itemcget(map_grid[y][x], "fill")
            new_color = 'black' if current_color == 'white' else 'white'
            canvas.itemconfig(map_grid[y][x], fill=new_color)
        last_cell = (x, y)


def load_map():
    file_path = filedialog.askopenfilename(filetypes=[('Text Files', '*.txt')])
    if file_path:
        with open(file_path, 'r') as file:
            # Load map from file and update the grid
            pass


def save_map():
    file_path = filedialog.asksaveasfilename(
        defaultextension='.txt', filetypes=[('Text Files', '*.txt')])
    if file_path:
        with open(file_path, 'w') as file:
            # Save the current map to the file
            pass


def update_rows(val):
    global m, square_size, map_grid
    m = int(val)
    square_size = 900 // max(m, n)
    map_grid = [[None for _ in range(n)] for _ in range(m)]
    canvas.delete('all')
    for i in range(m):
        for j in range(n):
            map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                     (j + 1) * square_size, (i + 1) * square_size, fill='white', outline='black')


def update_columns(val):
    global n, square_size, map_grid
    n = int(val)
    square_size = 900 // max(m, n)
    map_grid = [[None for _ in range(n)] for _ in range(m)]
    canvas.delete('all')
    for i in range(m):
        for j in range(n):
            map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                     (j + 1) * square_size, (i + 1) * square_size, fill='white', outline='black')


def update_both():
    global m, n, square_size, map_grid
    m = rows_slider.get()
    n = columns_slider.get()
    square_size = 900 // max(m, n)
    map_grid = [[None for _ in range(n)] for _ in range(m)]
    canvas.delete('all')
    for i in range(m):
        for j in range(n):
            map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                     (j + 1) * square_size, (i + 1) * square_size, fill='white', outline='black')


root = tk.Tk()
root.title("Map Editor")

# Create canvas for the grid
canvas = tk.Canvas(root, width=900, height=900, bg='white')
canvas.pack(side=tk.LEFT)

# Create frame for file dialogs
frame = tk.Frame(root)
frame.pack(side=tk.RIGHT, padx=10)

# Create buttons for loading and saving map
load_button = tk.Button(frame, text="Load Map", command=load_map)
load_button.pack(pady=10)

save_button = tk.Button(frame, text="Save Map", command=save_map)
save_button.pack(pady=10)

# Create sliders for changing number of rows and columns
rows_slider = tk.Scale(frame, from_=5, to=100,
                       orient=tk.HORIZONTAL, command=update_rows)
rows_slider.set(20)
rows_slider.pack(pady=10)

columns_slider = tk.Scale(frame, from_=5, to=100,
                          orient=tk.HORIZONTAL, command=update_columns)
columns_slider.set(20)
columns_slider.pack(pady=10)

# Set the size of each square in the grid
m = n = 20  # Number of rows and columns
square_size = 900 // max(m, n)

map_grid = [[None for _ in range(n)] for _ in range(m)]


def make_blocked(event):
    global last_cell
    x = event.x // square_size
    y = event.y // square_size
    if (x, y) != last_cell:
        if map_grid[y][x] is None:
            map_grid[y][x] = canvas.create_rectangle(x * square_size, y * square_size,
                                                     (x + 1) * square_size, (y + 1) * square_size, fill='white', outline='black')
        canvas.itemconfig(map_grid[y][x], fill='black')
        last_cell = (x, y)


def make_empty(event):
    global last_cell
    x = event.x // square_size
    y = event.y // square_size
    if (x, y) != last_cell:
        if map_grid[y][x] is None:
            map_grid[y][x] = canvas.create_rectangle(x * square_size, y * square_size,
                                                     (x + 1) * square_size, (y + 1) * square_size, fill='white', outline='black')
        canvas.itemconfig(map_grid[y][x], fill='white')
        last_cell = (x, y)


canvas.bind('<Button-1>', make_blocked)
canvas.bind('<B1-Motion>', make_blocked)
canvas.bind('<Button-3>', make_empty)
canvas.bind('<B3-Motion>', make_empty)

root.mainloop()
