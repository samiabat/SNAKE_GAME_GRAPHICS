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

def snakeBoard(coordinates, block_size, color = [white], filled = True):
		coordinate0 =np.array([
      					coordinates[0],
                        coordinates[1], 
                        coordinates[2]
                        ])+block_size/2
		coordinate1 =np.array([
      					coordinates[0],
           				coordinates[1]-2*(block_size/2), 
               			coordinates[2]
                  		])+block_size/2
		coordinate2 =np.array([
      					coordinates[0]-2*(block_size/2),
           				coordinates[1]-2*(block_size/2), 
               			coordinates[2]
                  		])+block_size/2
		coordinate3 =np.array([
      					coordinates[0]-2*(block_size/2),
           				coordinates[1], 
               			coordinates[2]
                  		])+block_size/2
		coordinate4 =np.array([
      					coordinates[0]-2*(block_size/2),
           				coordinates[1], 
               			coordinates[2]-2*(block_size/2)
                  		])+block_size/2
		coordinate5 =np.array([
      					coordinates[0],
           				coordinates[1], 
           				coordinates[2]-2*(block_size/2)
               			])+block_size/2
		coordinate6 =np.array([
      					coordinates[0],
           				coordinates[1]-2*(block_size/2), 
               			coordinates[2]-2*(block_size/2)
                  		])+block_size/2
		coordinate7 =np.array([
      					coordinates[0],
           				coordinates[1], 
               			coordinates[2]
                  		])-block_size/2
		
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
		



		surfaces = (
					(2, 1, 6, 7),
					)
  
		transform_matrix=np.array([
       								[1,		0,		0		],
                              		[0,np.cos(150),-np.sin(150)],
                                	[0,np.sin(150),np.cos(150)]
                                ])

		index = 0
		colors = color
		glBegin(GL_QUADS)
		
		for surface in surfaces:
			for vertex in surface:
				glColor3fv(colors[index % len(colors)])
				index += 1
				vertex=vertices[vertex]
				vertex=np.dot(vertex,transform_matrix)
				glVertex3fv(vertex)
		glEnd()
   

def target_food(coordinates, block_size = 0.25):
    snakeBoard(coordinates, block_size, color = [red, pink])
    
def snake(snake_lsit, snake_length, block_size = 0.49):
	if len(snake_lsit) > snake_length:
		snake_lsit.popleft()
	for xyz in snake_lsit:
		snakeBoard(xyz, block_size, [sky, yellow])

def main():
	pygame.init()
	display_height = 800
	display_width = 800
	pygame.display.set_mode((display_width, display_height), DOUBLEBUF|OPENGL)
	glClearColor(0.7,0.8,0.89,0.98)
	clock = pygame.time.Clock()
	FPS = 5


	block_size = 0.5
	arena_size = 25 * block_size
 
	x_change,z_change = block_size,  0
	x_coord, y_coord, z_coord = 0, 0, 0
	score = 0
	x_enable =  z_enable = True

	snake_length = 1
	snake_lsit = deque([])

	food_x_coordinate = round((random.randrange(-44,44)))*0.1 
	food_z_coordinate = round((random.randrange(-5,190)))*0.04 
	target_food((food_x_coordinate, 0,food_z_coordinate), block_size)
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
					x_change,  z_change = block_size,  0
					x_enable, z_enable = False, True
				elif event.key == pygame.K_LEFT and x_enable:
					x_change,  z_change = -block_size,  0
					x_enable, z_enable = False, True
				elif event.key == pygame.K_UP and z_enable:
					x_change,  z_change = 0,  -block_size
					x_enable, z_enable = True, True
				elif event.key == pygame.K_DOWN and z_enable:
					x_change,  z_change = 0, block_size
					x_enable, z_enable = True, True
				
		x_coord += x_change
		y_coord += 0
		z_coord += z_change
		snake_lsit.append((x_coord, y_coord, z_coord))

		# Hit Boundaries
		if abs(x_coord) >= 4.5 or z_coord<=-0.4 or z_coord>=8:
			game_over = True
		if (abs(x_coord-food_x_coordinate)<=0.5) and abs(z_coord-food_z_coordinate)<=0.5:
			print("Hitted the target")
			food_x_coordinate = round((np.random.randint(-44,44)))*0.1
			food_z_coordinate = round((np.random.randint(-5,190)))*0.04
			snake_length += 1
			score += 1

		for i in range(0, len(snake_lsit)):
			for j in range(i + 1, len(snake_lsit)):
				if snake_lsit[i][0] == snake_lsit[j][0] and snake_lsit[i][1] == snake_lsit[j][1] and snake_lsit[i][2] == snake_lsit[j][2]:
					game_over = True 

		glRotatef(0, 0, 0, 0)
		glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
		snakeBoard((0, 0, 0), arena_size, color = [green, red, yellow])
		snakeBoard((0, 0, 0), arena_size, filled = False)

		target_food((food_x_coordinate, 0,food_z_coordinate), block_size)
		snake(snake_lsit, snake_length)
		pygame.display.flip()
		clock.tick(FPS)

if __name__ == "__main__":
	main()
