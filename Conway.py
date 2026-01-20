import pygame, sys
import numpy as np
from pygame.time import Clock

BUTTON_MENU_HEIGHT = 50
BUTTON_MENU_WIDTH = 601
CELL_SCREEN_HEIGHT = 601
CELL_SCREEN_WIDTH = 601
ROWS = 40
COLUMNS = 40
SPACE_HEIGHT = CELL_SCREEN_HEIGHT // ROWS
SPACE_WIDTH = CELL_SCREEN_WIDTH // COLUMNS

#This is the number of times I want the cells to update per second
CELL_PROG_FREQ = 3

time_running = False

pygame.init()
screen = pygame.display.set_mode((CELL_SCREEN_WIDTH + 1, CELL_SCREEN_HEIGHT + BUTTON_MENU_HEIGHT + 1))
pygame.display.set_caption('Conway\'s Game Of Life')
clock = pygame.time.Clock()
text_font = pygame.font.Font(None, 50)
button_font = pygame.font.Font(None, 20)

#cell state array, 0 will be a dead cell, 1 will be an alive cell
cell_states = np.zeros((ROWS, COLUMNS))

#creating the surface for the cells
cell_surface = pygame.Surface((CELL_SCREEN_WIDTH, CELL_SCREEN_HEIGHT))
button_surface = pygame.Surface((BUTTON_MENU_WIDTH, BUTTON_MENU_HEIGHT))

progressing_surface = text_font.render('Progression Active', None, 'white')

class Button:
    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.clicked = False

    def draw(self):
        global time_running
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                time_running = not time_running
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        pygame.draw.rect(screen, '#404040', (self.x, self.y, self.width, self.height))
        text_surface = button_font.render(self.text, False, 'white')
        text_x = self.x + self.width // 10
        text_y = self.y + self.height // 4
        screen.blit(text_surface, (text_x, text_y))

def draw_grid():
    for x in range(0, CELL_SCREEN_WIDTH + SPACE_WIDTH, SPACE_WIDTH):
        pygame.draw.line(cell_surface, 'grey', (x, 0), (x, CELL_SCREEN_HEIGHT))
    for y in range(0, CELL_SCREEN_HEIGHT + SPACE_HEIGHT, SPACE_HEIGHT):
        pygame.draw.line(cell_surface, 'grey', (0, y), (CELL_SCREEN_WIDTH, y))

    return

def light_cell(x, y):
    pygame.draw.rect(cell_surface, "yellow", (x, y, SPACE_WIDTH, SPACE_HEIGHT))
    return

def dark_cell(x, y):
    pygame.draw.rect(cell_surface, "black", (x, y, SPACE_WIDTH, SPACE_HEIGHT))
    return

def update_cells():
    for x in range(ROWS):
        for y in range(COLUMNS):
            if cell_states[(y, x)] == 1:
                light_cell(x * SPACE_WIDTH, y * SPACE_HEIGHT)
            else:
                dark_cell(x * SPACE_WIDTH, y * SPACE_HEIGHT)
    return

def progress_cell_states():
    global cell_states
    cells = cell_states.copy()

    for p in range(ROWS):
         for q in range(COLUMNS):
            row_start = max(0, q - 1)
            row_end = min(cell_states.shape[0], q + 2)
            col_start = max(0, p - 1)
            col_end = min(cell_states.shape[1], p + 2)

            slice_1 = cells[row_start:row_end, col_start:col_end]
            slice_sum = slice_1.sum()

            if not(cells[(q, p)]) and slice_sum == 3:
                cell_states[(q, p)] = 1
            elif cells[(q, p)] and not(slice_sum == 3) and not(slice_sum == 4):
                cell_states[(q, p)] = 0
    return


toggle = Button(0, CELL_SCREEN_HEIGHT + 1, 150, 40, 'Toggle Progression')

#loop counter is used to slow down cell progression without slowing the game loop
loop_counter = 0
loop_reset_value = 60 // CELL_PROG_FREQ

while True:
    loop_counter += 1
    loop_counter = loop_counter % loop_reset_value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if pygame.mouse.get_pressed()[0] and time_running == False:
            box_x = pygame.mouse.get_pos()[0] // SPACE_WIDTH
            box_y = pygame.mouse.get_pos()[1] // SPACE_HEIGHT

            if 0 < box_x < ROWS and 0 < box_y < COLUMNS:
                if cell_states[(box_y, box_x)] == 0:
                    cell_states[(box_y, box_x)] = 1
                else:
                    cell_states[(box_y, box_x)] = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                time_running = not time_running

        if time_running:
            screen.blit(progressing_surface, (CELL_SCREEN_WIDTH // 3, CELL_SCREEN_HEIGHT + 1))
        else:
            pygame.draw.rect(screen, 'black', (CELL_SCREEN_WIDTH // 3, CELL_SCREEN_HEIGHT + 1, 2 * CELL_SCREEN_WIDTH // 2, BUTTON_MENU_WIDTH))
            pygame.display.update()


    if time_running and loop_counter == 0:
        progress_cell_states()


    update_cells()
    draw_grid()

    screen.blit(cell_surface, (0, 0))
    toggle.draw()
    pygame.display.update()
    clock.tick(60)
