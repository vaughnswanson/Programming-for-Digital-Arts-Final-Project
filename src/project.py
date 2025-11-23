import pygame
import random
import math

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
        #load sprite
        self.sprite = pygame.image.load(f"assets/images/bullet.png").convert_alpha()
        #scale sprite
        self.sprite = pygame.transform.scale(self.sprite, (32,32))
        #give sprite hitbox 
        self.rect = self.sprite.get_rect(topleft=pos)
       
       
    def update(self, dt, resolution):
        # Update bullet position based on direction and speed
        self.pos += (self.direction * self.speed * dt)
        self.rect.center = self.pos
        
        # Check if bullet is out of bounds and mark it as not alive
        if (self.pos[0] < 0 or self.pos[0] > resolution[0]or
            self.pos[1] < 0 or self.pos[1] > resolution[1]):
            self.alive = False
    
    def draw(self, screen):
        
        screen.blit(self.sprite, self.rect.topleft) 

class Turret():
    def __init__ (self, pos=(0,0), fire_rate=2,):
        self.pos = pos
        self.fire_rate = fire_rate  # bullets per second
        self.shot_timer = 0 # time since last shot
        self.cooldown = 1 / fire_rate # seconds between shots
      
        self.last_shot_time = 0
        #load sprite
        self.sprite = pygame.image.load(f"assets/images/turret.png").convert_alpha()
        #scale sprite
        self.sprite = pygame.transform.scale(self.sprite, (96,96))
        self.sprite2 = pygame.image.load(f"assets/images/turret_housing.png").convert_alpha()
        self.sprite2 = pygame.transform.scale(self.sprite2, (96,96))

    
    def position(self, resolution):
        self.pos = (50 , resolution[1]//2)
        self.rect = self.sprite.get_rect(center=self.pos)

    def can_fire(self):
        if self.shot_timer >= self.cooldown:
            self.shot_timer = 0
            return True
        return False


    def draw(self, screen):
        #draw the turret rotated to face the mouse
        rotated_sprite = pygame.transform.rotate(self.sprite, -self.rotation)
        screen.blit(rotated_sprite, rotated_sprite.get_rect(center=self.pos))
        #draw the turret housing
        screen.blit(self.sprite2, self.sprite2.get_rect(center=self.pos))
    
    #update turret to face mouse
    def update(self, dt):
        self.shot_timer += dt
         #get mouse position    
        mouse_x, mouse_y = pygame.mouse.get_pos()
        turret_x, turret_y = self.pos
        angle = math.atan2(mouse_y - turret_y, mouse_x - turret_x)
        self.rotation = math.degrees(angle)


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
    bullets = []
    #background = pygame.image.load("assets/images/HoardOfFreaks_Background.png").convert()
    #make the background black
    background = pygame.Surface(resolution)
    background.fill((0, 0, 0))
    background = pygame.transform.scale(background, resolution)
    #create turret
    turret = Turret()
    turret.position(resolution) 

    while running :
        #set delta time
        dt = clock.tick(60) / 1000 
        #event loop
        for event in pygame.event.get():
            #use quit to close program
            if event.type == pygame.QUIT:
                running = False 
            #check if mouse button is pressed
            if event.type == pygame.MOUSEBUTTONDOWN:
                if turret.can_fire():
                    #fire bullet
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    turret_x, turret_y = turret.pos
                    angle = math.atan2(mouse_y - turret_y, mouse_x - turret_x)
                    direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))
                    bullet = Bullet(pos=turret.pos, direction=direction, speed=500)
                    bullets.append(bullet)
            
        screen.blit(background, (0,0))

       
        #update bullets
        for bullet in bullets:
            bullet.update(dt, resolution)
            bullet.draw(screen)
            
            #check for collision with freaks
            for freak in freaks:
                if bullet.rect.colliderect(freak.rect):
                    freak.health -= 1
                    bullet.alive = False
        #delete dead bullets
        bullets = [bullet for bullet in bullets if bullet.alive]

        #update turret
        turret.update(dt)
        turret.draw(screen)
        


        #update freaks
        for freak in freaks:
            freak.update(dt)

        #spawn freaks
        freak_spawn_timer += dt
        while freak_spawn_timer >= 1 / freak_spawn_rate:
            freak_spawn_timer -= 1 / freak_spawn_rate       
            
            #spawn freak at random y position on right side of screen
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