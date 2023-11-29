def map_input(file_name):
    grid = []
    with open(file_name, "r") as file:
        n, m = map(int, file.readline().split(","))
        while floorname := file.readline().strip():
            floor = []
            for i in range(n):
                floor.append(list(file.readline().strip().split(",")))
            grid.append(floor)

    return grid


def get_starts(grid):
    starts = []
    for k in range(len(grid)):
        for i in range(len(grid[0])):
            for j in range(len(grid[0][0])):
                if grid[k][i][j].startswith("A"):
                    starts.append((k, i, j))
    return starts


def get_targets(grid):
    targets = []
    for k in range(len(grid)):
        for i in range(len(grid[0])):
            for j in range(len(grid[0][0])):
                if grid[k][i][j].startswith("T"):
                    targets.append((k, i, j))
    return targets
