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
SPEED_LIMIT = 30
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
            if self.y < 0:
                self.y = 0
                self.dy *= -1
            if self.x > WIDTH:
                self.x = WIDTH
                self.dx *= -1
            if self.y > HEIGHT:
                self.y = HEIGHT
                self.dy *= -1
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
            if abs(self.dx) > SPEED_LIMIT:
                self.dx /= self.dx
                self.dx *= SPEED_LIMIT
            if abs(self.dy) > SPEED_LIMIT:
                self.dy /= self.dy
                self.dy *= SPEED_LIMIT
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

    def draw(self):
        for marble in self.marbles:
            pygame.draw.circle(self.gameDisplay, black, (int(marble.x), int(marble.y)), 5)
        for grav in self.centers_of_gravity:
            pygame.draw.circle(self.gameDisplay, red, (grav[0], grav[1]), 10)
        # self.gameDisplay.fill(black, (STEP_SIZE*body_part[0], STEP_SIZE*body_part[1], STEP_SIZE, STEP_SIZE))
        # self.gameDisplay.fill(red, (self.food[0]*STEP_SIZE, self.food[1]*STEP_SIZE, STEP_SIZE, STEP_SIZE))
        # pygame.draw.line(self.gameDisplay, black, (10,10), (10, 30), 1)

    def move(self):

        for marble in self.marbles:
            for grav in self.centers_of_gravity:
                marble.apply_gravity(grav[0], grav[1])
            marble.move()

    def tick(self):
        now = time.time()
        if abs(self.tick_time - now) > TIME_STEP_SIZE:
            self.tick_time = now
            self.move()

    def start(self):
        self.end = False
        while not self.end:
            for event in pygame.event.get():
                if event.type == pygame.KEYUP:
                #     if event.key == pygame.K_LEFT:
                #         self.change_orientation('left')
                #     if event.key == pygame.K_RIGHT:
                #         self.change_orientation('right')
                #     if event.key == pygame.K_UP:
                #         self.change_orientation('up')
                #     if event.key == pygame.K_DOWN:
                #         self.change_orientation('down')
                    if event.key == pygame.K_m:
                        self.__init__()
                    if event.key == pygame.K_q:
                        self.end = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        pass
                    if event.key == pygame.K_RIGHT:
                        pass
                if event.type == pygame.QUIT:
                    self.end = True
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    self.centers_of_gravity.append(pos)
            self.tick()
            self.gameDisplay.fill(white)
            self.draw()
            pygame.display.update()
            self.clock.tick(60)
a = Game()
a.start()
