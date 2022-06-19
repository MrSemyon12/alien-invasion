import pygame, time, math, sys, random
from asteroid import Asteroid
from particle import Particle
from button import Button
from player import Player
from fps import FPS
from constants import *


# Setup ----------------------------------------------------------- #
pygame.init()
pygame.display.set_caption('Asteroids 2: Alien Invasion!')
pygame.display.set_icon(pygame.image.load('data/asteroid_t1.png'))
# window_size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
window_size = (1200, 900)
flags = pygame.DOUBLEBUF
screen = pygame.display.set_mode(window_size, flags, 32)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
fps = FPS()

# Images ---------------------------------------------------------- #    
asteroid_image = [
    pygame.image.load('data/asteroid_t1.png').convert_alpha(),
    pygame.image.load('data/asteroid_t2.png').convert_alpha(),
    pygame.image.load('data/asteroid_t3.png').convert_alpha(),
]
player_image = [
    pygame.transform.scale(pygame.image.load('data/smog.png').convert_alpha(), (200, 200)),
    pygame.transform.scale(pygame.image.load('data/smog_running.png').convert_alpha(), (200, 200)),
]   
logo_image = pygame.transform.scale(pygame.image.load('data/logo.png').convert_alpha(), (1000, 300))
invasion_image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('data/logo2.png').convert_alpha(), (200, 200)), -15)
playbutton_image = [
    pygame.image.load('data/playbutton1.png').convert_alpha(), 
    pygame.image.load('data/playbutton2.png').convert_alpha()
]
button_image = [
    pygame.transform.scale(pygame.image.load('data/button_up.png').convert_alpha(), (600, 100)), 
    pygame.transform.scale(pygame.image.load('data/button_down.png').convert_alpha(), (600, 100)), 
]

# Sounds ---------------------------------------------------------- #
sounds = {
    'background' : pygame.mixer.Sound('data/sfx/background.wav'),
    'impulse' : pygame.mixer.Sound('data/sfx/laser.wav'),
    'bump' : pygame.mixer.Sound('data/sfx/bump.wav')
}
sounds['background'].set_volume(0.1)
sounds['impulse'].set_volume(0.01)
sounds['bump'].set_volume(0.05)
sounds['background'].play(-1)   

def playMenu():
    # Menu preset ----------------------------------------------------- #
    particles = []
    asteroids = []
    for _ in range(10):
        for _ in range(3):
            asteroids.append(Asteroid(1, window_size, asteroid_image, random.randint(100, window_size[0] - 100), random.randint(100, window_size[1] - 100)))
        for _ in range(4):
            asteroids.append(Asteroid(2, window_size, asteroid_image, random.randint(100, window_size[0] - 100), random.randint(100, window_size[1] - 100)))
        for _ in range(3):
            asteroids.append(Asteroid(3, window_size, asteroid_image, random.randint(100, window_size[0] - 100), random.randint(100, window_size[1] - 100)))
        
    last_time = time.time()
    cursor_on_btn = 0

    # Menu loop ------------------------------------------------------- #
    while True:
        current_time = time.time()
        dt = (current_time - last_time) * 60
        last_time = current_time
        
        mouseX, mouseY = pygame.mouse.get_pos() 
        clicked = 0    

    # Drawing ----------------------------------------------------- #
        screen.fill(BLACK)

        for ast in asteroids:
            ast.draw(screen)
            ast.dx = ast.mx * dt
            ast.dy = ast.my * dt
            ast.dangle = ast.mangle * dt        
            ast.update()

        for par in reversed(particles):
            par.draw(screen)
            par.update()
            if par.timer < 1:
                particles.remove(par)
        
        screen.blit(invasion_image, (200, 250 + math.cos(current_time * 5) * 10 - 25))
        screen.blit(logo_image, (window_size[0] // 2 - logo_image.get_width() // 2, window_size[1] // 2 - logo_image.get_height() // 2 + math.sin(current_time * 5) * 10 - 25))
        screen.blit(playbutton_image[cursor_on_btn], (window_size[0] // 2 - playbutton_image[cursor_on_btn].get_width() // 2, window_size[1] // 2 - playbutton_image[cursor_on_btn].get_height() // 2 + 110))
        
        fps.draw(screen)
        fps.clock.tick(60)
        
        pygame.display.update()

    # Buttons ----------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:            
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = 1
            if event.type == pygame.KEYDOWN and (event.key == pygame.K_RETURN or event.key == pygame.K_SPACE):
                clicked = 2

        if (mouseX - window_size[0] // 2) ** 2 + (mouseY - (window_size[1] // 2 + 110)) ** 2 < 75 ** 2:        
            if (cursor_on_btn == 0):
                for _ in range(100):
                    particles.append(Particle(window_size[0] // 2, window_size[1] // 2 + 110, (255, 255, 255)))
            cursor_on_btn = 1
        else:
            cursor_on_btn = 0
                
        if clicked == 1 and cursor_on_btn or clicked == 2:        
            sounds['impulse'].play()
            break 

def palyGame():
    # Game preset ----------------------------------------------------- #
    player = Player(window_size, player_image)
    button = Button(button_image)   
    particles = []
    asteroids = []
    last_time = time.time()
    difficult = 0
    tick = -1
    gameOver = False

    # Game loop ------------------------------------------------------- #
    while not gameOver:      
        current_time = time.time()
        dt = (current_time - last_time) * 60    
        last_time = current_time  
        tick += 1        

        if tick % DIFFICULT_PERIOD == 0:
            difficult += 1    
            
        if tick % ASTEROID_SPAWN_PERIOD == 0:  
            for _ in range(difficult):          
                asteroids.append(Asteroid(3, window_size, asteroid_image))
                asteroids.append(Asteroid(3, window_size, asteroid_image))
                asteroids.append(Asteroid(2, window_size, asteroid_image))
                asteroids.append(Asteroid(2, window_size, asteroid_image))
                asteroids.append(Asteroid(2, window_size, asteroid_image))
                asteroids.append(Asteroid(2, window_size, asteroid_image))                    
        
    # Drawing ----------------------------------------------------- #   
        screen.fill(BLACK)  
        button.draw(screen, player.isRunning)

        for par in reversed(particles):
            par.draw(screen)
            par.update()
            if par.timer < 1:
                particles.remove(par)             

        for ast in asteroids:
            ast.draw(screen)
            ast.dx = ast.mx * dt
            ast.dy = ast.my * dt
            ast.dangle = ast.mangle * dt        
            ast.update()        
                
        player.draw(screen)
        player.update()            
        
        fps.draw(screen)
        fps.clock.tick(60)

    # Buttons ----------------------------------------------------- #
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:              
                gameOver = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                player.isRunning = True
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE or event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                player.isRunning = False

        if player.isRunning:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_SPACE] or pygame.mouse.get_pressed():
                player.dangle += PLAYER_ROTATING_SPEED * dt
                player.dx += math.cos(math.radians(player.angle)) * dt
                player.dy -= math.sin(math.radians(player.angle)) * dt 

    # Collide check ----------------------------------------------- # 
        for ast in reversed(asteroids):        
            if player.collide(ast.mask, ast.x, ast.y) != None: 
                player.dangle *= -0.5   
                player.dx *= 0.5 
                player.dy *= 0.5     
                sounds['bump'].play()
                for _ in range(10):
                    particles.append(Particle(ast.x, ast.y, (255, 255, 255)))
                asteroids.remove(ast)                
                    
        pygame.display.update()

while True:
    playMenu()
    palyGame()
