import pygame
import random
import math


# luxuary TODOs:
#TODO Implement turret upgrade system
#TODO add live score of freaks killed on screen
#TODO add live timer on screen

def EnemyHealthSpeedGenerator(seconds_survived, difficulty_multiplyer):
    
    max_points = 1 + int(seconds_survived // 25)* difficulty_multiplyer  # Increase max points every 00 seconds
    min_points = (max_points // 2) +1
   
    #give enemy random skill points 
    EnemyTotalPoints = random.randint(min_points, max_points)
    
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

    def __init__(self, pos=(0,0), seconds_survived=0, difficulty_multiplier=1):
        self.pos = pos
        self.health, self.speed = EnemyHealthSpeedGenerator(seconds_survived, difficulty_multiplier)
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
        self.pos = pygame.math.Vector2(pos)
        self.direction = pygame.math.Vector2(direction).normalize() #point the bullet in the correct direction
        self.speed = speed
        self.alive = True
       
        #load sprite and preserve it for rotation
        self.sprite_base = pygame.image.load(f"assets/images/bullet.png").convert_alpha()
        
        #scale sprite
        self.sprite_base = pygame.transform.scale(self.sprite_base, (32,32))
        
        #create sprite for rotation
        self.sprite = self.sprite_base
        
        #calculate rotation angle
        self.rotation = math.degrees(math.atan2(self.direction.y, self.direction.x))

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
        
        self.sprite = pygame.transform.rotate(self.sprite_base, - self.rotation)
        screen.blit(self.sprite, self.rect.topleft) 

class Turret():
    def __init__ (self, pos=(0,0), fire_rate=1):
        self.pos = pos
        self.fire_rate = fire_rate

        #fire rate control
        self.shot_timer = 0
        self.cooldown = .5 / fire_rate  # 1/fire_rate seconds between shots

        #load sprite
        self.sprite = pygame.image.load(f"assets/images/turret.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (96,96))
        self.sprite2 = pygame.image.load(f"assets/images/turret_housing.png").convert_alpha()
        self.sprite2 = pygame.transform.scale(self.sprite2, (96,96))

    
    def position(self, resolution):
        self.pos = (50 , resolution[1]//2)
        self.rect = self.sprite.get_rect(center=self.pos)

    def set_fire_rate(self, fire_rate):
        self.fire_rate = fire_rate
        self.cooldown = .5 / fire_rate
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

    #reset stats on new game function
    def reset_game():
        nonlocal health, freaks, bullets,bullet_damage, freak_spawn_timer, game_state, seconds_survived, freak_spawn_rate, freaks_killed, turret, played_lose_sound, difficulty_multiplier, damage_tier, spawn_tier, fire_rate_tier, difficulty_tier

        freaks = []
        bullets = []
        bullet_damage = 1
        seconds_survived = 0
        game_state = 1
        clock.tick()  # avoid huge dt
        freak_spawn_rate = 0.5
        freaks_killed = 0
        freak_spawn_timer = 0
        played_lose_sound = False
        difficulty_multiplier = 1
        damage_tier = 0
        spawn_tier = 0
        fire_rate_tier = 0
        difficulty_tier = 0
         
        health = 1

        turret.position(resolution)  
        turret.set_fire_rate(1)     

    damage_tier = 0
    spawn_tier = 0
    fire_rate_tier = 0
    difficulty_tier = 0

    played_lose_sound = False
    freak_spawn_timer = 0

    #keep track of freaks killed
    freaks_killed = 0

    #keep track of seconds survived
    seconds_survived = 0

    
    clock = pygame.time.Clock()
    running = True
    resolution = (1920,1080)
    screen = pygame.display.set_mode((resolution))
    
        
    #freak spawn timer
    freak_spawn_timer = 0
    freak_spawn_rate = 0.5  # freaks per second
    freaks = []
    
    difficulty_multiplier = 1
   
    #make the background
    background = pygame.Surface(resolution)
    background.fill((0, 0, 0))
    background = pygame.transform.scale(background, resolution)
    
    #create turret
    turret = Turret()
    turret.position(resolution) 
    bullets = []
    bullet_damage = 1
    fire_rate = 1

    #health stats
    health = 1

    #background image
    background = pygame.image.load("assets/images/HoardOfFreaks_Background.png").convert()

    #main game loop
    while running :
        if game_state == 1:
                #set delta time
                dt = clock.tick(60) / 1000 
                seconds_survived += dt
                
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
                        bullet = Bullet(pos=turret.pos, direction=direction, speed=1000)
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
                        #if bullet collides with freak deal damage
                        if bullet.rect.colliderect(freak.rect):
                            freak.health -= bullet_damage
                            bullet.alive = False 
                            
                            #play hurt sound
                            if freak.health > 0:
                                active_audio_hurt = pick_audio("hurt", 3)
                                pygame.mixer.Sound(active_audio_hurt).play()
                            
                            #play death sound and on death events
                            else:
                                active_audio_death = pick_audio("die", 3)
                                pygame.mixer.Sound(active_audio_death).play()
                                
                                #track freaks killed
                                freaks_killed += 1
                                
                                # cap fire rate increase
                                if fire_rate < 5:
                                    #increase fire rate every 10 freaks killed
                                    if freaks_killed // 20 > fire_rate_tier:
                                        fire_rate_tier += 1
                                        active_audio_levelup = pick_audio("levelup", 2)
                                        pygame.mixer.Sound(active_audio_levelup).play()
                                        fire_rate += .2
                                        turret.set_fire_rate(fire_rate)
                                        
                                
                                #increase bullet damage every 75 freaks killed
                                if freaks_killed // 75 > damage_tier:
                                    damage_tier += 1
                                    active_audio_levelup = pick_audio("levelup", 2)
                                    pygame.mixer.Sound(active_audio_levelup).play()
                                    bullet_damage += .2
                                
                                #increase difficulty every 500 freaks killed
                                if freaks_killed // 500 > difficulty_tier:
                                    difficulty_tier += 1
                                    difficulty_multiplier += .5
                font = pygame.font.SysFont("Arial", 40)
                #draw end bullet damage
                bullet_damage_text = font.render(f"Final Bullet Damage: {bullet_damage}", True, (255, 255, 255))
                bullet_damage_rect = bullet_damage_text.get_rect(center=(resolution[0] // 2, 150))  # 50 pixels below
                screen.blit(bullet_damage_text, bullet_damage_rect)

                # draw final fire rate
                fire_rate_text = font.render(f"Final Fire Rate: {round(fire_rate,2)}", True, (255, 255, 255))
                fire_rate_rect = fire_rate_text.get_rect(center=(resolution[0] // 2, 100))  # 50 pixels below
                screen.blit(fire_rate_text, fire_rate_rect)

                #draw freaks spawn rate
                spawn_rate_text = font.render(f"Final Freak Spawn Rate: {round(freak_spawn_rate,2)}", True, (255, 255, 255))
                spawn_rate_rect = spawn_rate_text.get_rect(center=(resolution[0] // 2, 50))  # 50 pixels below
                screen.blit(spawn_rate_text, spawn_rate_rect)
                # draw max points
                max_points = 1 + int(seconds_survived // 30)* difficulty_multiplier
                max_points_text = font.render(f"Max Freak Points: {max_points}", True, (255, 255, 255))
                max_points_rect = max_points_text.get_rect(center=(resolution[0] // 2, 200))  # 50 pixels below
                screen.blit(max_points_text, max_points_rect)                 

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
                        freak.alive = False

                        if health <= 0:
                            game_state = 0
                        
                #spawn freaks
                freak_spawn_timer += dt
                
                #cap spawn rate
                if freak_spawn_rate < 10:
                   # increase freak spawn rate once by .1 every 15 seconds survived
                     if seconds_survived // 15 > spawn_tier:
                        spawn_tier += 1
                        freak_spawn_rate += .2
                 
               
                while freak_spawn_timer >= 1 / freak_spawn_rate:
                    freak_spawn_timer -= 1 / freak_spawn_rate       

                    #spawn freak at random y position on right side of screen
                    y = random.choice(range(0, resolution[1]-96,96))                
                    freaks.append(Freak(pos=(resolution[0], y), seconds_survived=seconds_survived))
                
                #delete dead freaks
                freaks = [freak for freak in freaks if freak.alive]

                #draw freaks
                for freak in freaks:
                    freak.draw(screen)

                pygame.display.flip()
        
        # Game Over Screen
        elif game_state == 0:
            if not played_lose_sound:
                pygame.mixer.Sound("assets/audio/lose").play()
                played_lose_sound = True

            clock.tick(60)
            background_gameover = pygame.image.load("assets/images/HoardOfFreaks_Gameover.png").convert()
            screen.blit(background_gameover, (0,0))
            
            # Draw freaks killed counter
            font = pygame.font.SysFont("Arial", 40)
            freaks_killed_text = font.render(f"Freaks Killed: {freaks_killed}", True, (255, 255, 255))
            text_rect = freaks_killed_text.get_rect(center=(resolution[0] // 2, 800))  
            screen.blit(freaks_killed_text, text_rect)
            
            # Draw timer below freaks killed
            seconds_text = font.render(f"Time Survived: {int(seconds_survived)}s", True, (255, 255, 255))
            seconds_rect = seconds_text.get_rect(center=(resolution[0] // 2, 850))  # 50 pixels below
            screen.blit(seconds_text, seconds_rect)

            #draw end bullet damage
            bullet_damage_text = font.render(f"Final Bullet Damage: {bullet_damage}", True, (255, 255, 255))
            bullet_damage_rect = bullet_damage_text.get_rect(center=(resolution[0] // 2, 150))  # 50 pixels below
            screen.blit(bullet_damage_text, bullet_damage_rect)

            # draw final fire rate
            fire_rate_text = font.render(f"Final Fire Rate: {round(fire_rate,2)}", True, (255, 255, 255))
            fire_rate_rect = fire_rate_text.get_rect(center=(resolution[0] // 2, 100))  # 50 pixels below
            screen.blit(fire_rate_text, fire_rate_rect)

            #draw freaks spawn rate
            spawn_rate_text = font.render(f"Final Freak Spawn Rate: {round(freak_spawn_rate,2)}", True, (255, 255, 255))
            spawn_rate_rect = spawn_rate_text.get_rect(center=(resolution[0] // 2, 50))  # 50 pixels below
            screen.blit(spawn_rate_text, spawn_rate_rect)
            # draw max points
            max_points = 1 + int(seconds_survived // 30)* difficulty_multiplier
            max_points_text = font.render(f"Max Freak Points: {max_points}", True, (255, 255, 255))
            max_points_rect = max_points_text.get_rect(center=(resolution[0] // 2, 200))  # 50 pixels below
            screen.blit(max_points_text, max_points_rect)

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