# load picture
import os


class Piece(object):
    def __init__(self, row, col, animal, color):
        """
        color: True => red
               False => green
        """
        ANIMAL = {
            'rat': 1,
            'cat': 2,
            'dog': 3,
            'wolf': 4,
            'leopard': 5,
            'tiger': 6,
            'lion': 7,
            'elephant': 8,
        }
        self.row = row
        self.col = col
        self.animal = animal
        self.val = ANIMAL[animal]
        self.color = color
        self.movement = []
        self.img = os.path.join("assets", self.animal + ("Red" if self.color == True else "Green") + ".png")

    def validEat(self, board, dest_row, dest_col):
        """
        Check whether can eat.
        Return True of False
        """

        trap = {
            True: [(0, 2), (0, 4), (1, 3)],
            False: [(8, 2), (8, 4), (7, 3)]
        }

        other = board[dest_row][dest_col]

        if other is not None:
            if self.color != other.color:
                # if other in self trap
                if (other.row, other.col) in trap[self.color]:
                    return True
                if self.val == 8 and other.val == 1:
                    return False
                if self.val >= other.val or (self.val == 1 and other.val == 8):
                    return True
            else:
                return False
        else:
            if (dest_row, dest_col) in trap[self.color]:
                return False
            return True

    def validMove(self, board, terrain):
        """
        Show valid movement
        board: multidimensional list containing pieces and None
        Return valid movement in list
        """

        def rat(row=None, col=None):
            """
            Determine whether rat blocks the river
            """
            if row:
                if col == 1 or col == 4:
                    if board[row][col] or board[row][col + 1]:
                        return True
                else:
                    if board[row][col] or board[row][col - 1]:
                        return True

            else:
                if board[3][col] or board[4][col] or board[5][col]:
                    return True

            return False

        guesses = [(self.row - 1, self.col), (self.row, self.col - 1), (self.row + 1, self.col),
                   (self.row, self.col + 1)]
        moves = []

        for guess in guesses:
            row, col = guess
            if (row >= 0 and row <= 8 and col >= 0 and col <= 6):
                # rat can only eats enemy if they're in the same terrain (except trap)
                if self.animal == 'rat' and terrain[self.row][self.col] != '1' and terrain[self.row][self.col] != \
                        terrain[row][col]:
                    # no animal(rat or elephant) in destination
                    if board[row][col] is not None:
                        continue
                if terrain[row][col] == '2':
                    if self.animal == 'rat':
                        moves.append(guess)
                    elif self.animal in ['tiger', 'lion']:
                        if self.row == 2 or self.row == 6:
                            if rat(col=self.col) is False:
                                row = 6 if self.row == 2 else 2
                            else:
                                continue
                        elif col == 1 or col == 4:
                            if rat(row, col) is False:
                                col += 2
                            else:
                                continue
                        else:
                            col -= 2
                    else:
                        continue

                if self.validEat(board, row, col):
                    if col == 3:
                        if row == 0 and self.color or row ==8 and not self.color:
                            continue
                    moves.append((row, col))

        return moves

    def move(self, board, dest_row, dest_col):
        """
        Move pieces,change starting to None, destination to pieces
        """
        board[dest_row][dest_col] = Piece(dest_row, dest_col, self.animal, self.color)
        board[self.row][self.col] = None
