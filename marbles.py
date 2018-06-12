import tensorflow as tf
import copy
import time
import os
import pygame
import math
import random
import numpy as np

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0, 255, 0)
WIDTH = 1000
HEIGHT = 1000

TIME_STEP_SIZE = 0.02

MARBLE_WEIGHT = 20
SUN_WEIGHT = 400
BIG_G = 1

MARBLE_WIDTH = 5
PLAYER_WIDTH = 10
# os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(0,0)

class Game(object):

    class Marble(object):
        def __init__(self, id, gameDisplay):
            self.id = id
            self.x = random.randint(0, WIDTH)
            self.y = random.randint(0, HEIGHT)
            self.dx = random.randint(-5,5)
            self.dy = random.randint(-5,5)
            self.gameDisplay = gameDisplay
        def move(self):
            self.x += self.dx
            self.y += self.dy
            self.correct()
        def correct(self):
            if self.x < 0:
                self.x = 0
                self.dx *= -1
                self.dx /= 2
            if self.y < 0:
                self.y = 0
                self.dy *= -1
                self.dy /= 2
            if self.x > WIDTH:
                self.x = WIDTH
                self.dx *= -1
                self.dx /= 2
            if self.y > HEIGHT:
                self.y = HEIGHT
                self.dy *= -1
                self.dy /= 2
        def apply_gravity(self, to_x, to_y):
            force = BIG_G * MARBLE_WEIGHT * SUN_WEIGHT
            r = self.distance_to(to_x, to_y) * 2
            force /= r**2
            dx_to_g = abs(to_x - self.x)
            alpha = np.arcsin(dx_to_g/r)
            force_x = math.sin(alpha) * force
            force_y = math.cos(alpha) * force
            if to_x < self.x:
                force_x *= -1
            if to_y < self.y:
                force_y *= -1
            self.dx += force_x
            self.dy += force_y
        def distance_to(self, to_x, to_y):
            return math.sqrt( (to_x - self.x)**2 + (to_y - self.y)**2 )

    def __init__(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Marbles')
        self.clock = pygame.time.Clock()
        self.tick_time = time.time()
        self.marbles = [self.Marble(i, self.gameDisplay) for i in range(60)]
        self.centers_of_gravity = list()
        self.centers_of_gravity.append((random.randint(110, WIDTH-111),random.randint(100,HEIGHT-111)))

        self.player = [WIDTH//2, HEIGHT - 5]
        self.hit = 0

        self.x = tf.placeholder('float',[None, 400], name="self_x")
        self.y = tf.placeholder('float', name="self_y")
        self.classes = 4
        self.keep_rate = 0.8
        self.keep_prob = tf.placeholder(tf.float32)
        self.training = True

    def draw(self):
        for marble in self.marbles:
            pygame.draw.circle(self.gameDisplay, black, (int(marble.x), int(marble.y)), MARBLE_WIDTH)
        for grav in self.centers_of_gravity:
            pygame.draw.circle(self.gameDisplay, red, (grav[0], grav[1]), 10)

        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(str(SUN_WEIGHT), False, (255, 0, 0))
        self.gameDisplay.blit(textsurface,(10,10))
        textsurface = myfont.render(str(self.hit), False, (255, 0, 0))
        self.gameDisplay.blit(textsurface,(WIDTH - 40,10))
        
        pygame.draw.circle(self.gameDisplay, green, (self.player[0], self.player[1]), PLAYER_WIDTH)
        # self.gameDisplay.fill(black, (STEP_SIZE*body_part[0], STEP_SIZE*body_part[1], STEP_SIZE, STEP_SIZE))
        # self.gameDisplay.fill(red, (self.food[0]*STEP_SIZE, self.food[1]*STEP_SIZE, STEP_SIZE, STEP_SIZE))
        # pygame.draw.line(self.gameDisplay, black, (10,10), (10, 30), 1)

    def update_hits(self):
        remove_arr = []
        for i, marble in enumerate(self.marbles):
            if self.distance_player_marble(marble) < (MARBLE_WIDTH + PLAYER_WIDTH):
                self.hit += 1
                remove_arr.append(i)
        for i in remove_arr:
            del self.marbles[i]

    def distance_player_marble(self, marble):
        return math.sqrt((self.player[0] - marble.x)**2 + (self.player[1] - marble.y)**2)

    def move(self):

        for marble in self.marbles:
            for grav in self.centers_of_gravity:
                marble.apply_gravity(grav[0], grav[1])
            marble.move()

    def player_move(self, direction):
        if direction == 'left':
            if self.player[0] > 0:
                self.player[0] -= 10
        if direction == 'right':
            if self.player[0] < WIDTH:
                self.player[0] += 10
        if direction == 'up':
            if self.player[1] > 0:
                self.player[1] -= 10
        if direction == 'down':
            if self.player[1] < HEIGHT:
                self.player[1] += 10

    def tick(self):
        now = time.time()
        if abs(self.tick_time - now) > TIME_STEP_SIZE:
            self.tick_time = now
            self.move()

    def start(self):
        global SUN_WEIGHT
        self.end = False
        pause = False
        while not self.end:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player_move('left')
                    if event.key == pygame.K_d:
                        self.player_move('right')
                    if event.key == pygame.K_w:
                        self.player_move('up')
                    if event.key == pygame.K_s:
                        self.player_move('down')
                    if event.key == pygame.K_p:
                        pause = not pause
                    if event.key == pygame.K_r:
                        self.__init__()
                    if event.key == pygame.K_q:
                        self.end = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        SUN_WEIGHT -= 100
                        print(SUN_WEIGHT)
                    if event.key == pygame.K_RIGHT:
                        SUN_WEIGHT += 100
                        print(SUN_WEIGHT)
                if event.type == pygame.QUIT:
                    self.end = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.centers_of_gravity.append(pos)
            if not pause:
                self.tick()
            self.gameDisplay.fill(white)
            self.update_hits()
            self.draw()
            pygame.display.update()
            self.clock.tick(60)
a = Game()
a.start()
