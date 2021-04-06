import pygame
import random
import math
from pygame import mixer

# rewrite the comments
# try to make it object oriented

# Initialization
pygame.init()  # SHOULD BE THERE
screen = pygame.display.set_mode((800, 600))  # w , h # SHOULD BE THERE
pygame.display.set_caption("Space Invadors")
icon = pygame.image.load('space-invaders (1).png')
pygame.display.set_icon(icon)
background = pygame.image.load('2362730.jpg')

# player
player_icon = pygame.image.load('my_space.png')
player_x = 400
player_y = 450
changes_x = 0
changes_y = 0

enemy_icon = []
enemy_x = []
enemy_y = []
changes_enemy_x = []
changes_enemy_y = []
number_of_enemy = 5
enemy_icon.append(pygame.image.load('1.png'))
enemy_icon.append(pygame.image.load('2.png'))
enemy_icon.append(pygame.image.load('3.png'))
enemy_icon.append(pygame.image.load('4.png'))
enemy_icon.append(pygame.image.load('5.png'))

for i in range(number_of_enemy):
	enemy_x.append(random.randint(0, 700))
	enemy_y.append(random.randint(50, 200))
	changes_enemy_x.append(0.3)
	changes_enemy_y.append(0)
"""
# enemy
enemy_icon = pygame.image.load('egg.png')
enemy_x = random.randint(0, 700)
enemy_y = random.randint(50, 200)
changes_enemy_x = 0.3
changes_enemy_y = 0
"""
# bullet
bullet_icon = pygame.image.load('juice.png')
bullet_x = player_x
bullet_y = player_y
changes_bullet_x = 0.3
changes_bullet_y = 0.3
bullet_state = 'ready'


def player(x, y):
	screen.blit(player_icon, (x, y))


def enemy(x, y, i):
	screen.blit(enemy_icon[i], (x, y))


def fire_bullet(x, y):
	global bullet_state
	bullet_state = 'fire'
	screen.blit(bullet_icon, (x + 16, y - 5))


def isCollision_bullet(enemy_x, enemy_y, bullet_x, bullet_y):
	d = math.sqrt((enemy_x - bullet_x) ** 2 + (enemy_y - bullet_y) ** 2)
	print(f'Distance: {d}')
	return d < 28

def isCollision_player(enemy_x, enemy_y, player_x, player_y):
	d = math.sqrt((enemy_x - player_x) ** 2 + (enemy_y - player_y) ** 2)
	return d < 28
score = 0
score_collision = -1
font = pygame.font.Font('freesansbold.ttf', 32)


def show_score():
	s = font.render("SCORE: " + str(score), True, (255, 255, 255))
	screen.blit(s, (10, 10))

font_2 = pygame.font.Font('freesansbold.ttf', 70)

def game_over_text():
	over = font_2.render(
	"GAME OVER", True, (255, 255, 255))
	screen.blit(over, (200, 250))


# The main Game loop
running = True
while running:  # SHOULD BE THERE
	pygame.display.update()  # SHOULD BE THERE # It's used for to update any changes
	screen.fill((0, 0, 0))
	screen.blit(background, (0, 0))
	for event in pygame.event.get():  # SHOULD BE THERE
		if event.type == pygame.QUIT:  # QUIT = 256 it's just a constant
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				changes_x = -0.4
			if event.key == pygame.K_RIGHT:
				changes_x = 0.4
			# for fire
			if event.key == pygame.K_SPACE and bullet_state == 'ready':
				bullet_x = player_x
				bullet_y = player_y
				laser = mixer.Sound('laser.wav')
				laser.play()
				fire_bullet(bullet_x, bullet_y)
			if event.key == pygame.K_UP:
				changes_y = -0.4
			if event.key == pygame.K_DOWN:
				changes_y = 0.4
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				changes_x = 0
			if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
				changes_y = 0

	player(player_x, player_y)
	player_x += changes_x
	if (player_x <= 0):
		player_x = 0
	if (player_x >= 736):
		player_x = 736

	player_y += changes_y
	if (player_y <= 0):
		player_y = 0
	if (player_y >= 540):
		player_y = 540

	for i in range(number_of_enemy):
		enemy(enemy_x[i], enemy_y[i], i)
		enemy_x[i] += changes_enemy_x[i]
		if (enemy_x[i] <= 0):
			changes_enemy_x[i] = 0.6
			enemy_y[i] += 40
		if (enemy_x[i] >= 740):
			changes_enemy_x[i] = -0.6
			enemy_y[i] += 40
		if (enemy_y[i] >= 600):
			exp = mixer.Sound('laser.wav')
			exp.play()
			for m in range(number_of_enemy):
				enemy_y[m] = 2000
			game_over_text()
		# collision
		collision = isCollision_bullet(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
		c = isCollision_player(enemy_x[i], enemy_y[i], player_x, player_y)
		if collision and not c:
			score += 1
			print("bullet")
			print(bullet_x)
			print(bullet_y)
			print("player")
			print(player_x)
			print(player_y)
			print("enemy")
			print(enemy_x)
			print(enemy_y)
			print(f'spaceship {i}')
			print(enemy_x[i]-bullet_x)
			print(enemy_y[i]-bullet_y)
			exp = mixer.Sound('explosion.wav')
			exp.play()
			enemy_x[i] = random.randint(0, 700)
			enemy_y[i] = random.randint(50, 300)
			bullet_y = player_y
			bullet_x = player_x
			bullet_state = 'ready'
		collision_player = isCollision_player(enemy_x[i], enemy_y[i], player_x, player_y)
		if collision_player:
			exp = mixer.Sound('laser.wav')
			exp.play()
			for m in range(number_of_enemy):
				enemy_y[m] = 2000
			game_over_text()
			bullet_x = player_x
			bullet_y = player_y
			bullet_state = 'ready'
	if bullet_state == 'fire':
		fire_bullet(bullet_x, bullet_y)
		bullet_y -= 0.9
	if (bullet_y <= 0):
		bullet_y = player_y
		bullet_x = player_x
		bullet_state = 'ready'
		score = 0
	if bullet_state == 'ready':
		bullet_x = player_x
		bullet_y = player_y
	show_score()
