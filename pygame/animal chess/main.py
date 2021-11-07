# Import libraries
import pygame as pg
from piece import Piece
import os
import sys

# Initialize
pg.init()
WIDTH, HEIGHT = 600, 750
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('斗兽棋 Jungle')
icon = pg.image.load(os.path.join("assets", "icon.png"))
pg.display.set_icon(icon)
FPS = 60
clock = pg.time.Clock()
pg.mixer.music.load(os.path.join('assets', 'background.wav'))
pg.mixer.music.play(-1)

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

s = pg.Surface((WIDTH, HEIGHT))
s.set_alpha(128)
s.fill(COLORS['white'])

menu_font = pg.font.Font(os.path.join("assets", "8-BIT WONDER.TTF"), 40)


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
    river = pg.transform.scale(pg.image.load(
        os.path.join("assets", 'river.png')), (GRID * 2, GRID * 3))
    trap = pg.transform.scale(pg.image.load(
        os.path.join("assets", 'trap.png')), (GRID, GRID))
    king = pg.transform.scale(pg.image.load(
        os.path.join("assets", 'king.png')), (GRID, GRID))
    tiles = {
        "1": trap,
        "3": king,
    }

    for i in range(9):
        for j in range(7):
            if i == 3:
                if j == 1 or j == 4:
                    window.blit(river, start_pos(i, j))
            if terrain[i][j] != '2' and terrain[i][j] != '0':
                # pg.draw.rect(surface, rgb,((left, top), (width, height))
                window.blit(tiles[terrain[i][j]], start_pos(i, j))
            pg.draw.rect(window, (0, 0, 0), ((GRID * j + START_X,
                         GRID * i + START_Y), (GRID, GRID)), 3)


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
    MINIMIZE = 30
    num_font = pg.font.Font('freesansbold.ttf', 20)

    for i in range(9):
        for j in range(7):
            if board[i][j]:
                piece = board[i][j]
                color = 'red' if piece.color else 'green'
                num = num_font.render(str(piece.val), True, COLORS[color])
                img_loc = piece.img
                img = pg.transform.scale(pg.image.load(
                    img_loc), (GRID - MINIMIZE, GRID - MINIMIZE))
                x, y = start_pos(i, j)
                window.blit(num, (x + MINIMIZE, y+MINIMIZE*0.2))
                window.blit(img, (x + MINIMIZE / 2, y + MINIMIZE / 2 + 10))


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
    run = True
    terrain = draw_terrain()
    board = reset()
    choose_piece = False
    start_row, start_col = None, None
    player = True
    player_font = pg.font.Font('freesansbold.ttf', 20)
    player1 = [1, 2, 3, 4, 5, 6, 7, 8]
    player2 = [1, 2, 3, 4, 5, 6, 7, 8]
    pause = False
    move_sound = pg.mixer.Sound(os.path.join("assets", "move-sound.mp3"))
    move_sound_playing = False

    pause_color = COLORS['black']
    icon = player_font.render("ll", True, pause_color)

    mute = False
    muteImg = pg.image.load(os.path.join('assets', 'mute.png')) # Icon made by Pixel perfect from www.flaticon.com
    muteImg = pg.transform.scale(muteImg, (25, 25))
    muteImg.convert()  # optimise image format and makes drawing faster
    muteRect = muteImg.get_rect()  # returns a Rect object from an image
    muteRect.center = WIDTH - muteImg.get_width()//2 - icon.get_width() - \
        70, 30 - muteImg.get_height()//2 + 11

    def win():
        if board[0][3] or not player1:
            return 2
        elif board[8][3] or not player2:
            return 1
        else:
            return 0

    while run:
        clock.tick(FPS)
        window.fill(COLORS['white'])
        draw_board(terrain)
        print_pieces(board)
        row, col = show_mouse_loc(player)
        window.blit(muteImg, muteRect)
        pg.draw.rect(window, "#ffffff", muteRect, 1)

        if player:
            player_text = "Player 1"
            player_color = COLORS["red"]
        else:
            player_text = "Player 2"
            player_color = COLORS['green']
        player_label = player_font.render(
            "Turn: " + player_text, True, player_color)
        window.blit(player_label, (START_X, START_Y -
                    player_label.get_height() * 1.1))

        if not pause:
            circle = pg.draw.circle(
                window, COLORS["black"], center=(550, 30), radius=15, width=3)
            if circle.collidepoint(pg.mouse.get_pos()):
                pause_color = (255, 0, 0)
            else:
                pause_color = COLORS['black']
            window.blit(icon, (550 - icon.get_width() / 2,
                        30 - icon.get_height() / 2 + 1))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    pause = not pause

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if not pause:
                    if circle.collidepoint(pg.mouse.get_pos()):
                        pause = True

                    if muteRect.collidepoint(pg.mouse.get_pos()):
                        mute = not mute
                        pg.mixer.music.pause() if mute else pg.mixer.music.unpause()

                    if row is not None:
                        selected = board[row][col]
                        if move_sound_playing:
                            move_sound_playing = False
                            move_sound.stop()
                        if choose_piece:
                            if (row, col) in moves:
                                move_sound.play()
                                move_sound_playing = True
                                eaten = board[row][col]
                                if eaten:
                                    if player:
                                        player2.remove(eaten.val)
                                    else:
                                        player1.remove(eaten.val)
                                board[start_row][start_col].move(
                                    board, row, col)
                                player = not player  # change player
                            choose_piece = False

                        elif not choose_piece and selected is not None:
                            if selected.color == player:
                                choose_piece = True
                                start_row, start_col = row, col
                                moves = selected.validMove(board, terrain)
                else:
                    pause = False

        if choose_piece:
            for move in moves:
                row, col = move
                x, y = start_pos(row, col)
                pg.draw.circle(window, (100, 100, 100),
                               (x + GRID / 2, y + GRID / 2), 5)

        winner = win()

        if winner:
            run = False
        if pause:
            pause_label = menu_font.render("PAUSE", True, COLORS["black"])
            window.blit(s, (0, 0))
            window.blit(pause_label,
                        (WIDTH / 2 - pause_label.get_width() / 2, HEIGHT / 2 - pause_label.get_height() / 2))
        pg.display.update()
    win_menu(winner)


class Option:
    sound = pg.mixer.Sound(os.path.join("assets", "select-sound.wav"))
    option_font = pg.font.Font(os.path.join("assets", "8-BIT WONDER.TTF"), 32)
    rect_width = 400
    rect_height = 90
    start_height = 425
    gap = 30
    color = (0, 0, 102)

    def __init__(self, text, num):
        self.text_label = self.option_font.render(text, True, self.color)
        self.text = text
        self.num = num
        self.rect = pg.Rect(WIDTH / 2 - self.rect_width / 2,
                            self.start_height + self.num *
                            (self.rect_height + self.gap),
                            self.rect_width,
                            self.rect_height)

    def show_screen(self, color=color, change=None):
        pg.draw.rect(window, color, self.rect, 3, 5)
        if change:
            text_label = change
        else:
            text_label = self.text_label

        window.blit(text_label,
                    (WIDTH / 2 - text_label.get_width() / 2,
                     self.start_height + self.num * (
                        self.rect_height + self.gap) + self.rect_height / 2 - text_label.get_height() / 2))

    def mouse_touch(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            self.hover()
            return True
        else:
            return False

    def hover(self):
        color = (102, 0, 0)
        changed_text = self.option_font.render(self.text, True, color)
        self.show_screen(color, changed_text)

    def play_sound(self):
        self.sound.play()


def rules():
    print('hi')
    pass


def win_menu(winner):
    play_again = Option("PLAY AGAIN", 0)
    run = True
    play = False

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    play_again.play_sound()
                    main()

            if play and event.type == pg.MOUSEBUTTONDOWN:
                run = False
                main()

        window.blit(s, (0, 0))
        winner_label = menu_font.render("Player " + str(winner) + " WIN", True,
                                        COLORS["red" if winner == 1 else "green"])
        window.blit(winner_label,
                    (WIDTH / 2 - winner_label.get_width() / 2, HEIGHT / 2.75 - winner_label.get_height() / 2))
        play_again.show_screen()
        play = play_again.mouse_touch()
        pg.display.update()


def main_menu():
    run = True
    menu_label = menu_font.render("Jungle", True, (0, 0, 102))
    bg = pg.image.load(os.path.join("assets", "background.png"))

    options = []
    options.append(Option("PLAY", 0))
    options.append(Option("RULES", 1))
    options_dict = {
        "PLAY": main,
        "RULES": rules,
    }
    selection = 0

    while run:
        window.blit(bg, (0, 0))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                options[selection].play_sound()
                options_dict[options[selection].text]()

            if event.type == pg.KEYDOWN:
                options[selection].play_sound()
                if event.key == pg.K_DOWN:
                    selection += 1
                if event.key == pg.K_UP:
                    selection -= 1
                if event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN:
                    options_dict[options[selection].text]()

        for index, option in enumerate(options):
            option.show_screen()
            if option.mouse_touch():
                if index != selection:
                    options[selection].play_sound()
                    selection = index
            window.blit(menu_label,
                        (WIDTH / 2 - menu_label.get_width() / 2, HEIGHT / 2.75 - menu_label.get_height() / 2))
            options[selection].hover()

        if selection >= len(options):
            selection = 0
        if selection < 0:
            selection = len(options) - 1

        pg.display.update()
    pg.quit()


if __name__ == '__main__':
    main_menu()
