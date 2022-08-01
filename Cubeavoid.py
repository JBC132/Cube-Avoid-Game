from tkinter.tix import WINDOW
import pygame
import random
import turtle as t
from time import sleep

WINDOW_WIDTH = 480
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
    
    def load_player_image(self):
        self.image = pygame.image.load('Cubes\Teal_cube.PNG')
        self.width = self.image.get_rect().size[0]
        self.height = self.image.get_rect().size[1]
    
    def load_enemy_image(self):
        self.image = pygame.image.load('Cubes\Red_cube.PNG')
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

# main menu function
def draw_main_menu():
    draw_x = (WINDOW_WIDTH / 2) - 200
    draw_y = WINDOW_HEIGHT / 2
    image_intro = pygame.image.load('Cubes\The_Cube.PNG')
    screen.blit(image_intro, [draw_x, draw_y - 300])
    font_40 = pygame.font.SysFont("FixedSys", 40, True, False)
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_title = font_40.render("PyCube: Cube Avoid", True, GRAY)
    screen.blit(text_title, [draw_x, draw_y])
    text_score = font_40.render("Score: " + str(score), True, WHITE)
    screen.blit(text_score, [draw_x, draw_y + 70])
    text_start = font_30.render("Press Space Key to Start.", True, RED)
    screen.blit(text_start, [draw_x, draw_y + 140])
    pygame.display.flip()

# in-game score function
def draw_score():
    font_30 = pygame.font.SysFont("FixedSys", 30, True, False)
    text_score = font_30.render("Score: " + str(score), True, WHITE)
    screen.blit(text_score, [15, 15])

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("PyCube: Avoid Cube Game")
    clock = pygame.time.Clock()

    # making player cube
    player = Cube(WINDOW_WIDTH / 2, WINDOW_HEIGHT - 150, 0, 0)
    player.load_player_image()
    
    # making enemy cubes
    cubes = []
    cube_count = 3
    for i in range(cube_count):
        x = random.randrange(0, WINDOW_WIDTH - 55)
        y = random.randrange(-150, -50)
        cube = Cube(x, y, 0, random.randint(5, 10))
        cube.load_enemy_image()
        cubes.append(cube)
    
    # making white lines
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
            
            # restart game
            if crash:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    crash = False
                    for i in range(cube_count):
                        cubes[i].x = random.randrange(0, WINDOW_WIDTH - cubes[i].width)
                        cubes[i].y = random.randrange(-150, -50)
                        cubes[i].load_enemy_image()
                    
                    player.load_player_image() # player색 바꾸기 싫으면 이 줄 제거
                    player.x = WINDOW_WIDTH / 2
                    player.dx = 0
                    score = 0
                    pygame.mouse.set_visible(False)

            # move cube        
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

        screen.fill(BLACK)

        # load/print game on screen        
        if not crash:
            # moving white lines
            for i in range(lane_count):
                pygame.draw.rect(screen, WHITE, [lanes[i][0], lanes[i][1], lane_width, lane_height])
                lanes[i][1] += 10
                if lanes[i][1] > WINDOW_HEIGHT:
                    lanes[i][1] = -40 - lane_height

            # player cube
            player.draw_image()
            player.move_x()
            player.check_out_of_screen()

            # enemy cube
            for i in range(cube_count):
                cubes[i].draw_image()
                cubes[i].y += cubes[i].dy
                if cubes[i].y > WINDOW_HEIGHT:
                    score += 10
                    cubes[i].x = random.randrange(0, WINDOW_WIDTH - cubes[i].width)
                    cubes[i].y = random.randrange(-150, -50)
                    cubes[i].dy = random.randint(5, 10)
                    cubes[i].load_enemy_image()

            # check crashes
            for i in range(cube_count):
                if player.check_crash(cubes[i]):
                    crash = True
                    sleep(2)
                    pygame.mouse.set_visible(True)
                    break

            draw_score()
            pygame.display.flip()

        else:
            draw_main_menu()
        
        clock.tick(60)

    pygame.quit()
