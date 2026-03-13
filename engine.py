import random
import sys
from file_pars import parse_config
import time
from collections import deque


class MazeToSmall(Exception):
    pass


class Grid:
    def __init__(self, height, width, the_entry, the_exit):
        self.height = height
        self.width = width
        self.entry = the_entry
        self.exit = the_exit
        self.grid = [[15 for x in range(width)] for y in range(height)]

    def make_42(self):
        if self.width >= 9 and self.height >= 7:
            h = int(self.height / 2)
            w = int(self.width / 2)

            self.grid[h][w - 1] = 100
            self.grid[h][w - 2] = 100
            self.grid[h][w - 3] = 100

            self.grid[h - 1][w - 3] = 100
            self.grid[h - 2][w - 3] = 100

            self.grid[h + 1][w - 1] = 100
            self.grid[h + 2][w - 1] = 100

            self.grid[h][w + 1] = 100
            self.grid[h][w + 2] = 100
            self.grid[h][w + 3] = 100

            self.grid[h + 1][w + 1] = 100
            self.grid[h + 2][w + 1] = 100

            self.grid[h + 2][w + 2] = 100
            self.grid[h + 2][w + 3] = 100

            self.grid[h - 1][w + 3] = 100
            self.grid[h - 2][w + 3] = 100

            self.grid[h - 2][w + 2] = 100
            self.grid[h - 2][w + 1] = 100

    def make_entry_exit(self):
        self.grid[self.entry[0]][self.entry[1]] += 16
        self.grid[self.exit[0]][self.exit[1]] += 16

    def make_solution(self, solution):
        for y, x in solution[1:]:
            self.grid[y][x] += 16

    def r_row(self, array, high, i):
        row = []
        for j, v in enumerate(array):
            if v & 1 or v == 100:
                row.extend(["█", "█", "█", "█", "█", "█", "█"])
            elif v & 16 and self.grid[i - 1][j] & 16:
                row.extend(["█", "█",
                            "\033[31m█\033[0m",
                            "\033[31m█\033[0m",
                            "\033[31m█\033[0m",
                            "\033[31m█\033[0m",
                            "\033[31m█\033[0m"])
            else:
                row.extend(["█","█", " "," ", " ", " ", " "])
        row.extend(["█", "█", "\n"])
        for x in range(2):
            for j, v in enumerate(array):
                if v & 8 or v == 100:
                    if v == 100:
                        row.extend(["█", "█",
                                    "\033[90m█\033[0m",
                                    "\033[90m█\033[0m",
                                    "\033[90m█\033[0m",
                                    "\033[90m█\033[0m",
                                    "\033[90m█\033[0m"])
                    else:
                        if v & 16:
                            row.extend(["█", "█",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m"])
                        else:
                            row.extend(["█", "█", " ", " ", " ", " ", " "])
                else:
                    if v & 16:
                        if self.grid[i][j - 1] & 16:
                            row.extend(["\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m"])
                        else:
                            row.extend([" ",
                                        " ",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m",
                                        "\033[31m█\033[0m"])

                    else:
                        row.extend([" ", " ", " ", " ", " ", " ", " "])

            row.extend(["█", "█", "\n"])
        if i == (high - 1):
            for v in array:
                if v & 4:
                    row.extend(["█", "█", "█", "█", "█", "█", "█"])
            row.extend(["█", "█", "\n"])
        return row

    def print_maze(self):
        visual = []
        for i, array in enumerate(self.grid):
            visual.extend(self.r_row(array, self.height, i))
        return visual


class Engine:
    def __init__(self, grid_array, height, width, exit_coord):
        self.grid = grid_array
        self.height = height
        self.width = width
        self.exit = exit_coord

    def dfs(self, y, x):
        lst = []
        while 1:
            moves = [(-1, 0, 1), (0, 1, 2), (0, -1, 8), (1, 0, 4)]
            random.shuffle(moves)
            flag = True
            for move in moves:
                yy = move[0]
                xx = move[1]
                wall = move[2]
                yyy = y + yy
                xxx = x + xx
                if (
                    0 <= xxx < self.width
                    and 0 <= yyy < self.height
                    and (self.grid[yyy][xxx] == 15
                         or self.grid[yyy][xxx] == 31)
                ):
                    self.grid[y][x] -= wall
                    if wall == 1:
                        self.grid[yyy][xxx] -= 4
                    elif wall == 2:
                        self.grid[yyy][xxx] -= 8
                    elif wall == 4:
                        self.grid[yyy][xxx] -= 1
                    elif wall == 8:
                        self.grid[yyy][xxx] -= 2
                    lst.append((y, x))
                    y = yyy
                    x = xxx
                    flag = False
                    break
            if flag:
                if lst:
                    y, x = lst.pop()
                else:
                    break

    def bfs_solver(self, y, x):
        queue = deque([(y, x, [])])
        visited = {(y, x)}
        while 1:
            p = queue.popleft()
            y = p[0]
            x = p[1]
            solution = p[2]
            if y == self.exit[0] and x == self.exit[1]:
                return solution
            nighbors = (
                    (y - 1, x + 0, 1),
                    (y + 1, x + 0, 4),
                    (y + 0, x - 1, 8),
                    (y + 0, x + 1, 2))
            for nighbor in nighbors:
                if (0 <= nighbor[0] < self.height
                    and 0 <= nighbor[1] < self.width):
                    if not self.grid[y][x] & nighbor[2]:
                        if (nighbor[0], nighbor[1]) not in visited:
                            visited.add((nighbor[0], nighbor[1]))
                            queue.append((nighbor[0], nighbor[1], solution + [(y, x)]))
    
def output_file(maze_array, solution, height, width, the_entry, the_exit):
    with open("output_maze.txt", 'w') as output:
        for y in range(height):
            for x in range(width):
                cell = maze_array[y][x]
                if cell >= 100:
                    output.write("F")
                else:
                    cell = cell & 15
                    output.write(f"{cell:X}")
            output.write("\n")
        output.write("\n")
        output.write(f"{the_entry[0]},{the_entry[1]}\n")
        output.write(f"{the_exit[0]},{the_exit[1]}\n")
        i = 0
        while (i < (len(solution) - 1)):
            y = solution[i][0]
            x = solution[i][1]
            y2 = solution[i + 1][0]
            x2 = solution[i + 1][1]
            if y == y2 and x > x2:
                output.write("W")
            elif y == y2 and x < x2:
                output.write("E")
            elif y > y2 and x == x2:
                output.write("N") 
            elif y < y2 and x == x2:
                output.write("S")
            i += 1
        output.write("\n")

        
def main():
    if len(sys.argv) == 2:
        try:
            config = parse_config(sys.argv[1])
            grid = Grid(
                    config["HEIGHT"],
                    config["WIDTH"],
                    (config["ENTRY_Y"], config["ENTRY_X"]),
                    (config["EXIT_Y"], config["EXIT_X"])
                    )
            grid.make_42()
            grid.make_entry_exit()
            engine = Engine(grid.grid, grid.height, grid.width, grid.exit)
            engine.dfs(config["ENTRY_Y"], config["ENTRY_X"])
            solution = engine.bfs_solver(config["ENTRY_Y"], config["ENTRY_X"])
            grid.make_solution(solution)
            lst = grid.print_maze()
            for x in lst:
                print(x, end="")
            output_file(grid.grid, solution, grid.height, grid.width, grid.entry, grid.exit)

        except ValueError as e:
            print(e)
        except FileNotFoundError as e:
            print(e)
    elif len(sys.argv) == 1:
        print("you must provide config.txt file example: python3 a_maze_ing.py config.txt")
    else:
        print("you must run at most one arguments example: python3 a_maze_ing.py config.txt")


if __name__ == "__main__":
    main()
