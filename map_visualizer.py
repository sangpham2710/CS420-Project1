from tkinter import *
from tkinter import ttk
from PIL import Image
from PIL import EpsImagePlugin

EpsImagePlugin.gs_windows_binary = r'./gs10.02.1/bin/gswin64c.exe'


class MapGUI:
    TIME_INTERVAL = 500
    WINDOW_WIDTH = 1500
    WINDOW_HEIGHT = 1000
    PANEL_WIDTH = 200
    COLOR_BLOCKED = "#3f3f3f"
    COLOR_EMPTY = "lightgray"
    COLOR_DOOR = "burlywood4"
    COLOR_ELEVATOR_UP = "orange"
    COLOR_ELEVATOR_DOWN = "blue"
    COLOR_KEY = "yellow"
    COLOR_START = "brown1"
    TCOLOR_START = "black"
    COLOR_TARGET = "chartreuse3"
    TCOLOR_TARGET = "black"
    COLOR_CURRENT = "pink"
    COLOR_PATH = "lightblue"
    TCOLOR_PATH = "red"

    def __init__(self, root, grid, paths, starts, targets, points, is_level4=False):
        self.is_level4 = is_level4
        self.floors = len(grid)
        self.num_rows = len(grid[0])
        self.num_columns = len(grid[0][0])

        self.CELL_SIZE = min(
            MapGUI.WINDOW_HEIGHT // self.num_rows,
            (MapGUI.WINDOW_WIDTH - MapGUI.PANEL_WIDTH) // self.num_columns,
        )

        self.root = root

        self.grid = grid
        self.paths = paths
        self.points = points

        self.num_agents = len(self.paths)
        self.current_agent_path_indexes = [0] * self.num_agents
        self.current_agent_turn = 0

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
        self.current_agent_var = StringVar()
        self.current_agent_turn_var = StringVar()

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

        font_size = 16

        ttk.Label(self.info_panel, text="Position of current agent:", font=(
            "default", font_size), anchor="w").grid(row=0, column=0, sticky='w', padx=10)
        ttk.Label(self.info_panel, textvariable=self.current_position_var, font=(
            "default", font_size), anchor="w").grid(row=0, column=1, sticky='w', padx=10)

        ttk.Label(self.info_panel, text="Current point of agent 1 (A1):", font=(
            "default", font_size), anchor="w").grid(row=1, column=0, sticky='w', padx=10)
        ttk.Label(self.info_panel, textvariable=self.current_point_var, font=(
            "default", font_size), anchor="w").grid(row=1, column=1, sticky='w', padx=10)

        ttk.Label(self.info_panel, text="Current viewing floor:", font=(
            "default", font_size), anchor="w").grid(row=2, column=0, sticky='w', padx=10)
        ttk.Label(self.info_panel, textvariable=self.current_floor_var, font=(
            "default", font_size), anchor="w").grid(row=2, column=1, sticky='w', padx=10)

        ttk.Label(self.info_panel, text="Current viewing agent:", font=(
            "default", font_size), anchor="w").grid(row=3, column=0, sticky='w', padx=10)
        ttk.Label(self.info_panel, textvariable=self.current_agent_var, font=(
            "default", font_size), anchor="w").grid(row=3, column=1, sticky='w', padx=10)

        ttk.Label(self.info_panel, text="Current agent turn:", font=(
            "default", font_size), anchor="w").grid(row=4, column=0, sticky='w', padx=10)
        ttk.Label(self.info_panel, textvariable=self.current_agent_turn_var, font=(
            "default", font_size), anchor="w").grid(row=4, column=1, sticky='w', padx=10)

        self.control_panel.columnconfigure(0, weight=1)
        self.control_panel.columnconfigure(1, weight=1)
        self.control_panel.columnconfigure(2, weight=1)
        self.control_panel.columnconfigure(3, weight=1)
        self.control_panel.columnconfigure(4, weight=1)
        ttk.Button(self.control_panel, text="TO FIRST", command=self.to_start).grid(
            row=4, column=0, sticky=(W, E), padx=5)
        ttk.Button(self.control_panel, text="PREVIOUS", command=self.to_previous).grid(
            row=4, column=1, sticky=(W, E), padx=5)

        self.button_stop = ttk.Button(
            self.control_panel, text="STOP", command=self.toggle_loop)
        self.button_stop.grid(row=4, column=2, sticky=(W, E), padx=5)

        ttk.Button(self.control_panel, text="NEXT", command=self.to_next).grid(
            row=4, column=3, sticky=(W, E), padx=5)
        ttk.Button(self.control_panel, text="TO LAST", command=self.to_end).grid(
            row=4, column=4, sticky=(W, E), padx=5)

        ttk.Button(self.control_panel, text="HEATMAP", command=self.toggle_heatmap).grid(
            row=5, column=2, sticky=(W, E), padx=5)
        ttk.Button(self.control_panel, text="EXPORT ALL HEATMAP", command=self.export_heatmap).grid(
            row=5, column=3, columnspan=2, sticky=(W, E), padx=5)

        self.focus_mode = 'agent'
        self.current_agent_focus = 0
        self.current_floor_focus = 0
        ttk.Button(self.control_panel, text="SWITCH FLOOR", command=self.switch_floor).grid(
            row=6, column=2, sticky=(W, E), padx=5)

        ttk.Button(self.control_panel, text="SWITCH AGENT", command=self.switch_agent).grid(
            row=6, column=3, sticky=(W, E), padx=5)

        self.is_looping = True

        self.is_heatmap = False

        self.setup()
        self.draw_grid()
        self.root.mainloop()

    def get_current_floor(self):
        if self.focus_mode == 'agent':
            return self.paths[self.current_agent_focus][
                self.current_agent_path_indexes[self.current_agent_focus]
            ][0]
        else:
            return self.current_floor_focus

    def switch_floor(self):
        if self.focus_mode == 'agent':
            self.focus_mode = 'floor'
        else:
            self.current_floor_focus = (
                self.current_floor_focus + 1) % self.floors
        self.update_labels()
        self.draw_grid()

    def switch_agent(self):
        if self.focus_mode == 'floor':
            self.focus_mode = 'agent'
        else:
            self.current_agent_focus = (
                self.current_agent_focus + 1) % self.num_agents
        self.update_labels()
        self.draw_grid()

    def export_heatmap(self):
        import os

        for file in os.listdir("./heatmap-output"):
            if file.endswith(".png"):
                os.remove(os.path.join("./heatmap-output", file))

        self.current_agent_path_indexes = [
            len(path) - 1 for path in self.paths]
        self.current_agent_turn = self.num_agents - 1

        for turn, path in enumerate(self.paths):
            for floor in range(self.floors):
                self.focus_mode = 'floor'
                self.current_floor_focus = floor
                self.current_agent_turn = turn
                self.is_heatmap = True
                self.draw_grid()
                filename = "./heatmap-output/heatmap_agent_" + \
                    str(turn + 1) + "_floor_" + str(floor + 1)
                self.canvas.postscript(
                    file=filename + ".eps", colormode='color', pagewidth=1000)
                img = Image.open(filename + ".eps")
                img.convert()
                img.save(filename + ".png", "png")
                img.close()

                os.remove(filename + ".eps")

        self.current_agent_path_indexes = [0] * self.num_agents
        self.current_agent_turn = 0
        self.is_heatmap = False

    def toggle_heatmap(self):
        self.is_heatmap = not self.is_heatmap
        self.draw_grid()

    def update_labels(self):
        self.current_position_var.set(
            str(
                self.paths[self.current_agent_turn][
                    self.current_agent_path_indexes[self.current_agent_turn]
                ]
            )
        )
        self.current_floor_var.set(
            str(
                self.get_current_floor()
            )
        )
        self.current_agent_var.set(
            str(
                self.current_agent_focus + 1 if self.focus_mode == 'agent' else 'N/A'
            )
        )
        self.current_point_var.set(
            str(
                self.points[self.current_agent_path_indexes[0]]
            )
        )
        self.current_agent_turn_var.set(
            str(
                self.current_agent_turn + 1
            )
        )

    def toggle_loop(self):
        self.is_looping = not self.is_looping
        self.button_stop.config(text="STOP" if self.is_looping else "CONTINUE")

    def to_start(self):
        self.current_agent_path_indexes = [0] * self.num_agents
        self.current_agent_turn = 0

        self.update_labels()

        self.draw_grid()

    def to_end(self):
        self.current_agent_path_indexes = [
            len(path) - 1 for path in self.paths]
        self.current_agent_turn = 0

        self.update_labels()

        self.draw_grid()

    def to_previous(self, redraw=True):
        self.current_agent_turn = (
            self.current_agent_turn - 1) % self.num_agents

        self.current_agent_path_indexes[self.current_agent_turn] -= 1

        if self.current_agent_path_indexes[self.current_agent_turn] < 0:
            self.current_agent_path_indexes[self.current_agent_turn] = 0

        self.update_labels()

        self.draw_grid()

    def to_next(self, redraw=True):
        if self.current_agent_path_indexes[self.current_agent_turn] + 1 >= len(
            self.paths[self.current_agent_turn]
        ):
            return

        self.current_agent_path_indexes[self.current_agent_turn] += 1

        self.current_agent_turn = (
            self.current_agent_turn + 1) % self.num_agents

        self.update_labels()

        self.draw_grid()

    def setup(self):
        self.root.title("CS420-Project1")
        self.root.geometry(str(MapGUI.WINDOW_WIDTH) +
                           "x" + str(MapGUI.WINDOW_HEIGHT))
        self.root.resizable(False, False)
        self.root.after(MapGUI.TIME_INTERVAL, self.loop)

    def loop(self):
        if self.is_looping:
            self.to_next()
        self.root.after(MapGUI.TIME_INTERVAL, self.loop)

    def draw_grid(self):
        if self.is_heatmap:
            self.color_heatmap()
        else:
            self.color_grids()
            self.color_starts()
            self.color_targets()
            self.color_current_position()

    def color_heatmap(self):
        self.freq = [[[[0 for _ in range(self.num_columns)]
                       for _ in range(self.num_rows)] for _ in range(self.floors)] for _ in range(self.num_agents)]
        for turn, path in enumerate(self.paths):
            if len(path) <= 0:
                continue

            for i in range(self.current_agent_path_indexes[turn] + 1):
                floor = path[i][0]
                row = path[i][1]
                col = path[i][2]
                self.freq[turn][floor][row][col] += 1

        max_freq = 0
        for turn, path in enumerate(self.paths):
            if len(path) <= 0:
                continue

            for floor in range(self.floors):
                for row in range(self.num_rows):
                    for col in range(self.num_columns):
                        if self.freq[turn][floor][row][col] > max_freq:
                            max_freq = self.freq[turn][floor][row][col]

        for agent_id in range(self.num_agents):
            if self.cell_agent[agent_id] is not None:
                self.canvas.delete(self.cell_agent[agent_id])
                self.cell_agent[agent_id] = None
            if self.cell_agent_text[agent_id] is not None:
                self.canvas.delete(self.cell_agent_text[agent_id])
                self.cell_agent_text[agent_id] = None

        for row in range(self.num_rows):
            for col in range(self.num_columns):
                cell_value = self.grid[self.get_current_floor()][row][col]
                if cell_value == "-1":
                    self.draw_cell(
                        row, col, background_fill=MapGUI.COLOR_BLOCKED)
                else:
                    cur_freq = self.freq[self.current_agent_turn][self.get_current_floor(
                    )][row][col]
                    if cur_freq == 0:
                        self.draw_cell(
                            row, col, background_fill=MapGUI.COLOR_EMPTY)
                    else:
                        self.draw_cell(
                            row, col, background_fill=self.get_heatmap_color(cur_freq, max_freq), text=str(cur_freq)
                        )

    def get_heatmap_color(self, freq, max_freq):
        g = int(255 * (1 - freq / max_freq))
        r = int(255 * (freq / max_freq))
        return '#%02x%02x%02x' % (r, g, 0)

    def color_grids(self):
        for row in range(self.num_rows):
            for col in range(self.num_columns):
                cell_value = self.grid[self.get_current_floor()][row][col]
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
        for agent_id in range(self.num_agents):
            if self.cell_agent[agent_id] is not None:
                self.canvas.delete(self.cell_agent[agent_id])
                self.cell_agent[agent_id] = None
            if self.cell_agent_text[agent_id] is not None:
                self.canvas.delete(self.cell_agent_text[agent_id])
                self.cell_agent_text[agent_id] = None
        for turn, path in enumerate(self.paths):
            if len(path) <= 0:
                continue

            current_path_index = self.current_agent_path_indexes[turn]

            if path[current_path_index][0] == self.get_current_floor():
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
            list(filter(lambda x: x[0] ==
                 self.get_current_floor(), self.starts))
        ):
            self.draw_cell(
                start[1],
                start[2],
                text="A" + str(i + 1),
                background_fill=MapGUI.COLOR_START,
                text_fill=MapGUI.TCOLOR_START,
            )

    def color_targets(self):
        if not self.is_level4:
            for i, target in enumerate(
                list(filter(lambda x: x[0] ==
                     self.get_current_floor(), self.targets))
            ):
                self.draw_cell(
                    target[1],
                    target[2],
                    text="T" + str(i + 1),
                    background_fill=MapGUI.COLOR_TARGET,
                    text_fill=MapGUI.TCOLOR_TARGET,
                )
        else:
            current_targets = []
            for i, target in enumerate(self.targets):
                if target[self.current_agent_path_indexes[i]][0] == self.get_current_floor():
                    current_targets.append(
                        target[self.current_agent_path_indexes[i]])
                else:
                    current_targets.append(None)

            for i, target in enumerate(current_targets):
                if target is not None:
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
