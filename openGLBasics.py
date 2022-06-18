import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random
import numpy as np 
from queue import deque

red = (1, 0, 0)
green = (0, 1, 0)
blue = (0, 0, 1)
white = (1, 1, 1)
sky = (0, 1, 1)
yellow = (1, 1, 0)
black = (0, 0, 0)
gray = (0.5, 0.5, 0.5)
pink = (1, 0, 1)

upperBound = (255, 255, 255)

def snakeBoard(coordinates, block_size, color = [white], fill = True):
		coordinate0 =np.array([coordinates[0],coordinates[1], coordinates[2]])+block_size/2
		coordinate1 =np.array([coordinates[0],coordinates[1]-2*(block_size/2), coordinates[2]])+block_size/2
		coordinate2 =np.array([coordinates[0]-2*(block_size/2),coordinates[1]-2*(block_size/2), coordinates[2]])+block_size/2
		coordinate3 =np.array([coordinates[0]-2*(block_size/2),coordinates[1], coordinates[2]])+block_size/2
		coordinate4 =np.array([coordinates[0]-2*(block_size/2),coordinates[1], coordinates[2]-2*(block_size/2)])+block_size/2
		coordinate5 =np.array([coordinates[0],coordinates[1], coordinates[2]-2*(block_size/2)])+block_size/2
		coordinate6 =np.array([coordinates[0],coordinates[1]-2*(block_size/2), coordinates[2]-2*(block_size/2)])+block_size/2
		coordinate7 =np.array([coordinates[0],coordinates[1], coordinates[2]])-block_size/2
		
		vertices=(
				coordinate0.tolist(),
				coordinate1.tolist(),
				coordinate2.tolist(),
				coordinate3.tolist(),
				coordinate4.tolist(),
				coordinate5.tolist(),
				coordinate6.tolist(),
				coordinate7.tolist(),
			)
		



		edges = (#(0,1),
				# (1,2),
				# (2,3),
				# (3,0),
				# (5,6),
				# (6,7),
				# (7,4),
				# (4,5),
				# (0,5),
				# (1,6),
				# (2,7),
				# (3,4)
				)

		surfaces = (#(0, 1, 2, 3),
					#(4, 5, 6, 7),
					# (0, 1, 6, 5),
					(2, 1, 6, 7),
					# (7, 2, 3, 4),
					#(3, 4, 5, 0)
					)
		degree = 150
		tranform = np.array([[1, 0, 0], 
		[0, np.cos(degree), -np.sin(degree)],
		 [0, np.sin(degree), np.cos(degree)]])


		if not fill:
			glBegin(GL_LINES)
			glColor3fv(white)
			for edge in edges:
				for vertex in edge:
					glVertex3fv(vertices[vertex])

			glEnd()
		else:	
			i = 0
			colors = color
			glBegin(GL_QUADS)
			for surface in surfaces:
				for vertex in surface:
					vertex = vertices[vertex] 
					vertex = np.dot(vertex, tranform)
					glColor3fv(colors[i % len(colors)])
					i += 1
					glVertex3fv(vertex)
			glEnd()

def target_food(coordinates, block_size = 0.25):
	snakeBoard(coordinates, block_size, color = [red, pink])
def snake(snake_lsit, snake_length, block_size = 0.5):
	if len(snake_lsit) > snake_length:
		snake_lsit.popleft()
	for xyz in snake_lsit:
		snakeBoard(xyz, block_size, [sky, yellow])

def main():
	pygame.init()
	display_height = 800
	display_width = 800
	pygame.display.set_mode((display_width, display_height), DOUBLEBUF|OPENGL)
	clock = pygame.time.Clock()
	FPS = 4


	block_size = 0.5
	arena_size = 25 * block_size
 
	x_change, y_change, z_change = block_size, 0, 0
	x, y, z = 0, 0, 0
	score = 0
	x_enable = y_enable = z_enable = True

	snake_length = 1
	snake_lsit = deque([])

	food_x_coordinate = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
	food_y_coordinate = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
	food_z_coordinate = round((random.randrange( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
	target_food((food_x_coordinate, food_y_coordinate, food_z_coordinate), block_size)

	# OpenGL Params
	gluPerspective(45, (display_width / display_height), 0.1, 50.0)

	glTranslatef(0.0, 0.0, -2 * arena_size)

	game_over = False
	while not game_over:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				elif event.key == pygame.K_RIGHT and x_enable:
					x_change, y_change, z_change = block_size, 0, 0
					x_enable, y_enable, z_enable = False, True, True
				elif event.key == pygame.K_LEFT and x_enable:
					x_change, y_change, z_change = -block_size, 0, 0
					x_enable, y_enable, z_enable = False, True, True
				elif event.key == pygame.K_UP and y_enable:
					x_change, y_change, z_change = 0, 0, -block_size
					x_enable, y_enable, z_enable = True, False, True
				elif event.key == pygame.K_DOWN and y_enable:
					x_change, y_change, z_change = 0,  0, block_size
					x_enable, y_enable, z_enable = True, False, True
				elif event.key == pygame.K_w and z_enable:
					x_change, y_change, z_change = 0, 0, -block_size
					x_enable, y_enable, z_enable = True, True, False
				elif event.key == pygame.K_s and z_enable:
					x_change, y_change, z_change = 0, 0, block_size
					x_enable, y_enable, z_enable = True, True, False
				elif event.key == pygame.K_p:
					snake_length += 1
					score += 1

		x += x_change
		y += y_change
		z += z_change
		snake_lsit.append((x, y, z))

		# Hit Boundaries
		# if abs(x) >= abs((arena_size - block_size) / 2) or abs(y) >= abs((arena_size - block_size) / 2) or abs(z) >= abs((arena_size - block_size) / 2):
		# 	game_over = True    


		if (abs(x-food_x_coordinate)<=0.09 and abs(z-food_z_coordinate)<=0.09):
			food_x_coordinate = round((np.random.randint( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
			food_y_coordinate = round((np.random.randint( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
			food_z_coordinate = round((np.random.randint( - (arena_size - block_size) / 2, (arena_size - block_size) / 2)) / block_size) * block_size
			snake_length += 1
			score += 1

		for i in range(0, len(snake_lsit)):
			for j in range(i + 1, len(snake_lsit)):
				if snake_lsit[i][0] == snake_lsit[j][0] and snake_lsit[i][1] == snake_lsit[j][1] and snake_lsit[i][2] == snake_lsit[j][2]:
					game_over = True 

		# Rendering
		glRotatef(0, 0, 0, 1)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		snakeBoard((0, 0, 0), arena_size, color = [green, red, yellow])
		snakeBoard((0, 0, 0), arena_size, fill = False)

		target_food((food_x_coordinate, 0, food_z_coordinate), block_size)
		snake(snake_lsit, snake_length)
		pygame.display.flip()
		clock.tick(FPS)

if __name__ == "__main__":
	main()
