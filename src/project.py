import pygame
import random

class Enemy():

    def __init__(self, pos(0,0), health, speed):
        self.pos = pos
        self.health = health
        self.speed = speed
        self.alive = True
