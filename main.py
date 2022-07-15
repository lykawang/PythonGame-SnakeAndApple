import random
import time
import pygame
from pygame.locals import *


SIZE = 40


class Snake:
    def __init__(self, frame, length):
        self.parent_screen = frame
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'  # randomly pick one

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
        # alternatively, could write pygame.display.update(), they only have just little different

    def move_left(self):
        if self.direction == 'right' and self.length > 1:
            pass
        else:
            self.direction = 'left'

    def move_right(self):
        if self.direction == 'left' and self.length > 1:
            pass
        else:
            self.direction = 'right'

    def move_up(self):
        if self.direction == 'down' and self.length > 1:
            pass
        else:
            self.direction = 'up'

    def move_down(self):
        if self.direction == 'up' and self.length > 1:
            pass
        else:
            self.direction = 'down'

    def walk(self):
        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)


class Apple:
    def __init__(self, frame):
        self.parent_screen = frame
        self.apple = pygame.image.load("resources/apple.jpg").convert()
        self.x = SIZE * random.randint(0, 19)
        self.y = SIZE * random.randint(0, 19)

    def draw(self):
        self.parent_screen.blit(self.apple, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0,19) * SIZE
        self.y = random.randint(0,19) * SIZE


class Game:

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake And Apple Game")
        pygame.mixer.init()
        self.play_background_music()
        self.frame = pygame.display.set_mode((800, 800))
        self.snake = Snake(self.frame, 1)
        self.snake.draw()
        self.apple = Apple(self.frame)
        self.apple.draw()

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play(loops=-1)

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/grass.jpeg")
        self.frame.blit(bg, (0, 0))

    def display_score(self):
        font = pygame.font.SysFont('arial-black', 20)
        score = font.render(f"Score: {self.snake.length-1}", True, (225, 225, 225))
        self.frame.blit(score, (670, 30))

    def is_collision(self, x1, y1, x2, y2):
        if x2 <= x1 < x2 + SIZE:
            if y2 <= y1 < y2 + SIZE:
                return True
        return False

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # collision with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            self.snake.increase_length()
            self.apple.move()

        # collision with itself
        for i in range(2, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("crash")
                raise "Game over"  # exception

        # collision with the boarder
        if self.snake.x[0]<0 or self.snake.x[0]>800 or self.snake.y[0]<0 or self.snake.y[0]>800:
            self.play_sound("crash")
            raise "Game over"  # exception

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('Verdana', 24)
        line1 = font.render(f"Game is over! Your score is {self.snake.length}", True, (255,0,0))
        self.frame.blit(line1, (100,350))
        line2 = font.render("To play again press Enter. To exit press Escape.", True, (255,0,0))
        self.frame.blit(line2, (100, 400))
        pygame.display.flip()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake = Snake(self.frame, 1)
        self.apple = Apple(self.frame)

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
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(.1)


if __name__ == "__main__":
    game = Game()
    game.run()




