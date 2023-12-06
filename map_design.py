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
              'A': 'red', 'T': 'green', '0': 'white', '-1': 'black'}

char_dict = {'brown': 'D', 'yellow': 'K', 'gray': 'U', 'red': 'A',
             'green': 'T', 'white': '0', 'black': '-1', 'blue': 'DO', 'orange': 'UP'}


def load_map():
    # get the grid from the clipboard and convert it into a grid

    global root, map_grid, map_text, char_dict
    grid_str = root.clipboard_get()
    print(repr(str(grid_str)))
    grid_str = grid_str.strip()
    print(repr(grid_str))
    grid_str = grid_str.split('\n')
    grid_str = list(map(lambda row: row.split(','), grid_str))
    print(repr(grid_str))
    m = len(grid_str)
    n = len(grid_str[0])
    square_size = 900 // max(m, n)

    canvas.delete('all')

    map_grid = [[None for _ in range(n)] for _ in range(m)]
    map_text = [[None for _ in range(n)] for _ in range(m)]

    for i in range(m):
        for j in range(n):
            if grid_str[i][j] == '-1':
                map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                         (j + 1) * square_size, (i + 1) * square_size, fill='black', outline='black')
                map_text[i][j] = canvas.create_text(
                    j * square_size + square_size // 2, i * square_size + square_size // 2, text=grid_str[i][j], fill='white')
            if grid_str[i][j] == '0':
                map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                         (j + 1) * square_size, (i + 1) * square_size, fill='white', outline='black')
                map_text[i][j] = canvas.create_text(
                    j * square_size + square_size // 2, i * square_size + square_size // 2, text=grid_str[i][j])
            if grid_str[i][j].startswith('A'):
                map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                         (j + 1) * square_size, (i + 1) * square_size, fill='red', outline='black')
                map_text[i][j] = canvas.create_text(
                    j * square_size + square_size // 2, i * square_size + square_size // 2, text=grid_str[i][j], fill='white')
            if grid_str[i][j].startswith('T'):
                map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                         (j + 1) * square_size, (i + 1) * square_size, fill='green', outline='black')
                map_text[i][j] = canvas.create_text(
                    j * square_size + square_size // 2, i * square_size + square_size // 2, text=grid_str[i][j], fill='white')
            if grid_str[i][j].startswith('D'):
                map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                         (j + 1) * square_size, (i + 1) * square_size, fill='brown', outline='black')
                map_text[i][j] = canvas.create_text(
                    j * square_size + square_size // 2, i * square_size + square_size // 2, text=grid_str[i][j])
            if grid_str[i][j].startswith('K'):
                map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                         (j + 1) * square_size, (i + 1) * square_size, fill='yellow', outline='black')
                map_text[i][j] = canvas.create_text(
                    j * square_size + square_size // 2, i * square_size + square_size // 2, text=grid_str[i][j])
            if grid_str[i][j] == 'UP':
                map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                         (j + 1) * square_size, (i + 1) * square_size, fill='orange', outline='black')
                map_text[i][j] = canvas.create_text(
                    j * square_size + square_size // 2, i * square_size + square_size // 2, text=grid_str[i][j])
            if grid_str[i][j] == 'DO':
                map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                         (j + 1) * square_size, (i + 1) * square_size, fill='blue', outline='black')
                map_text[i][j] = canvas.create_text(
                    j * square_size + square_size // 2, i * square_size + square_size // 2, text=grid_str[i][j], fill='white')

    dimensions_slider.set(m)


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
    global root, map_grid, char_dict, map_text
    grid_str = ""

    for row in map_text:
        grid_str += ",".join(
            list(map(lambda cell: canvas.itemcget(cell, "text"), row))) + "\n"

    root.clipboard_clear()
    root.clipboard_append(grid_str)


# Create buttons for loading and saving map
load_button = tk.Button(
    frame, text="Load Map from clipboard", command=load_map)
load_button.pack(pady=10)

copy_button = tk.Button(frame, text="Copy Map to clipboard", command=copy_map)
copy_button.pack(pady=10)

# create hints for the user
hint_label = tk.Label(
    frame, text="Left click to block, right click to unblock")
hint_label.pack(pady=10)

hint_label = tk.Label(
    frame, text="Press a key to add a special cell")
hint_label.pack(pady=10)

hint_label = tk.Label(
    frame, text="d: Door, k: Key, u: Up, o: Down, a: Agent, t: Target")
hint_label.pack(pady=10)


last_cell = None


def update_dimensions(val):
    global m, n, square_size, map_grid, map_text
    m = n = int(val)
    square_size = 900 // max(m, n)
    map_grid = [[None for _ in range(n)] for _ in range(m)]
    map_text = [[None for _ in range(n)] for _ in range(m)]
    canvas.delete('all')
    for i in range(m):
        for j in range(n):
            map_grid[i][j] = canvas.create_rectangle(j * square_size, i * square_size,
                                                     (j + 1) * square_size, (i + 1) * square_size, fill='white', outline='black')
            map_text[i][j] = canvas.create_text(
                j * square_size + square_size // 2, i * square_size + square_size // 2, text='0', fill='black')


clear_button = tk.Button(frame, text="Clear", command=lambda: update_dimensions(
    dimensions_slider.get()))
clear_button.pack(pady=10)
# Create a slider for changing the number of rows and columns
dimensions_slider = tk.Scale(frame, from_=5, to=100,
                             orient=tk.HORIZONTAL, command=update_dimensions)
dimensions_slider.set(20)
dimensions_slider.pack(pady=10)


def make_blocked(event):
    global last_cell
    x = event.x // square_size
    y = event.y // square_size
    if (x, y) != last_cell:
        if map_grid[y][x] is None:
            map_grid[y][x] = canvas.create_rectangle(x * square_size, y * square_size,
                                                     (x + 1) * square_size, (y + 1) * square_size, outline='black', fill='black')
            map_text[y][x] = canvas.create_text(
                x * square_size + square_size // 2, y * square_size + square_size // 2, text='-1', fill='white')
        canvas.itemconfig(map_grid[y][x], fill='black')
        canvas.itemconfig(map_text[y][x], text='-1',
                          fill='white', font=('Arial', 10))
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
                x * square_size + square_size // 2, y * square_size + square_size // 2, text='0', fill='black')
        canvas.itemconfig(map_grid[y][x], fill='white')
        canvas.itemconfig(map_text[y][x], text='0', fill='black')
        last_cell = (x, y)


def test(event):
    global last_cell
    x = event.x // square_size
    y = event.y // square_size
    char = event.char
    if map_grid[y][x] is None:
        map_grid[y][x] = canvas.create_rectangle(x * square_size, y * square_size,
                                                 (x + 1) * square_size, (y + 1) * square_size, outline='black')
        # create text in the middle of the cell
        map_text[y][x] = canvas.create_text(
            x * square_size + square_size // 2, y * square_size + square_size // 2, text='0', fill='black')

    if char.isdigit():
        canvas.itemconfig(map_text[y][x], text=canvas.itemcget(
            map_text[y][x], "text") + char, fill=canvas.itemcget(map_text[y][x], "fill"))
    elif char == 'd':
        canvas.itemconfig(map_grid[y][x], fill='brown')
        canvas.itemconfig(map_text[y][x], text='D', fill='white')
    elif char == 'k':
        canvas.itemconfig(map_grid[y][x], fill='yellow')
        canvas.itemconfig(map_text[y][x], text='K', fill='black')
    elif char == 'u':
        canvas.itemconfig(map_grid[y][x], fill='orange')
        canvas.itemconfig(map_text[y][x], text='UP', fill='black')
    elif char == 'o':
        canvas.itemconfig(map_grid[y][x], fill='blue')
        canvas.itemconfig(map_text[y][x], text='DO', fill='white')
    elif char == 'a':
        canvas.itemconfig(map_grid[y][x], fill='red')
        canvas.itemconfig(map_text[y][x], text='A', fill='white')
    elif char == 't':
        canvas.itemconfig(map_grid[y][x], fill='green')
        canvas.itemconfig(map_text[y][x], text='T', fill='white')

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
