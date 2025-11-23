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

def pick_freak():
    num = random.randrange(1,6)
    return f"freak{num}.png"
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
        self.sprite = pygame.image.load(f"assets/images/{pick_freak()}").convert_alpha()
        #scale sprite
        self.sprite = pygame.transform.scale(self.sprite, (96,96))
        #give sprite hitbox
        self.rect = self.sprite.get_rect(topleft=pos)
        
        self.spawn_rate = .5  # freaks per second

    def update(self, dt):
        #delete the freak if its health falls to 0 or below
        if self.health <= 0:
            self.alive = False
        self._update_pos(dt)
            
        # if freak moves off scereen delete it
        if self.pos[0] <= 0:
           
            self.alive = False
        
        #update rect position
        self.rect.topleft = self.pos




    def draw(self, screen):
        
        screen.blit(self.sprite, self.rect.topleft)     

    def _update_pos(self, dt):
        x,y = self.pos
        x -= self.speed * dt * 15
        self.pos = (x,y)  

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


  
    
    clock = pygame.time.Clock()
    running = True
    resolution = (1920,1080)
    screen = pygame.display.set_mode((resolution))
    freak_spawn_timer = 0
    freak_spawn_rate = .5  # freaks per second
    #spawn freak at random y position on right side of screen
    freaks = []
    #background = pygame.image.load("assets/images/HoardOfFreaks_Background.png").convert()
    #make the background black
    background = pygame.Surface(resolution)
    background.fill((0, 0, 0))
    background = pygame.transform.scale(background, resolution)

    while running :
        #set delta time
        dt = clock.tick(60) / 1000 
        #event loop
        for event in pygame.event.get():
            #use quit to close program
            if event.type == pygame.QUIT:
                running = False
        screen.blit(background, (0,0))
        
        #update freaks
        for freak in freaks:
            freak.update(dt)

        freak_spawn_timer += dt
        while freak_spawn_timer >= 1 / freak_spawn_rate:
            freak_spawn_timer -= 1 / freak_spawn_rate       

            y = random.choice(range(0, resolution[1]-96,96))
            freaks.append(Freak(pos=(resolution[0], y)))


        #delete dead freaks
        freaks = [freak for freak in freaks if freak.alive]

        #draw freaks
        for freak in freaks:
            freak.draw(screen)

        pygame.display.flip()
        
        

if __name__ == "__main__":
    main()