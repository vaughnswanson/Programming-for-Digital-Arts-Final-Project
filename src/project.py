import pygame
import random

def EnemyHealthSpeedGenerator():
    #give enemy random skill points from 1 to 5
    EnemyTotalPoints = random.randint(1, 5)
    
    #set base speed and health
    health = 1
    speed = 1
    
    #distribute points randomly between health and speed
    for _ in range(EnemyTotalPoints):
        if random.choice([True, False]):
            health += 1
        else:
            speed += 1

    return health, speed

#TODO: give enemys hitboxes
#TODO: give bullets hitboxes
#TODO: delete bullet after hitting a freak
#TODO: make bulltets thake away health from freaks
#TODO: implement main


class Freak():

    def __init__(self, pos=(0,0)):
        self.pos = pos
        self.health, self.speed = EnemyHealthSpeedGenerator()
        self.alive = True
        
        #load sprite
        self.sprite = pygame.image.load("assets/images/freak1.png").convert_alpha()
        #scale sprite
        self.sprite = pygame.transform.scale(self.sprite, (50, 50))
        #give sprite hitbox
        self.rect = self.sprite.get_rect(topleft=pos)


    def update(self, dt):
        if self.health <= 0:
            self.alive = False

            # if freak moves off scereen delete it
        if (self.pos[0] < 0 or self.pos[0] > 800 or
            self.pos[1] < 0 or self.pos[1] > 600):
            self.alive = False

    def draw(self, screen):
        
        screen.blit(self.sprite, self.rect.topleft)       

class Bullet():
    def __init__(self, pos=(0,0), direction=(0,0), speed=10):
        self.pos = pos
        self.direction = direction
        self.speed = speed
        self.alive = True

    def update(self, dt):
        # Update bullet position based on direction and speed
        self.pos = (self.pos[0] + self.direction[0] * self.speed*dt,
                    self.pos[1] + self.direction[1] * self.speed*dt)
        
        # Check if bullet is out of bounds ( 800x600 place holder)
        if (self.pos[0] < 0 or self.pos[0] > 800 or
            self.pos[1] < 0 or self.pos[1] > 600):
            self.alive = False

class Turret():
    def __init__ (self, pos=(0,0), fire_rate=2):
        self.pos = pos
        self.fire_rate = fire_rate  # bullets per second
        self.last_shot_time = 0

    def is_fireing(self, fire_rate):
        if pygame.MOUSEBUTTONDOWN:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time >= 2 / fire_rate:
                self.last_shot_time = current_time
                return True
        
def main():
    #initalise pygame
    pygame.init()

   
    pygame.display.set_caption("Hoard of Freaks")

    screen = pygame.display.set_mode((800, 600))
    screen.fill((0, 0, 0))
    
    clock = pygame.time.Clock()
    running = True
    freaks = [Freak(pos=(random.randint(0, 800), random.randint(0, 600))) for _ in range(5)]
 
    while running :
        #set delta time
        dt = clock.tick(60) / 1000 
        #event loop
        for event in pygame.event.get():
            #use quit to close program
            if event.type == pygame.QUIT:
                running = False
        #update freaks
        for freak in freaks:
            freak.update(dt)

        
        #delete dead freaks
        freaks = [freak for freak in freaks if freak.alive]

        #draw freaks
        for freak in freaks:
            freak.draw(screen)

        pygame.display.flip()
        
        

if __name__ == "__main__":
    main()