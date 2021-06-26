import pygame
import random
import math
from pygame import mixer

# Initialise pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')

# Background Sound
mixer.music.load('background.wav')
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption('Space Invaders')
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

NUM_ENEMIES = 6
GAMEOVER = 440
score_value = 0


class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def setX(self, x):
        self.x = x

    def setY(self, y):
        self.y = y


class Character(Point):
    def __init__(self, x, y, img, x_change, y_change):
        Point.__init__(self, x, y)
        self.img = pygame.image.load(img)
        self.x_change = x_change
        self.y_change = y_change

    def getImg(self):
        return self.img

    def getX_change(self):
        return self.x_change

    def getY_change(self):
        return self.y_change

    def setY_change(self, ychange):
        self.y_change = ychange

    def setX_change(self, xchange):
        self.x_change = xchange

    def move(self):
        """Move x and y by x_change and y_change"""
        self.setX(self.getX() + self.getX_change())
        self.setY(self.getY() + self.getY_change())

    def blit(self):
        screen.blit(self.getImg(), (self.getX(), self.getY()))


class Player(Character):
    def __init__(self):
        Character.__init__(self, 370, 480, 'player.png', 0, 0)

    def move(self):
        Character.move(self)
        x = self.getX()
        if x <= 0:
            self.setX(0)
        elif x >= 736:
            self.setX(736)


class Enemy(Character):
    def __init__(self):
        Character.__init__(self, random.randint(0, 736), random.randint(50, 150), 'enemy.png', 0.2, 40)

    def move(self):
        x = self.getX()
        y = self.getY()

        self.setX(x + self.getX_change())
        x = self.getX()

        if x <= 0 or x >= 736:
            self.setX_change(-self.getX_change())
            self.setY(y + self.getY_change())

    def gameOver(self):
        if self.getY() > GAMEOVER:
            return True


class Bullet(Character):
    def __init__(self, x):
        Character.__init__(self, x, 480, 'bullet.png', 0, -1)
        self.state = True

    def getBulletState(self):
        return self.state

    def setBulletState(self, state):
        self.state = state

    def isCollision(self, other):
        selfX = self.getX()
        selfY = self.getY()
        otherX = other.getX()
        otherY = other.getY()
        distance = math.sqrt(math.pow(selfX - otherX, 2) + math.pow(selfY - otherY, 2))

        return True if distance < 27 else False

    def blit(self):
        screen.blit(self.getImg(), (self.getX() + 16, self.getY() + 10))

    def setState(self, val):
        self.state = val


class Text(Point):
    def __init__(self, x, y, fontstyle, size, rgb):
        Point.__init__(self, x, y)
        self.font = pygame.font.Font(fontstyle, size)
        self.rgb = rgb

    def show_Text(self, string):
        text = self.font.render(string, True, self.rgb)
        screen.blit(text, (self.getX(), self.getY()))


def createEnemy(enemies):
    """Create Enemies and append into enemies list"""
    enemies.append(Enemy())


def main():
    bullet = None
    player = Player()
    enemies = []

    for i in range(NUM_ENEMIES):
        createEnemy(enemies)

    running = True
    global score_value
    score = Text(10, 10, 'freesansbold.ttf', 32, (255, 255, 255))
    game_over = Text(200, 250, 'freesansbold.ttf', 64, (255, 255, 255))

    while running:
        # RGB
        screen.fill((0, 0, 0))

        # background image
        screen.blit(background, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # if keystroke is pressed, checked whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.setX_change(-0.3)
                if event.key == pygame.K_RIGHT:
                    player.setX_change(0.3)

                if not bullet and event.key == pygame.K_SPACE:
                    bullet = Bullet(player.getX())
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bullet.blit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.setX_change(0)

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()

        if enemies:
            for enemy in enemies:
                enemy.move()

                if enemy.gameOver():
                    enemies.clear()
                    break

                if bullet:
                    collision = bullet.isCollision(enemy)
                    if collision:
                        explosion_Sound = mixer.Sound('explosion.wav')
                        explosion_Sound.play()
                        bullet = None
                        score_value += 1
                        enemies.remove(enemy)
                        createEnemy(enemies)

                enemy.blit()
        else:
            game_over.show_Text('GAME OVER')

        if bullet:
            bullet.move()
            bullet.blit()

            if bullet.getY() <= 0:
                bullet = None

        player.move()
        player.blit()
        score.show_Text('Score: ' + str(score_value))
        pygame.display.update()


if __name__ == '__main__':
    main()
