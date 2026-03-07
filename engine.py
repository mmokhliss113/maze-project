import random

WIDTH = 23
HEIGHT = 21
ENTRY = 0,0
EXIT = 19,14
PERFECT = True

class MazeToSmall(Exception):
    pass

class Grid:
    def __init__(self, height, width):
        self.height = height
        self.width = width
        self.grid = [[15 for x in range(width)] for y in range(height)]
    
    def make_42(self):
        if self.width >= 9 and self.height >= 7:
            h = int(self.height / 2)
            w = int(self.width / 2)
            
            self.grid[h][w - 1] = 16
            self.grid[h][w - 2] = 16
            self.grid[h][w - 3] = 16
            
            self.grid[h - 1][w - 3] = 16
            self.grid[h - 2][w - 3] = 16
            
            self.grid[h + 1][w - 1] = 16
            self.grid[h + 2][w - 1] = 16
           


            self.grid[h][w + 1] = 16
            self.grid[h][w + 2] = 16
            self.grid[h][w + 3] = 16

            self.grid[h + 1][w + 1] = 16
            self.grid[h + 2][w + 1] = 16
            
            self.grid[h + 2][w + 2] = 16
            self.grid[h + 2][w + 3] = 16
            
            self.grid[h - 1][w + 3] = 16
            self.grid[h - 2][w + 3] = 16

            self.grid[h - 2][w + 2] = 16
            self.grid[h - 2][w + 1] = 16
        else:
            raise MazeToSmall("the maze is to small")
        
    @staticmethod
    def r_row(array, high, i):
        row = []
        for v in array:
                if v & 1 or v == 16:
                    row.extend(["███████"])
                else:
                    row.extend(["██", "     "])
        row.extend(["██", "\n"])
        for x in range(2):
            for v in array:
                if v & 8 or v == 16:
                    if v == 16:

                        row.extend(["██", "\033[90m█████\033[0m"]) 
                    else:
                        row.extend(["██", "     "])
                else:
                    row.extend(["       "])
            row.extend(["██", "\n"])
        if i == (high - 1): 
            for v in array:
                if v & 4:
                    row.extend(["███████"])
            row.extend(["██", "\n"])
        return(row)


    def print_maze(self):
        visual = []
        for i, array in enumerate(self.grid):
            visual.extend(self.r_row(array, self.height, i))
        return visual
            
class Engine:
    def __init__(self, grid):
        self.maze = grid

    def dfs(self, y, x):
        lst = []
        while(1):
            moves = [(-1, 0, 1), (0, 1, 2), (0, -1, 8), (1, 0, 4)]
            random.shuffle(moves)
            flag = True
            for move in moves:
                yy = move[0]
                xx = move[1]
                wall = move[2]
                yyy = y + yy
                xxx = x + xx
                if 0 <= xxx < self.maze.width\
                        and 0 <= yyy < self.maze.height\
                        and self.maze.grid[yyy][xxx] == 15:
                        self.maze.grid[y][x] -= wall
                        if wall == 1:
                            self.maze.grid[yyy][xxx] -= 4
                        elif wall == 2:
                            self.maze.grid[yyy][xxx] -= 8
                        elif wall == 4:
                            self.maze.grid[yyy][xxx] -= 1
                        elif wall == 8:
                            self.maze.grid[yyy][xxx] -= 2
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

def main():
    try:
        grid = Grid(HEIGHT, WIDTH)
        grid.make_42()
        engine = Engine(grid)
        engine.dfs(0, 0)
        lst = grid.print_maze()
        for x in lst:
            print(x, end="")
    except MazeToSmall as e:
        print(e)

if __name__ == "__main__":
    main()

