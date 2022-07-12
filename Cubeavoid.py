import pygame
import random
import turtle as t
from time import sleep

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 800

BLACK = (0,0,0)
WHITE = (255,255,255)
GRAY = (150,150,150)
RED = (255,0,0)

class Cube:
    def __init__(self, x=0, y=0, dx=0, dy=0):
        self.image = ""
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
    
    def load_image(self):
        self.image = pygame.image.load('Teal_cube.PNG')
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]
    
    def draw_image(self):
        screen.blit(self.image, [self.x, self.y])
        

    def move_x(self):
        self.x += self.dx
    
    def move_y(self):
        self.y += self.dy
    
    def check_out_of_screen(self):
        if self.x + self.width > WINDOW_WIDTH or self.x < 0:
            self.x -= self.dx
    
    def check_crash(self, cube):
        if (self.x + self.width > cube.x) and (self.x < cube.x + cube.width) and (self.y < cube.y + cube.height) and (self.y + self.height > cube.y):
            return True
        else:
            return False

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PyCube: Avoid Cube Game")
    clock = pygame.time.Clock()

    player = Cube((WINDOW_WIDTH / 2), (WINDOW_HEIGHT - 150), 0, 0)
    player.load_image()
    
    cubes = []
    cube_count = 3
    for i in range(cube_count):
        x = random.randrange(0, WINDOW_WIDTH - 55)
        y = random.randrange(-150, -50)
        cube = Cube(x, y, 0, random.randint(5, 10))
        cube.load_image()
        cubes.append(cube)
    
    lanes = []
    lane_width = 10
    lane_height = 80
    lane_margin = 20
    lane_count = 20
    lane_x = (WINDOW_WIDTH - lane_width) / 2
    lane_y = -10
    for i in range(lane_count):
        lanes.append([lane_x, lane_y])
        lane_y += lane_height + lane_margin

    score = 0
    crash = True
    game_on = True
    while game_on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_on = False
            
            if crash:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    crash = False
                    for i in range(cube_count):
                        cubes[i].x = random.randrange(0, WINDOW_WIDTH - cubes[i].width)
                        cubes[i].y = random.randrange(-150, -50)
                        cubes[i].load_image()
                    
                    player.load_image() # player색 바꾸기 싫으면 이 줄 제거
                    player.x = WINDOW_WIDTH / 2
                    player.dx = 0
                    score = 0
                    pygame.mouse.set_visible(False)
            if not crash:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 4
                    elif event.key == pygame.K_LEFT:
                        player.dx = -4
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        player.dx = 0
                    elif event.key == pygame.K_LEFT:
                        player.dx = 0

        screen.fill(GRAY)
                
