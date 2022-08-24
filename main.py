import pygame
import os
pygame.font.init()

WIDTH,HEIGHT = 800,400
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Shooter!")

IMAGE_WIDTH,IMAGE_HEIGHT = 40, 50
HEALTH_FONT = pygame.font.SysFont('comicsans', 30)
WINNER_FONT = pygame.font.SysFont('comicsans', 60)

# RED SHIP
RED_SHIP_IMG = pygame.image.load(os.path.join("Screenshots", "spaceship_red.png"))
RED_SHIP = pygame.transform.rotate(pygame.transform.scale(RED_SHIP_IMG, (IMAGE_WIDTH, IMAGE_HEIGHT)), 90)

# YELLOW SHIP
YELLOW_SHIP_IMG = pygame.image.load(os.path.join("Screenshots", "spaceship_yellow.png"))
YELLOW_SHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SHIP_IMG, (IMAGE_WIDTH, IMAGE_HEIGHT)), 270)

BG = pygame.transform.scale(pygame.image.load(os.path.join("Screenshots", "space.png")), (WIDTH,HEIGHT))

YELLOW_HIT = pygame.USEREVENT + 1 # EventId = 24 + 1
RED_HIT = pygame.USEREVENT + 2 # EventId = 24 + 2

# To sperate the game board 
BORDER = pygame.Rect(WIDTH/2 - 5, 0, 5, HEIGHT)

def draw_window(red,yellow, red_bullets ,yellow_bullets,red_health,yellow_health):
	WIN.blit(BG,(0,0))
	pygame.draw.rect(WIN,(0,0,0),BORDER)
	WIN.blit(RED_SHIP,(red.x,red.y))
	WIN.blit(YELLOW_SHIP,(yellow.x,yellow.y))

	red_health_text = HEALTH_FONT.render("HEALTH : " + str(red_health),1,(255,255,255))
	WIN.blit(red_health_text, (WIDTH - 150, 10))
	yellow_health_text = HEALTH_FONT.render("HEALTH : " + str(yellow_health), 1, (255,255,255))
	WIN.blit(yellow_health_text, (10,10))

	for bullet in yellow_bullets:
		pygame.draw.rect(WIN,(255,255,0),bullet)

	for bullet in red_bullets:
		pygame.draw.rect(WIN,(255,0,0),bullet)

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

def handle_bullet(yellow_bullets,red_bullets,yellow ,red,red_health,yellow_health):
	for bullet in yellow_bullets:
		bullet.x += BULLET_VEL
		if red.colliderect(bullet):
			pygame.event.post(pygame.event.Event(RED_HIT))
			yellow_bullets.remove(bullet)
		elif bullet.x > WIDTH:
			yellow_bullets.remove(bullet)

	for bullet in red_bullets:
		bullet.x -= BULLET_VEL
		if yellow.colliderect(bullet):
			pygame.event.post(pygame.event.Event(YELLOW_HIT))
			red_bullets.remove(bullet)
		elif bullet.x < 0:
			red_bullets.remove(bullet)


def draw_winner(text):
	winner_text = WINNER_FONT.render(text, 1, (255,255,255))
	WIN.blit(winner_text, (WIDTH/2 - winner_text.get_width()/2, HEIGHT/2 - winner_text.get_height()))
	pygame.display.update()
	pygame.time.delay(5000)

def main():
	red = pygame.Rect(650,170, IMAGE_WIDTH, IMAGE_HEIGHT)
	yellow = pygame.Rect(100,170, IMAGE_WIDTH, IMAGE_HEIGHT)
	run = True

	red_bullets = []
	yellow_bullets = []
	red_health = 10
	yellow_health = 10

	clock = pygame.time.Clock()

	while run:
		clock.tick(FPS)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False
				pygame.quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LCTRL:
					bullet = pygame.Rect(yellow.x + yellow.width, yellow.y  + yellow.height/2 -2, 30, 5)
					yellow_bullets.append(bullet)
							

				if event.key == pygame.K_RCTRL:
					bullet = pygame.Rect(red.x, red.y  + red.height/2 - 2, 30, 5)
					red_bullets.append(bullet)

			if event.type == RED_HIT:
				red_health -= 1
			if event.type == YELLOW_HIT:
				yellow_health -= 1

		winner_text = ""
		if red_health <= 0:
			winner_text = "YELLOW WIN!"
		elif yellow_health <= 0:
			winner_text = "RED WIN!"
		
		if winner_text != "":
			draw_winner(winner_text)
			break

		draw_window(red, yellow, red_bullets, yellow_bullets, red_health,yellow_health)	

		handle_bullet(yellow_bullets,red_bullets,yellow,red,red_health,yellow_health)
		
		keys_pressed = pygame.key.get_pressed()
		YELLOW_SHIP_CONTROLLER(keys_pressed, yellow)
		RED_SHIP_CONTROLLER(keys_pressed, red)

	main()

if __name__ == '__main__':
	main()
