import pygame
from pygame.locals import *
import time
import random

# from PIL import Image

import os

os.chdir(
    os.path.dirname(
        os.path.abspath("C:/Users/HP/Desktop/visiual studio code/snake_game/resources")
    )
)

colour = (10, 54, 3)
SIZE = 40


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        # self.image= pygame.image.load("resources/apple_download.png")
        self.image = pygame.image.load("resources/apple_download.png").convert_alpha()
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 24) * SIZE
        self.y = random.randint(0, 17) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        # self.score=length-1
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/green_block.png")
        self.snake_head_down = pygame.image.load("resources/snake_head_down.png")
        self.snake_head_up = pygame.image.load("resources/snake_head_up.png")
        self.snake_head_right = pygame.image.load("resources/snake_head_right.png")
        self.snake_head_left = pygame.image.load("resources/snake_head_left.png")
        # self.snake_head = Image.open("resources/snake_head.png")

        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = "down"

    def draw(self, dir):
        self.dir = dir
        if self.dir == "left":
            self.parent_screen.blit(self.snake_head_left, (self.x[0], self.y[0]))
        if self.dir == "right":
            self.parent_screen.blit(self.snake_head_right, (self.x[0], self.y[0]))
        if self.dir == "up":
            self.parent_screen.blit(self.snake_head_up, (self.x[0], self.y[0]))
        if self.dir == "down":
            self.parent_screen.blit(self.snake_head_down, (self.x[0], self.y[0]))

        for i in range(self.length - 1, 0, -1):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        # pygame.display.flip()

    def increase_lenght(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    # def rot_center(image, angle, x, y):

    # rotated_image = pygame.transform.rotate(image, angle)
    # new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    # return rotated_image, new_rect

    def move_right(self):
        self.direction = "right"

    def move_left(self):
        self.direction = "left"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):

        if self.direction == "right":
            # self.x[0]= self.snake_head.rotate(-90)
            # self.x[0]= pygame.transform.rotate(self.snake_head,90)
            self.x[0] += SIZE
            if self.x[0] > 1000:
                self.x[0] = 0

            self.draw(self.direction)

        if self.direction == "left":
            # self.x[0]= self.snake_head.rotate(90)
            self.x[0] -= SIZE
            if self.x[0] < 0:
                self.x[0] = 1000

            self.draw(self.direction)

        if self.direction == "up":
            # self.x[0]= self.snake_head.rotate(180)
            self.y[0] -= SIZE
            if self.y[0] < 0:
                self.y[0] = 720
            self.draw(self.direction)

        if self.direction == "down":
            # self.x[0]= self.snake_head.rotate(360)
            self.y[0] += SIZE
            if self.y[0] > 720:
                self.y[0] = 0
            self.draw(self.direction)

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.play_bg_music()
        self.surface = pygame.display.set_mode((1000, 720))
        self.surface.fill(colour)
        # self.game_over_surface= pygame.display.set_mode((500,360))
        # self.game_over_surface.fill(255, 255, 255)
        self.snake = Snake(self.surface, 1)
        self.snake.draw(self.snake.direction)
        self.apple = Apple(self.surface)
        self.apple.draw()

    def display_score(self):
        font = pygame.font.SysFont("arial", 30)
        score = font.render(f"Score:{(self.snake.length-1)*5}", True, (255, 255, 255))
        self.surface.blit(score, (800, 10))
        pygame.display.flip()

    def is_collision(self, x1, x2, y1, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y2 >= y1 and y2 < y1 + SIZE:
                return True
        return False

    # def is_boundary_crash(self, x1, y1):
    # if x1>1000 or x1<0 or y1>720 or y1<0:
    # return True
    # return False

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def play_bg_music(self):
        bg_music = pygame.mixer.music.load("resources/snake_bg_music.mp3")
        pygame.mixer.music.play(loops=-1)

    def render_beckground(self):
        bg = pygame.image.load("resources/background_9.jpg")
        self.surface.blit(bg, (0, 0))

    def render_game_over_beckground(self):
        bg_1 = pygame.image.load("resources/game_over_bg.png")
        self.surface.blit(bg_1, (0, 0))

    def play(self):
        self.render_beckground()
        self.snake.walk()
        self.apple.draw()
        self.display_score()

        pygame.display.flip()

        if self.is_collision(
            self.apple.x, self.snake.x[0], self.apple.y, self.snake.y[0]
        ):
            self.play_sound("eating")
            self.snake.increase_lenght()
            self.apple.move()

        for i in range(3, self.snake.length):
            if self.is_collision(
                self.snake.x[i], self.snake.x[0], self.snake.y[i], self.snake.y[0]
            ):
                self.play_sound("crash_1")
                time.sleep(2)
                raise "game over"

        # if self.is_boundary_crash(self.snake.x[0], self.snake.y[0]):
        # self.play_sound("crash")
        # time.sleep(2)
        # raise "game over"

    def show_game_over(self):
        # self.render_beckground()
        self.render_game_over_beckground()
        # self.game_over_surface= pygame.display.set_mode((500,360))
        # self.game_over_surface.fill(255, 255, 255)
        font = pygame.font.SysFont("minecraft", 60)
        line1 = font.render(f"GAME OVER", True, (0, 0, 0))
        self.surface.blit(line1, (50, 50))

        line2 = font.render(f"SCORE: {(self.snake.length-1)*5}", True, (0, 0, 0))
        self.surface.blit(line2, (50, 125))

        line3 = font.render(f"TO PLAY AGAIN PRESS ENTER ", True, (0, 0, 0))
        self.surface.blit(line3, (50, 200))

        line4 = font.render(f"TO EXIT PRESS ESCAPE", True, (0, 0, 0))
        self.surface.blit(line4, (50, 275))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)

    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.play()
                        pause = False

                    if not pause:
                        if event.key == K_RIGHT:
                            if not (self.snake.direction == "left"):
                                self.snake.move_right()

                        elif event.key == K_LEFT:
                            if not (self.snake.direction == "right"):
                                self.snake.move_left()

                        elif event.key == K_UP:
                            if not (self.snake.direction == "down"):
                                self.snake.move_up()

                        elif event.key == K_DOWN:
                            if not (self.snake.direction == "up"):
                                self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
