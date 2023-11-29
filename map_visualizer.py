from tkinter import *


class MapGUI:
    WINDOW_WIDTH = 1366
    WINDOW_HEIGHT = 768
    PANEL_WIDTH = 400
    COLOR_BLOCKED = "#3f3f3f"
    COLOR_EMPTY = "lightgray"
    COLOR_DOOR = "burlywood4"
    COLOR_ELEVATOR_UP = "gray"
    COLOR_ELEVATOR_DOWN = "gray"
    COLOR_KEY = "yellow"
    COLOR_START = "brown1"
    TCOLOR_START = "black"
    COLOR_TARGET = "chartreuse3"
    TCOLOR_TARGET = "black"
    COLOR_CURRENT = "blue"
    COLOR_PATH = "lightblue"
    TCOLOR_PATH = "red"

    def __init__(self, root, grid, paths, starts, targets):
        # initialize the number of floor, the width and height of the grid
        self.floors = len(grid)
        self.num_rows = len(grid[0])
        self.num_columns = len(grid[0][0])
        print(self.floors, self.num_rows, self.num_columns)

        self.CELL_SIZE = min(
            MapGUI.WINDOW_HEIGHT // self.num_rows,
            (MapGUI.WINDOW_WIDTH - MapGUI.PANEL_WIDTH) // self.num_columns,
        )

        # tkinter gui handler
        self.root = root

        # initialize information

        self.grid = grid
        self.paths = paths
        self.freq = [[[0 for _ in range(self.num_columns)] for _ in range(
            self.num_rows)] for _ in range(self.floors)]

        self.num_agents = len(self.paths)
        self.current_agent_path_indexes = [0] * self.num_agents
        self.current_agent_turn = 0
        self.current_floor = self.paths[self.current_agent_turn][
            self.current_agent_path_indexes[self.current_agent_turn]
        ][0]

        self.starts = starts
        self.targets = targets

        self.canvas = Canvas(
            self.root,
            width=self.CELL_SIZE * self.num_columns,
            height=self.CELL_SIZE * self.num_rows,
        )
        self.canvas.pack(side=LEFT)

        self.panel_group = Frame(
            self.root,
            width=MapGUI.PANEL_WIDTH,
            height=MapGUI.WINDOW_HEIGHT,
            highlightbackground="blue",
            highlightthickness=1,
        )
        self.panel_group.pack(side=RIGHT, fill=BOTH, expand=True)

        self.current_position_var = StringVar()
        self.current_point_var = StringVar()
        self.current_floor_var = StringVar()

        self.info_panel = Frame(
            self.panel_group,
            width=MapGUI.PANEL_WIDTH,
            height=MapGUI.WINDOW_HEIGHT // 2,
            highlightbackground="red",
            highlightthickness=1,
        )
        self.info_panel.pack(side=TOP, fill=BOTH, expand=True)
        self.control_panel = Frame(
            self.panel_group,
            width=MapGUI.PANEL_WIDTH,
            height=MapGUI.WINDOW_HEIGHT // 2,
            highlightbackground="green",
            highlightthickness=1,
        )
        self.control_panel.pack(side=BOTTOM, fill=BOTH, expand=True)

        self.cell_rect = [
            [None for _ in range(self.num_columns)] for _ in range(self.num_rows)
        ]
        self.cell_text = [
            [None for _ in range(self.num_columns)] for _ in range(self.num_rows)
        ]
        self.cell_agent = [
            None for _ in range(self.num_agents)
        ]
        self.cell_agent_text = [
            None for _ in range(self.num_agents)
        ]

        # Labels to display information, make it align left with some margin
        Label(self.info_panel, text="Current Position:").pack(side=TOP)
        Label(self.info_panel, textvariable=self.current_position_var).pack(side=TOP)
        Label(self.info_panel, text="Current Point:").pack(side=TOP)
        Label(self.info_panel, textvariable=self.current_point_var).pack(side=TOP)
        Label(self.info_panel, text="Current Floor:").pack(side=TOP)
        Label(self.info_panel, textvariable=self.current_floor_var).pack(side=TOP)

        # Buttons
        self.control_panel.columnconfigure(0, weight=1)
        self.control_panel.columnconfigure(1, weight=1)
        self.control_panel.columnconfigure(2, weight=1)
        self.control_panel.columnconfigure(3, weight=1)
        self.control_panel.columnconfigure(4, weight=1)
        Button(self.control_panel, text="Start", command=self.to_start).grid(
            row=4, column=0, sticky=(W, E)
        )
        Button(self.control_panel, text="Previous", command=self.to_previous).grid(
            row=4, column=1, sticky=(W, E)
        )
        Button(self.control_panel, text="Stop", command=self.toggle_loop).grid(
            row=4, column=2, sticky=(W, E)
        )
        Button(self.control_panel, text="Next", command=self.to_next).grid(
            row=4, column=3, sticky=(W, E)
        )
        Button(self.control_panel, text="End", command=self.to_end).grid(
            row=4, column=4, sticky=(W, E)
        )

        # is_looping
        self.is_looping = True

        self.setup()
        self.draw_grid()
        self.root.mainloop()

    def update_labels(self):
        # change label
        self.current_position_var.set(
            str(
                self.paths[self.current_agent_turn][
                    self.current_agent_path_indexes[self.current_agent_turn]
                ]
            )
        )
        self.current_floor_var.set(
            str(
                self.paths[self.current_agent_turn][
                    self.current_agent_path_indexes[self.current_agent_turn]
                ][0]
            )
        )

    def toggle_loop(self):
        self.is_looping = not self.is_looping

    def to_start(self):
        # update the current position
        self.current_agent_path_indexes = [0] * self.num_agents
        self.current_agent_turn = 0
        self.current_floor = self.paths[self.current_agent_turn][
            self.current_agent_path_indexes[self.current_agent_turn]
        ][0]

        # update the labels
        self.update_labels()

        self.draw_grid()

    def to_end(self):
        # TODO: fix for multiple agents
        # update the current position
        self.current_agent_path_indexes = [
            len(path) - 1 for path in self.paths]
        self.current_agent_turn = self.num_agents - 1
        self.current_floor = self.paths[self.current_agent_turn][
            self.current_agent_path_indexes[self.current_agent_turn]
        ][0]

        # update the labels
        self.update_labels()

        self.draw_grid()

    def to_previous(self, redraw=True):
        # update the current position
        if self.current_agent_path_indexes[self.current_agent_turn] - 1 < 0:
            return

        self.current_agent_path_indexes[self.current_agent_turn] -= 1

        self.current_agent_turn = (
            self.current_agent_turn - 1) % self.num_agents

        self.current_floor = self.paths[self.current_agent_turn][
            self.current_agent_path_indexes[self.current_agent_turn]
        ][0]

        # update the labels
        self.update_labels()

        self.draw_grid()

    def to_next(self, redraw=True):
        # update the current position
        if self.current_agent_path_indexes[self.current_agent_turn] + 1 >= len(
            self.paths[self.current_agent_turn]
        ):
            return

        self.current_agent_path_indexes[self.current_agent_turn] += 1

        self.current_agent_turn = (
            self.current_agent_turn + 1) % self.num_agents

        self.current_floor = self.paths[self.current_agent_turn][
            self.current_agent_path_indexes[self.current_agent_turn]
        ][0]

        # update the labels
        self.update_labels()

        self.draw_grid()

    def setup(self):
        self.root.title("CS420-Project1")
        self.root.geometry(str(MapGUI.WINDOW_WIDTH) +
                           "x" + str(MapGUI.WINDOW_HEIGHT))
        self.root.resizable(False, False)
        self.root.after(500, self.loop)

    def loop(self):
        if self.is_looping:
            self.to_next()
        self.root.after(500, self.loop)

    def draw_grid(self, heatmap=False):
        if heatmap:
            self.color_heatmap()
        else:
            self.color_grids()
            self.color_starts()
            self.color_targets()
            self.color_current_position()

    def color_heatmap(self):
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                cell_value = self.freq[self.current_floor][row][col]
                if cell_value == "-1":
                    self.draw_cell(
                        row, col, background_fill=MapGUI.COLOR_BLOCKED)
                else:
                    self.draw_cell(
                        row, col, background_fill=MapGUI.COLOR_EMPTY)

    def color_grids(self):
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                cell_value = self.grid[self.current_floor][row][col]
                if cell_value == "-1":
                    self.draw_cell(
                        row, col, background_fill=MapGUI.COLOR_BLOCKED)
                elif cell_value == "0":
                    self.draw_cell(
                        row, col, background_fill=MapGUI.COLOR_EMPTY)
                elif cell_value.startswith("K"):
                    self.draw_cell(
                        row, col, background_fill=MapGUI.COLOR_KEY, text=cell_value
                    )
                elif cell_value == "DO":
                    self.draw_cell(
                        row,
                        col,
                        background_fill=MapGUI.COLOR_ELEVATOR_DOWN,
                        text=cell_value,
                    )
                elif cell_value == "UP":
                    self.draw_cell(
                        row,
                        col,
                        background_fill=MapGUI.COLOR_ELEVATOR_UP,
                        text=cell_value,
                    )
                elif cell_value.startswith("D"):
                    self.draw_cell(
                        row, col, background_fill=MapGUI.COLOR_DOOR, text=cell_value
                    )

    def color_current_position(self):
        for turn, path in enumerate(self.paths):
            if len(path) <= 0:
                continue

            current_path_index = self.current_agent_path_indexes[turn]

            if path[current_path_index][0] == self.current_floor:
                self.draw_agent(
                    path[current_path_index][1],
                    path[current_path_index][2],
                    turn,
                    background_fill=MapGUI.COLOR_CURRENT,
                    text=str(turn + 1),
                )

    def draw_agent(self, row, col, agent_id, background_fill=None, text=""):
        x0 = col * self.CELL_SIZE
        y0 = row * self.CELL_SIZE
        x1 = x0 + self.CELL_SIZE
        y1 = y0 + self.CELL_SIZE

        x = (x0 + x1) / 2
        y = (y0 + y1) / 2
        if self.cell_agent[agent_id] is None:
            self.cell_agent[agent_id] = self.canvas.create_oval(
                x0, y0, x1, y1, outline="black", fill=background_fill
            )
            self.cell_agent_text[agent_id] = self.canvas.create_text(
                x,
                y,
                text=text,
                font=("Arial", int(self.CELL_SIZE / 2.5), "bold"),
            )
        else:
            self.canvas.coords(self.cell_agent[agent_id], x0, y0, x1, y1)
            self.canvas.itemconfig(
                self.cell_agent[agent_id], fill=background_fill)
            self.canvas.coords(self.cell_agent_text[agent_id], x, y)

    def color_starts(self):
        for i, start in enumerate(
            list(filter(lambda x: x[0] == self.current_floor, self.starts))
        ):
            self.draw_cell(
                start[1],
                start[2],
                text="A" + str(i + 1),
                background_fill=MapGUI.COLOR_START,
                text_fill=MapGUI.TCOLOR_START,
            )

    def color_targets(self):
        for i, target in enumerate(
            list(filter(lambda x: x[0] == self.current_floor, self.targets))
        ):
            self.draw_cell(
                target[1],
                target[2],
                text="T" + str(i + 1),
                background_fill=MapGUI.COLOR_TARGET,
                text_fill=MapGUI.TCOLOR_TARGET,
            )

    def draw_cell(self, row, col, text="", background_fill=None, text_fill="black"):
        x0 = col * self.CELL_SIZE
        y0 = row * self.CELL_SIZE
        x1 = x0 + self.CELL_SIZE
        y1 = y0 + self.CELL_SIZE

        if self.cell_rect[row][col] is None:
            self.cell_rect[row][col] = self.canvas.create_rectangle(
                x0, y0, x1, y1, outline="black", fill=background_fill
            )
        else:
            self.canvas.itemconfig(
                self.cell_rect[row][col], fill=background_fill)

        if self.cell_text[row][col] is None:
            # draw text in the center of the cell
            x = (x0 + x1) / 2
            y = (y0 + y1) / 2
            self.cell_text[row][col] = self.canvas.create_text(
                x,
                y,
                text=text,
                font=("Arial", int(self.CELL_SIZE / 2.5), "bold"),
                fill=text_fill,
            )
        else:
            self.canvas.itemconfig(self.cell_text[row][col], text=text)


if __name__ == "__main__":
    from utils import *
    from collections import deque

    class BFS:
        def __init__(self, grid):
            self.grid = grid
            self.n = len(grid)
            self.m = len(grid[0])
            self.explored = [[False] * self.m for _ in range(self.n)]
            self.directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
            self.diagonals = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
            self.path = [[(-1, -1)] * self.m for _ in range(self.n)]
            for i in range(self.n):
                for j in range(self.m):
                    if grid[i][j] == "A1":
                        self.start = (i, j)
                    elif grid[i][j] == "T1":
                        self.target = (i, j)

        def is_valid(self, x, y):
            return 0 <= x < self.n and 0 <= y < self.m and self.grid[x][y] != '-1'

        def process(self):
            queue = deque([(self.start[0], self.start[1])])
            self.explored[self.start[0]][self.start[1]] = True

            while queue:
                x, y = queue.popleft()

                if (x, y) == self.target:
                    return True

                for dx, dy in self.directions:
                    nx, ny = x + dx, y + dy

                    if self.is_valid(nx, ny) and not self.explored[nx][ny]:
                        queue.append((nx, ny))
                        self.explored[nx][ny] = True
                        self.path[nx][ny] = (x, y)

                for dx, dy in self.diagonals:
                    nx, ny = x + dx, y + dy

                    if self.is_valid(nx, ny) and not self.explored[nx][ny] and self.is_valid(x + dx, y) and self.is_valid(x, y + dy):
                        queue.append((nx, ny))
                        self.explored[nx][ny] = True
                        self.path[nx][ny] = (x, y)
            return False

        def get_path(self):
            path = []
            x, y = self.target
            while (x, y) != (-1, -1):
                path.append((x, y))
                x, y = self.path[x][y]
            return path[::-1]

    grid = map_input("test2.txt")
    bfs = BFS(grid[0])
    bfs.process()
    path = bfs.get_path()
    paths = [[(0, x, y) for x, y in path]]
    starts = get_starts(grid)
    targets = get_targets(grid)
    gui = MapGUI(Tk(), grid, paths, starts, targets)
