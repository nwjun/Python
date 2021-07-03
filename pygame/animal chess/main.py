# Import libraries
import pygame as pg
from piece import Piece
import os

# Initialize
pg.init()
WIDTH, HEIGHT = 600, 750
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('斗兽棋 Jungle')
icon = pg.image.load(os.path.join("assets","icon.png"))
pg.display.set_icon(icon)
# Board Set Up
GRID = 70
START_X = (WIDTH - GRID * 7) / 2  # Starting point of board
START_Y = (HEIGHT - GRID * 9) / 2

COLORS = {
    "red": (172, 50, 50),
    "green": (67, 141, 90),
    "black": (0, 0, 0),
    "white": (255, 255, 255),
}


def draw_terrain():
    """
    Draw terrain
    """
    terrain = [["0" for i in range(7)] for i in range(9)]

    # trap
    for i in [0, 8]:
        for j in [2, 4]:
            terrain[i][j] = '1'
    terrain[1][3] = "1"
    terrain[7][3] = "1"

    # river
    for i in [3, 4, 5]:
        for j in [1, 2, 4, 5]:
            terrain[i][j] = '2'

    # hole
    terrain[0][3] = '3'
    terrain[8][3] = '3'

    return terrain


def draw_board(terrain):
    """
    Display board onto screen
    """
    river = pg.transform.scale(pg.image.load(os.path.join("assets", 'river.png')), (GRID * 2, GRID * 3))
    trap = pg.transform.scale(pg.image.load(os.path.join("assets", 'trap.png')), (GRID, GRID))
    king = pg.transform.scale(pg.image.load(os.path.join("assets", 'king.png')), (GRID, GRID))
    tiles = {
        "1": trap,
        "3": king,
    }

    for i in range(9):
        for j in range(7):
            if i == 3:
                if j == 1 or j == 4:
                    window.blit(river, start_pos(i, j))
            if terrain[i][j] != '2' and terrain[i][j]!='0':
                # pg.draw.rect(surface, rgb,((left, top), (width, height))
                window.blit(tiles[terrain[i][j]], start_pos(i, j))
            pg.draw.rect(window, (0, 0, 0), ((GRID * j + START_X, GRID * i + START_Y), (GRID, GRID)), 3)


def reset():
    """
    Reset the pieces to original place. 
    Return multidimensional list containing the pieces
    """
    PIECES = {
        (0, 0): 'lion',
        (0, 6): 'tiger',
        (1, 1): 'dog',
        (1, 5): 'cat',
        (2, 0): 'rat',
        (2, 2): 'leopard',
        (2, 4): 'wolf',
        (2, 6): 'elephant'

    }

    board = [[None for i in range(7)] for i in range(9)]
    for i in PIECES.keys():
        animal = PIECES[i]
        row, col = i
        board[row][col] = Piece(row, col, animal, True)
        # flip
        row = 8 - row
        col = 6 - col
        board[row][col] = Piece(row, col, animal, False)

    return board


def start_pos(row, col):
    """
    Return left corner position
    """
    return (GRID * col + START_X, GRID * row + START_Y)


def print_pieces(board):
    """
    Print pieces to screen if board[i][j] != None
    """
    MINIMIZE = 10
    for i in range(9):
        for j in range(7):
            if board[i][j]:
                piece = board[i][j]
                img_loc = piece.img
                img = pg.transform.scale(pg.image.load(img_loc), (GRID - MINIMIZE, GRID - MINIMIZE))
                x, y = start_pos(i, j)
                window.blit(img, (x + MINIMIZE / 2, y + MINIMIZE / 2))


def in_board(x, y):
    if x > START_X and x < START_X + GRID * 7 and y > START_Y and y < START_Y + GRID * 9:
        return True
    return False


def show_mouse_loc(player):
    color = (255, 0, 0) if player else (0, 255, 0)
    x, y = pg.mouse.get_pos()
    if in_board(x, y):
        col = int((x - START_X) // GRID)
        row = int((y - START_Y) // GRID)
        pg.draw.rect(window, color, (start_pos(row, col), (GRID, GRID)), 3)
        return row, col
    else:
        return None, None


def main():
    FPS = 60
    clock = pg.time.Clock()
    run = True
    terrain = draw_terrain()
    board = reset()
    choose_piece = False
    start_row, start_col = None, None
    player = True
    player_font = pg.font.Font('freesansbold.ttf', 20)

    def win():
        if board[0][3]:
            return 2
        elif board[8][3]:
            return 1
        else:
            return 0

    while run:
        clock.tick(FPS)
        window.fill(COLORS['white'])
        draw_board(terrain)
        print_pieces(board)
        row, col = show_mouse_loc(player)
        if player:
            player_text = "Player 1"
            player_color = COLORS["red"]
        else:
            player_text = "Player 2"
            player_color = COLORS['green']
        player_label = player_font.render("Turn: " + player_text, True, player_color)
        window.blit(player_label, (START_X, START_Y - player_label.get_height() * 1.1))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and row is not None:
                selected = board[row][col]
                if choose_piece:
                    if (row, col) in moves:
                        board[start_row][start_col].move(board, row, col)
                        player = not player  # change player
                    choose_piece = False
                elif not choose_piece and selected is not None:
                    if selected.color == player:
                        choose_piece = True
                        start_row, start_col = row, col
                        moves = selected.validMove(board, terrain)

        if choose_piece:
            for move in moves:
                row, col = move
                x, y = start_pos(row, col)
                pg.draw.circle(window, (100, 100, 100), (x + GRID / 2, y + GRID / 2), 5)

        winner = win()
        if winner:
            run = False
            return winner

        pg.display.update()


def main_menu():
    title_font = pg.font.SysFont("comicsans", 40)
    run = True
    winner = None
    title_label = title_font.render("Red Goes First. Press Mouse to Begin", True, (0, 0, 0))
    s = pg.Surface((WIDTH, HEIGHT))
    s.set_alpha(128)
    s.fill(COLORS['white'])
    while run:
        window.blit(s, (0, 0))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.MOUSEBUTTONDOWN:
                winner = main()
        if winner:
            winner_label = title_font.render("Winner: Player " + str(winner), True,
                                             COLORS["red" if winner == 1 else "green"])
            window.blit(winner_label,
                        (WIDTH / 2 - winner_label.get_width() / 2, HEIGHT / 2 - winner_label.get_height() / 2))
        else:
            window.blit(title_label,
                        (WIDTH / 2 - title_label.get_width() / 2, HEIGHT / 2 - title_label.get_height() / 2))
        pg.display.update()
    pg.quit()


if __name__ == '__main__':
    main_menu()
