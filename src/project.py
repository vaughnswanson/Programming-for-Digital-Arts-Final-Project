import pygame
import random

class Enemy():

    def __init__(self, pos(0,0), health, speed):
        self.pos = pos
        self.health = health #add random health from 1-5
        self.speed = speed # assign random speed from 1-3
        self.alive = True

    def update(self):
        if self.health <= 0:
            self.alive = False