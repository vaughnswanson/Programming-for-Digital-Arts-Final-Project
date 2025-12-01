import pygame
import random
import math


#TODO restart when player hits enter on loose screen
#TODO Implement score system based on number of freaks killed
#TODO Implement levels with increasing freak spawn rates and speeds
# luxuary TODOs:
#TODO Implement turret upgrade system
#TODO add live score of freaks killed on screen
#TODO add live timer on screen

def EnemyHealthSpeedGenerator():
    #give enemy random skill points from 1 to 5
    EnemyTotalPoints = random.randint(1, 12)
    
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


def pick_audio(filename, filenum_range):

    num = random.randrange(1, filenum_range + 1)
    
    file_path = f"assets/audio/{filename}{num}"
    
    return file_path

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
    def __init__ (self, pos=(0,0), fire_rate=5,):
        self.pos = pos
        self.fire_rate = fire_rate  # bullets per second
        self.shot_timer = 0 # time since last shot
        self.cooldown = .5 / fire_rate # seconds between shots
      
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
    
    
    def update(self, dt):
        #update turret to face mouse
        self.shot_timer += dt
        #get mouse position    
        mouse_x, mouse_y = pygame.mouse.get_pos()
        turret_x, turret_y = self.pos
        angle = math.atan2(mouse_y - turret_y, mouse_x - turret_x)
        self.rotation = math.degrees(angle)

def main():
    #initalise pygame
    pygame.init()

    game_state = 1  # 1 = playing, 0 = game over

    pygame.display.set_caption("Hoard of Freaks")

    def reset_game():
        nonlocal freaks, bullets, freak_spawn_timer, game_state
        freaks = []
        bullets = []
        freak_spawn_timer = 0
        game_state = 1
        clock.tick()  # Reset clock to avoid large dt on restart

  
    
    clock = pygame.time.Clock()
    running = True
    resolution = (1920,1080)
    screen = pygame.display.set_mode((resolution))
    
    #spawn freak at random y position on right side of screen
    freak_spawn_rate = 2  # freaks per second
    freak_spawn_timer = 0
    freaks = []
    
    #background = pygame.image.load("assets/images/HoardOfFreaks_Background.png").convert()
    
    #make the background black
    background = pygame.Surface(resolution)
    background.fill((0, 0, 0))
    background = pygame.transform.scale(background, resolution)
    
    #create turret
    turret = Turret()
    turret.position(resolution) 
    bullets = []

    #health stats
    health = 1


    while running :
        if game_state == 1:
                #set delta time
                dt = clock.tick(60) / 1000 

                #set background
                background = pygame.image.load("assets/images/HoardOfFreaks_Background.png").convert()
                #event loop
                for event in pygame.event.get():
                    #use quit to close program
                    if event.type == pygame.QUIT:
                        running = False 
                
                #check if mouse button is pressed
                mouse_buttons = pygame.mouse.get_pressed()
                
                #check if left mouse button is pressed
                if mouse_buttons[0]: 
                    if turret.can_fire():
                        #fire bullet
                        mouse_x, mouse_y = pygame.mouse.get_pos()
                        turret_x, turret_y = turret.pos
                        angle = math.atan2(mouse_y - turret_y, mouse_x - turret_x)
                        direction = pygame.math.Vector2(math.cos(angle), math.sin(angle))
                        bullet = Bullet(pos=turret.pos, direction=direction, speed=2000)
                        bullets.append(bullet)
                        active_audio_fire = pick_audio("fire", 3)
                        pygame.mixer.Sound(active_audio_fire).play()
                    
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
                            if freak.health > 0:
                                active_audio_hurt = pick_audio("hurt", 3)
                                pygame.mixer.Sound(active_audio_hurt).play()
                            else:
                                active_audio_death = pick_audio("die", 3)
                                pygame.mixer.Sound(active_audio_death).play()

                #delete dead bullets
                bullets = [bullet for bullet in bullets if bullet.alive]

                #update turret
                turret.update(dt)
                turret.draw(screen)
                


                #update freaks
                for freak in freaks:
                    freak.update(dt)
                    
                    if freak.pos[0] <= 0:
                        health -= 1
                        pygame.mixer.Sound("assets/audio/lose").play()
                        freak.alive = False

                        if health <= 0:
                            game_state = 0
                        
                        

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

        elif game_state == 0:
            
            clock.tick(60)
            background = pygame.image.load("assets/images/HoardOfFreaks_Gameover.png").convert()
            screen.blit(background, (0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if game_state == 0 and event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_state = 1
                        reset_game()
                        health = 1
                pygame.display.flip()

if __name__ == "__main__":
    main()