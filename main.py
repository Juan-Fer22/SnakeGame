import sys
import random
import time
import pygame
from pygame.locals import *

# size of window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
INCREMENT_SIZE = 40
SPEED_GAME = 60

# colors for the game
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
POISSON_APPLE = (218, 168, 168)


score = 10


class Snake:
    def __init__(self):
        self.size = INCREMENT_SIZE
        self.body = [(100, 100), (80, 100), (60, 100)]
        self.direction = (1, 0)
        self.speed = 25

    def move(self, deltaTime):
        headX, headY = self.body[0]
        dirX, dirY = self.direction
        newHead = (headX + dirX * self.size * deltaTime * self.speed, headY + dirY * self.size * deltaTime * self.speed)

        if newHead[0] >= SCREEN_WIDTH:
            newHead = (0, newHead[1])
        elif newHead[0] < 0:  # Si se va fuera del borde izquierdo, aparece en el derecho
            newHead = (SCREEN_WIDTH - self.size, newHead[1])

            # Si se va fuera del borde inferior, aparece en la parte superior
        if newHead[1] >= SCREEN_HEIGHT:
            newHead = (newHead[0], 0)
        elif newHead[1] < 0:  # Si se va fuera del borde superior, aparece en la parte inferior
            newHead = (newHead[0], SCREEN_HEIGHT - self.size)

        self.body.insert(0, newHead)
        self.body.pop()

    def changeDirection(self, direction):
        if (self.direction[0] * -1, self.direction[1] * -1) != direction:
            self.direction = direction

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (*segment, self.size, self.size))

    def grow(self):
        global score
        score += 10
        self.body.append(self.body[-1])

    def shrink(self, damage, gameWindow):
        global score
        score -= 10 * damage
        for _ in range(0, damage):
            if not self.body:
                gameOver(gameWindow)
            self.body.pop()

    def checkCollision(self, gameWindow):
        if len(self.body) == 0:
            gameOver(gameWindow)
        return self.body[0] in self.body[1:]

    def checkCollitionWithApple(self, apple, gameWindow):
        if len(self.body) == 0:
            gameOver(gameWindow)

        head_x, head_y = self.body[0]

        # Verificamos si la cabeza de la serpiente toca la manzana
        if (head_x < apple.position[0] + apple.size and head_x + self.size > apple.position[0]) and \
                (head_y < apple.position[1] + apple.size and head_y + self.size > apple.position[1]):
            return True
        return False


class Apple:
    def __init__(self):
        self.size = INCREMENT_SIZE
        self.position = (random.randint(0, (SCREEN_WIDTH - self.size) // self.size) * self.size,
                         random.randint(0, (SCREEN_HEIGHT - self.size) // self.size) * self.size)

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, (*self.position, self.size, self.size))

    def randomPosition(self, snake):
        goodPosition = False
        while not goodPosition:
            self.position = (random.randint(0, (SCREEN_WIDTH - self.size) // self.size) * self.size,
                             random.randint(0, (SCREEN_HEIGHT - self.size) // self.size) * self.size)
            if snake.body is None or self.position not in snake.body:
                goodPosition = True


class PoissonApple(Apple):
    def __init__(self):
        super().__init__()
        self.damage = random.randint(0, 5)


# def mainMenu():

def showScore(choice, color, font, size, gameWindow):
    scoreFont = pygame.font.SysFont(font, size)

    scoreSurface = scoreFont.render('Score : ' + str(score), True, color)

    score_rect = scoreSurface.get_rect()

    gameWindow.blit(scoreSurface, score_rect)


def gameOver(gameWindow):
    global score
    myFont = pygame.font.SysFont('times new roman', 50)

    if score < 0:
        score = 0

    gameOverSurface = myFont.render(
        'Your Score is : ' + str(score), True, RED)

    # create a rectangular object for the text
    # surface object
    gameOverRect = gameOverSurface.get_rect()

    # setting position of the text
    gameOverRect.midtop = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)

    # blit will draw the text on screen
    gameWindow.blit(gameOverSurface, gameOverRect)
    pygame.display.flip()

    # after 2 seconds we will quit the program
    time.sleep(2)

    # deactivating pygame library
    pygame.quit()

    # quit the program
    quit()


def playMenu():
    global score
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Snake Game")
    snake = Snake()
    apple = Apple()
    poissonApple = PoissonApple()

    fps = pygame.time.Clock()

    exitGame = False

    while not exitGame:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:  # Movimiento hacia la izquierda
            snake.changeDirection((-1, 0))
        if keys[pygame.K_RIGHT]:  # Movimiento hacia la derecha
            snake.changeDirection((1, 0))
        if keys[pygame.K_UP]:  # Movimiento hacia arriba
            snake.changeDirection((0, -1))
        if keys[pygame.K_DOWN]:  # Movimiento hacia abajo
            snake.changeDirection((0, 1))

        last_update_time = pygame.time.get_ticks()
        delta_time = fps.tick(60) / 1000.0  # Tiempo entre frames

        snake.move(delta_time)

        if snake.checkCollitionWithApple(apple, screen):
            snake.grow()
            apple.randomPosition(snake)

        if snake.checkCollitionWithApple(poissonApple, screen):
            snake.shrink(poissonApple.damage, screen)
            poissonApple = PoissonApple()

        if snake.checkCollision(screen):
            gameOver(screen)
            exitGame = True

        if score <= 0:
            gameOver(screen)

        showScore(1, WHITE, 'times new roman', 30, screen)

        snake.draw(screen)
        apple.draw(screen, RED)
        poissonApple.draw(screen, POISSON_APPLE)
        pygame.display.update()
        fps.tick(SPEED_GAME)

    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    playMenu()
