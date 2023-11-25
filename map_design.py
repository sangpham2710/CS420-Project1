import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.title("Map Editor")
# Create canvas for the grid
canvas = tk.Canvas(root, width=900, height=900, bg='white')
canvas.pack(side=tk.LEFT)
# Create frame for file dialogs
frame = tk.Frame(root)
frame.pack(side=tk.RIGHT, padx=10)

# Set the size of each square in the grid
m = n = 20  # Number of rows and columns
square_size = 900 // max(m, n)

map_grid = [[None for _ in range(n)] for _ in range(m)]
map_text = [[None for _ in range(n)] for _ in range(m)]

color_dict = {'D': 'brown', 'K': 'yellow', 'UP': 'gray', 'DO': 'gray',
              'A': 'red', 'T': 'green'}

char_dict = {'brown': 'D', 'yellow': 'K', 'gray': 'U', 'red': 'A',
             'green': 'T', 'white': '0', 'black': '-1', 'blue': 'DO', 'orange': 'UP'}


def load_map():
    pass


def copy_map():
    # convert the grid into a string and copy it to the clipboard
    # the grid should be of the type

    # [floor1]
    # -1,0,0,A1,0
    # 0,0,0,-1,0
    # -1,-1,-1,0,0
    # 0,T1,0,0,0
    # -1,0,0,0,0

    # convert
    global root, map_grid, char_dict
    grid_str = ""

    for row in map_grid:
        grid_str += ",".join(
            list(map(lambda cell: char_dict[canvas.itemcget(cell, "fill")], row))) + "\n"

    root.clipboard_clear()
    root.clipboard_append(grid_str)


# Create buttons for loading and saving map
load_button = tk.Button(
    frame, text="Load Map from clipboard", command=load_map)
load_button.pack(pady=10)

copy_button = tk.Button(frame, text="Copy Map to clipboard", command=copy_map)
copy_button.pack(pady=10)


last_cell = None


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


# Create sliders for changing number of rows and columns
rows_slider = tk.Scale(frame, from_=5, to=100,
                       orient=tk.HORIZONTAL, command=update_rows)
rows_slider.set(20)
rows_slider.pack(pady=10)

columns_slider = tk.Scale(frame, from_=5, to=100,
                          orient=tk.HORIZONTAL, command=update_columns)
columns_slider.set(20)
columns_slider.pack(pady=10)


def make_blocked(event):
    global last_cell
    x = event.x // square_size
    y = event.y // square_size
    if (x, y) != last_cell:
        if map_grid[y][x] is None:
            map_grid[y][x] = canvas.create_rectangle(x * square_size, y * square_size,
                                                     (x + 1) * square_size, (y + 1) * square_size, outline='black')
            map_text[y][x] = canvas.create_text(
                x * square_size + square_size // 2, y * square_size + square_size // 2, text='')
        canvas.itemconfig(map_grid[y][x], fill='black')
        last_cell = (x, y)


def make_empty(event):
    global last_cell
    x = event.x // square_size
    y = event.y // square_size
    if (x, y) != last_cell:
        if map_grid[y][x] is None:
            map_grid[y][x] = canvas.create_rectangle(x * square_size, y * square_size,
                                                     (x + 1) * square_size, (y + 1) * square_size, outline='black')
            map_text[y][x] = canvas.create_text(
                x * square_size + square_size // 2, y * square_size + square_size // 2, text='')
        canvas.itemconfig(map_grid[y][x], fill='white')
        last_cell = (x, y)


def test(event):
    global last_cell
    x = event.x // square_size
    y = event.y // square_size
    char = event.char
    if (x, y) != last_cell:
        if map_grid[y][x] is None:
            map_grid[y][x] = canvas.create_rectangle(x * square_size, y * square_size,
                                                     (x + 1) * square_size, (y + 1) * square_size, outline='black')
            # create text in the middle of the cell
            map_text[y][x] = canvas.create_text(
                x * square_size + square_size // 2, y * square_size + square_size // 2, text='')

        elif char == 'd':
            canvas.itemconfig(map_grid[y][x], fill='brown')
            canvas.itemconfig(map_text[y][x], text='D')
        elif char == 'k':
            canvas.itemconfig(map_grid[y][x], fill='yellow')
            canvas.itemconfig(map_text[y][x], text='K')
        elif char == 'u':
            canvas.itemconfig(map_grid[y][x], fill='orange')
            canvas.itemconfig(map_text[y][x], text='UP')
        elif char == 'o':
            canvas.itemconfig(map_grid[y][x], fill='blue')
            canvas.itemconfig(map_text[y][x], text='DO')
        elif char == 'a':
            canvas.itemconfig(map_grid[y][x], fill='red')
            canvas.itemconfig(map_text[y][x], text='A')
        elif char == 't':
            canvas.itemconfig(map_grid[y][x], fill='green')
            canvas.itemconfig(map_text[y][x], text='T')

        last_cell = (x, y)


def do_nothing(event):
    pass


canvas.bind('<Button-1>', make_blocked)
canvas.bind('<B1-Motion>', make_blocked)
canvas.bind('<Button-3>', make_empty)
canvas.bind('<B3-Motion>', make_empty)
canvas.bind('<Key>', test)
canvas.focus_set()

root.mainloop()
