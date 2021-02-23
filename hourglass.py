import os
import sys
import time
import math
import pygame as pg
from pygame.locals import *

# Declares the color values; these are purposely muted to be autism-friendly
black  = (  0,   0,   0)
white  = (255, 255, 255)
d_grey = (211, 211, 211)
l_grey = (230, 230, 230)
green  = (182, 214, 193)
yellow = (232, 205, 160)
red    = (240, 180, 159)

pg.init()                               # Starts the PyGame engine
pg.display.set_caption('Visual Timer')  # The window titla
my_font = pg.font.SysFont('Comic Sans MS', 20)
title_font = pg.font.SysFont('Comic Sans MS', 50)

# Set the height and width of the screen
# RasPi 7" screen is 800x480
# Use the first screen line for testing and the second for use
screen = pg.display.set_mode([800, 480])
#screen = pg.display.set_mode(size, pg.FULLSCREEN)


# Function to draw the timer as a gradient from green to yellow to red
def draw_gradient(r, g, b):
    for i in range(476):    # This for loop is lower than 480 so it doesn't go past the rounded corners of the timer
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

# The timer screen
def timer_screen(done=False, check=0.00, top=1, timer=60):
    # Grey background color, draws the timer boundaries, and sets the gradient
    resolution = timer / 480
    screen.fill(l_grey)
    draw_gradient(green[0], green[1], green[2])

    # The main loop which ticks the timer down
    while not done:
        # Draws the frame and buttons each loop
        pg.draw.rect(screen, black, [150, 0, 500, 480], 6, border_radius=10)

        # Reset button with black outline
        button_reset = pg.draw.circle(screen, white, [75, 250], 40)
        button_outl1 = pg.draw.circle(screen, black, [75, 250], 40, 4)

        # Menu button with black outline
        button_menu  = pg.draw.circle(screen, white, [725, 250], 40)
        button_outl2 = pg.draw.circle(screen, black, [725, 250], 40, 4)

        # Button text
        label_reset  = my_font.render('Reset', True, black)
        label_menu   = my_font.render('Menu', True, black)

        # Creates objects out of the buttons for click/tap detection
        screen.blit(label_reset, [50, 235])
        screen.blit(label_menu, [700, 235])

        # Handles closing the window or any button presses
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if button_menu.collidepoint(pos):
                    main_screen(done=False)
                if button_reset.collidepoint(pos):
                    draw_gradient(green[0], green[1], green[2])
                    top = 1
                    check = 0.00

        # If enough time has passed, remove a layer of pixels
        if check < float(time.time()):
            pg.draw.rect(screen, d_grey, [153, top, 494, 1])        # Fills in the top line with the bkgnd color
            pg.draw.rect(screen, black, [153, (top + 1), 494, 3])   # Makes the top line thicker & black
            check = float(time.time()) + resolution
            top += 1

        pg.display.flip()   # Updates the screen


def custom_time(done=False):
    screen.fill(l_grey)

    while not done:

        label_menu_text = title_font.render('Enter your time (minutes):', True, black)
        screen.blit(label_menu_text, [100, 50])

        pg.draw.rect(screen, white, [290, 150, 220, 60], border_radius=10)
        pg.draw.rect(screen, black, [290, 150, 220, 60], 8, border_radius=10)

        pg.draw.rect(screen, d_grey, [310, 220, 60, 60], border_radius=10)        # 1
        pg.draw.rect(screen, black,  [370, 220, 60, 60], border_radius=10)        # 2
        pg.draw.rect(screen, d_grey, [430, 220, 60, 60], border_radius=10)        # 3

        pg.draw.rect(screen, black,  [310, 280, 60, 60], border_radius=10)        # 4
        pg.draw.rect(screen, d_grey, [370, 280, 60, 60], border_radius=10)        # 5
        pg.draw.rect(screen, black,  [430, 280, 60, 60], border_radius=10)        # 6

        pg.draw.rect(screen, d_grey, [310, 340, 60, 60], border_radius=10)        # 7
        pg.draw.rect(screen, black,  [370, 340, 60, 60], border_radius=10)        # 8
        pg.draw.rect(screen, d_grey, [430, 340, 60, 60], border_radius=10)        # 9

        pg.draw.rect(screen, red,    [310, 400, 60, 60], border_radius=10)        # Backspace button
        pg.draw.rect(screen, d_grey, [370, 400, 60, 60], border_radius=10)        # 0
        pg.draw.rect(screen, green,  [430, 400, 60, 60], border_radius=10)      # Enter button

        button_reset = pg.draw.circle(screen, white, [725, 400], 40)
        button_outl2 = pg.draw.circle(screen, black, [725, 400], 40, 4)
        label_menu = my_font.render('Menu', True, black)
        screen.blit(label_menu, [700, 385])

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                exit()

        pg.display.flip()


def main_screen(done=False):
    screen.fill(l_grey)

    while not done:
        # Draws the buttons
        button_10min = pg.draw.circle(screen, white, [160, 260], 60)
        button_15min = pg.draw.circle(screen, white, [320, 260], 60)
        button_30min = pg.draw.circle(screen, white, [480, 260], 60)
        button_60min = pg.draw.circle(screen, white, [640, 260], 60)

        button_custom = pg.draw.rect(screen, white, [240, 380, 320, 75], border_radius=15)

        # Creates the text
        label_10min = my_font.render('10 min', True, black)
        label_15min = my_font.render('15 min', True, black)
        label_30min = my_font.render('30 min', True, black)
        label_60min = my_font.render('60 min', True, black)

        label_custom = my_font.render('Custom Time', True, black)

        label_menu_text = title_font.render('Please select a time', True, black)

        # Turns the buttons into objects
        screen.blit(label_10min, [130, 245])
        screen.blit(label_15min, [290, 245])
        screen.blit(label_30min, [450, 245])
        screen.blit(label_60min, [610, 245])

        screen.blit(label_custom, [340, 400])

        screen.blit(label_menu_text, [190, 80])

        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                exit()
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if button_10min.collidepoint(pos):
                    timer_screen(False, 0.00, 1, 600)
                if button_15min.collidepoint(pos):
                    timer_screen(False, 0.00, 1, 900)
                if button_30min.collidepoint(pos):
                    timer_screen(False, 0.00, 1, 1800)
                if button_60min.collidepoint(pos):
                    timer_screen(False, 0.00, 1, 3600)
                if button_custom.collidepoint(pos):
                    custom_time()

        pg.display.flip()


main_screen()

pg.quit()   # IDLE-friendly exit line
