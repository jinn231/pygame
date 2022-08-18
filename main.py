import pygame
import os

WIDTH,HEIGHT = 800,400
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shooter!")

IMAGE_WIDTH,IMAGE_HEIGHT = 40, 50

# RED SHIP
RED_SHIP_IMG = pygame.image.load(os.path.join("Screenshots", "spaceship_red.png"))
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMG, (IMAGE_WIDTH, IMAGE_HEIGHT)), 90)

# YELLOW SHIP
YELLOW_SHIP_IMG = pygame.image.load(os.path.join("Screenshots", "spaceship_yellow.png"))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_IMG, (IMAGE_WIDTH, IMAGE_HEIGHT)), 270)

BG = pygame.image.load(os.path.join("Screenshots", "space.png"))

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# To sperate the game board 
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 5, HEIGHT)

def draw_window(red,yellow):
	WIN.fill((255,255,255))
	pygame.draw.rect(WIN,(0,0,0),BORDER)
	WIN.blit(RED_SHIP,(red.x,red.y))
	WIN.blit(YELLOW_SHIP,(yellow.x,yellow.y))
	pygame.display.update()

FPS = 80
VEL = 5
BULLET_VEL = 7
MAX_BULLET = 3

def YELLOW_SHIP_CONTROLLER(key,ship):
		if key[pygame.K_a] and ship.x - VEL > 0:
			ship.x -= VEL
		elif key[pygame.K_d] and ship.x + VEL + ship.width + 20 < BORDER.x:
			ship.x += VEL
		elif key[pygame.K_w] and ship.y - VEL > 0:
			ship.y -= VEL
		elif key[pygame.K_s] and ship.y + VEL + ship.height < HEIGHT :
			ship.y += VEL

def RED_SHIP_CONTROLLER(key, ship):
		if key[pygame.K_LEFT] and ship.x - VEL - 10 > BORDER.x + BORDER.width:
			ship.x -= VEL
		elif key[pygame.K_RIGHT] and ship.x + VEL + ship.width + 10 < WIDTH:
			ship.x += VEL
		elif key[pygame.K_UP] and ship.y - VEL > 0:
			ship.y -= VEL
		elif key[pygame.K_DOWN] and ship.y + VEL + ship.height < HEIGHT :
			ship.y += VEL

def handl_bullet(yellow_bullet,red_bullet,yellow , red):
	for bullet in yellow_bullet:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))	
			yellow_bullet.remove(bullet)		

        for bullet in red_bullet:
                bullet.x += BULLET_VEL
                if yellow.colliderect(bullet):
                        pygame.event.post(pygame.event.Event(YELLOW_HIT))  
                        red_bullet.remove(bullet)

def main():
	red = pygame.Rect(650,170, IMAGE_WIDTH, IMAGE_HEIGHT)
	yellow = pygame.Rect(100,170, IMAGE_WIDTH, IMAGE_HEIGHT)
	run = True

	red_bullets = []
	yellow_bullets = []

	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
	    		
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLET:
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y  + yellow.height/2 -2, 10, 5)
					yellow_bullets.append(bullet)
							

				if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLET:
                                        bullet = pygame.Rect(red.x, red.y  + red.height/2 -2, 10, 5)
                                        red_bullets.append(bullet)

		draw_window(red, yellow)	

		handle_bullet(yellow_bullet,red_bullet,yellow,red)
		
		keys_pressed = pygame.key.get_pressed()
		YELLOW_SHIP_CONTROLLER(keys_pressed, yellow)
		RED_SHIP_CONTROLLER(keys_pressed, red)

	pygame.quit()

main()
