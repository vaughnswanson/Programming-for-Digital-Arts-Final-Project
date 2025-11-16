import pygame
import random

def EnemyHealthSpeedGenerator():
    #give enemy random skill points from 1 to 5
    EnemyTotalPoints = random.randint(1, 5)
    
    #set base speed and health
    health = 1
    speed = 1
    
    #distribute points randomly between health and speed
    for points in EnemyTotalPoints:
        if random.choice([True, False]):
            health += 1
        else:
            speed += 1

    return health, speed

class Enemy():

    def __init__ (self, pos(0,0), health=1, speed=1):
        self.pos = pos
        self.health, self.speed = EnemyHealthSpeedGenerator()
        
        self.alive = True


    def update(self):
        if self.health <= 0:
            self.alive = False