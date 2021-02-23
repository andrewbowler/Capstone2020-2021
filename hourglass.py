import time
import math
import pygame as pg
from pygame.locals import *

# Declares the color values
black  = (  0,   0,   0)
white  = (255, 255, 255)
d_grey = (211, 211, 211)
l_grey = (230, 230, 230)
green  = (182, 214, 193)
yellow = (232, 205, 160)
red    = (240, 180, 159)

pg.init()                               # Starts the PyGame engine
pg.display.set_caption('Visual Timer')  # The window titla

# Set the height and width of the screen
# RasPi 7" screen is 800x480
# Use the first screen line for testing and the second for use
screen = pg.display.set_mode([800, 480])
#screen = pg.display.set_mode(size, pg.FULLSCREEN)

# Placeholder hard-coded values for how long it takes for the timer to tick down
timer = 30
resolution = timer / 480


# Function to draw the timer as a gradient from green to yellow to red
def draw_gradient(r, g, b):
    for i in range(472):    # This for loop is lower than 480 so it doesn't go past the rounded corners of the timer
        pg.draw.rect(screen, [math.floor(r), math.floor(g), math.floor(b)], [153, i, 494, 1])

        if r <= yellow[0]:
            r += abs((green[0] - yellow[0])) / 160
        elif r > yellow[0]:
            r += abs((yellow[0] - red[0])) / 160

        if g >= yellow[1]:
            g -= abs((green[1] - yellow[1])) / 160
        elif g < yellow[1]:
            g -= abs((yellow[1] - red[1])) / 160

        if b >= yellow[2]:
            b -= abs((green[2] - yellow[2])) / 160
        elif b < yellow[2]:
            b -= abs((yellow[2] - red[2])) / 160
        pg.display.flip()

# TODO:
#def main_screen():

# The timer screen
def timer_screen(done=False, check=0.00, top=1):
    # Grey background color, draws the timer boundaries, and sets the gradient
    screen.fill(l_grey)
    draw_gradient(green[0], green[1], green[2])
    my_font = pg.font.SysFont('Comic Sans MS', 20)

    # The main loop which ticks the timer down
    while not done:
        # Draws the frame and buttons each loop
        pg.draw.rect(screen, black, [150, 0, 500, 480], 8, border_radius=15)
        button_reset = pg.draw.circle(screen, white, [75, 250], 40)
        button_outl1 = pg.draw.circle(screen, black, [75, 250], 40, 4)
        button_menu  = pg.draw.circle(screen, white, [725, 250], 40)
        button_outl2 = pg.draw.circle(screen, black, [725, 250], 40, 4)
        label_reset  = my_font.render('Reset', True, black)
        label_menu   = my_font.render('Menu', True, black)
        screen.blit(label_reset, [50, 235])
        screen.blit(label_menu, [700, 235])

        # Handles closing the window or any button presses
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if button_menu.collidepoint(pos):
                    time.sleep(1)
                if button_reset.collidepoint(pos):
                    draw_gradient(green[0], green[1], green[2])
                    top = 1
                    check = 0.00

        # If enough time has passed, remove a layer of pixels
        if check < float(time.time()):
            pg.draw.rect(screen, d_grey, [153, top, 494, 1])
            pg.draw.rect(screen, black, [153, (top + 1), 494, 3])
            check = float(time.time()) + resolution
            top += 1

        pg.display.flip()   # Updates the screen

timer_screen()

pg.quit()   # IDLE-friendly exit line
