import random, os, sys
import numpy as np

marks = 0

def trim(seqs, direction=0):
    """
    direction: 1=> right,down 0=> left,up
    """
    if direction:
        return ([0,0,0,0] + [seq for seq in seqs if seq])[-4:]
    else:
        return ([seq for seq in seqs if seq] + [0,0,0,0])[:4]
        

def sum_seqs(seqs, direction=0):
    """
    direction: 1=> right,down 0=> left,up
    """
    global marks
    if direction:
        ran = range(1,4)
    else:
        ran = range(3)

    for i in ran:
        now = i
        nex = i+1
        if direction:
            now = -now
            nex = -nex
        if seqs[now] and seqs[nex] and seqs[now] == seqs[nex]:
            mark = seqs[now] * 2
            marks += mark
            seqs[now] = mark
            seqs[nex] = 0   

    return trim(seqs,direction=direction)

def up(grid):
    # Return Transposed array
    return np.array([sum_seqs(trim(r)) for r in grid.T]).T

def down(grid):
    # Return Transposed array
    return np.array([sum_seqs(trim(r,direction=1),direction=1) for r in grid.T]).T

def left(grid):
    return [sum_seqs(trim(r)) for r in grid]

def right(grid):
    return [sum_seqs(trim(r,direction = 1), direction = 1) for r in grid]

class Game:
    grid = np.zeros((4,4),int)
    controls=['w','a','s','d']
    global marks

    def rnd_field(self):
        """
        Create 2 or 4 in random field
        """
        number = random.choice([2,4,2,4,2,4,2,4,2,4,2,4])
        field = (self.grid==0).nonzero()
        xs = field[0]
        ys = field[1]
        coor = random.randint(0,len(xs)*3-1)//3
        x, y = xs[coor],ys[coor]
        self.grid[x][y] = number
    
    def print_screen(self):
        """
        print board and score
        """
        os.system('cls')
        print('-'*21)
        for row in self.grid:
            print('|{}|'.format('|'.join([(str(col) if col != 0 else '').center(4) for col in row])))
        print('-'*21)
        print('Scores:',marks)

    def logic(self,control):
        grid = np.array({'w':up,'a':left,'s':down,'d':right}[control](np.copy(self.grid)))
        if 2048 in grid:
            self.grid = np.copy(grid)
            return 1, 'You win!'

        if (grid == self.grid).all():
            if 0 not in grid and np.all([(f(grid) == grid).all() for f in [up,down,left,right]]):
                return -1, 'You lose!'
            else:
                return 0,''
        self.grid = np.copy(grid)
        self.rnd_field()
        return 0,''

    def main_loop(self):
        self.grid = np.zeros((4,4),int)
        self.rnd_field()
        self.rnd_field()
        while True:
            self.print_screen()
            control = input('input w/a/s/d:')
            if control in self.controls:
                status, info = self.logic(control)
                if status:
                    print(info)
                    if input('Start another game?[Y/n]').lower() == "y":
                        break
                    else:
                        sys.exit(0)
        self.main_loop()
        
if __name__ == '__main__':
    Game().main_loop()