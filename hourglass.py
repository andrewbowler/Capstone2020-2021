##**************************************************
## FILE:        hourglass.py
## PROJECT:     Bridgewell Visual Timer
## DATE:        20210222
## AUTHOR:      Drew Bowler
## PHONE #:     (978) 763-5124
## EMAIL:       arbowl@tutanota.com
##
## PURPOSE:     To display a visual hourglass timer
##              to track the passage of time for
##              those with cognitive impairments
##              that struggle to intuitively
##              understand traditional clocks.
##
## INPUT:       User input (time in minutes)
## OUTPUT:      Hourglass timer visuals
##
## REVISED:     20210223
##
## COMMENT:     Fixed time spent/left over/underflow
##**************************************************

import os
import sys
import time
import math
import pygame as pg
from pygame.locals import *

# Declares the color values; these are purposely muted to be easy on the eyes
black  = (  0,   0,   0)
white  = (255, 255, 255)
d_grey = (166, 166, 166)
m_grey = (200, 200, 200)
l_grey = (220, 220, 220)
green  = (182, 214, 193)
yellow = (232, 205, 160)
red    = (240, 180, 159)

pg.init()                               # Starts the PyGame engine
pg.display.set_caption('Visual Timer')  # The window title

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


# Easily prints lines of text where maintaining the line as an object isn't important
def print_line(text, size, x, y):
    screen.blit(pg.font.SysFont('Comic Sans MS', size).render(text, True, black), [x, y])


# The timer screen
def timer_screen(done=False, check=0.00, top=1, timer=60):
    # Grey background color, draws the timer boundaries, and sets the gradient
    times_up = False
    flash_check = 0
    time_finished = 0
    menu_tick_one, menu_tick_two = white, white
    reset_tick_one, reset_tick_two, reset_tick_three = white, white, white
    reset_time, menu_time = 0, 0
    reset_counter, menu_counter = 0, 0
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
        print_line('Reset', 20, 50, 235)
        print_line('Menu', 20, 700, 235)

        # Rectangles and counters for the reset button
        pg.draw.rect(screen, white, [55, 300, 40, 20])
        pg.draw.rect(screen, black, [55, 300, 40, 20], 4)
        pg.draw.rect(screen, reset_tick_one,   [59, 306, 9, 9], border_radius=3)
        pg.draw.rect(screen, reset_tick_two,   [71, 306, 9, 9], border_radius=3)
        pg.draw.rect(screen, reset_tick_three, [83, 306, 9, 9], border_radius=3)
        pg.draw.rect(screen, black, [59, 306, 9, 9], 3, border_radius=3)
        pg.draw.rect(screen, black, [71, 306, 9, 9], 3, border_radius=3)
        pg.draw.rect(screen, black, [83, 306, 9, 9], 3, border_radius=3)

        # Rectangles and counters for the menu button
        pg.draw.rect(screen, white, [705, 300, 40, 20])
        pg.draw.rect(screen, black, [705, 300, 40, 20], 4)
        pg.draw.rect(screen, menu_tick_one, [709, 306, 9, 9], border_radius=3)
        pg.draw.rect(screen, menu_tick_two, [721, 306, 9, 9], border_radius=3)
        pg.draw.rect(screen, black, [709, 306, 9, 9], 3, border_radius=3)
        pg.draw.rect(screen, black, [721, 306, 9, 9], 3, border_radius=3)
        pg.draw.rect(screen, black, [733, 306, 9, 9], 3, border_radius=3)

        # Time elapsed in minutes
        if times_up is False:
            time_spent = math.floor(top * resolution / 60)

        # Time left in minutes
        if times_up is False:
            time_left = math.ceil((480 - top) * resolution / 60)

        # Handles the spacing for 0, 1, and double digit numbers
        if len(str(time_spent)) < 2:
            if time_spent == 1:
                spent_spacing = 36
            else:
                spent_spacing = 29
        else:
            spent_spacing = 24

        # Handles the plural of "minute"
        if time_spent == 1:
            spent_minute = ' minute'
        else:
            spent_minute = ' minutes'

        # Handles the plural of "minute"
        if time_left == 1:
            left_minute = ' minute'
        else:
            left_minute = ' minutes'

        # Handles the spacing for 0, 1, and double digit numbers
        if len(str(time_left)) < 2:
            if time_left == 1:
                left_spacing = 686
            else:
                left_spacing = 679
        else:
            left_spacing = 674

        # Rectangles for "time spent"
        pg.draw.rect(screen, white, [20, 20, 110, 100], border_radius=15)
        pg.draw.rect(screen, black, [20, 20, 110, 100], 4, border_radius=15)
        print_line('Time Spent:', 15, 33, 30)
        print_line(str(time_spent) + spent_minute, 20, spent_spacing, 65)

        # Rectangles for "time left"
        pg.draw.rect(screen, white, [670, 20, 110, 100], border_radius=15)
        pg.draw.rect(screen, black, [670, 20, 110, 100], 4, border_radius=15)
        print_line('Time Left:', 15, 690, 30)
        print_line(str(time_left) + left_minute, 20, left_spacing, 65)

        # If enough time has passed, remove a layer of pixels
        if check < float(time.time()):
            pg.draw.rect(screen, d_grey, [156, top, 488, 1])        # Fills in the top line with the bkgnd color

            # This "if" statement flashes the background of the timer in shades of grey for the last 5%
            if top >= 456 and times_up is False:
                if math.floor(time.time()) % 3 != 0:
                    pg.draw.rect(screen, m_grey, [150, 3, 500, top - 3], border_top_left_radius=15, border_top_right_radius=15)
                    pg.draw.rect(screen, black, [150, 0, 500, 480], 6, border_radius=10)
                else:
                    pg.draw.rect(screen, d_grey, [150, 6, 500, top - 3], border_radius=15)
                    pg.draw.rect(screen, black, [150, 0, 500, 480], 6, border_radius=10)

            pg.draw.rect(screen, black, [153, (top + 1), 494, 3])   # Makes the top line thicker & black
            check = float(time.time()) + resolution
            top += 1

        # Resets the reset counter if it hasn't been pressed for 3 seconds
        if (reset_time + 3) < float(time.time()):
            reset_counter = 0
            reset_tick_one, reset_tick_two, reset_tick_three = white, white, white

        # Resets the menu counter if it hasn't been pressed for 3 seconds
        if (menu_time + 3) < float(time.time()):
            menu_counter = 0
            menu_tick_one, menu_tick_two = white, white

        # If the timer reaches the bottom, it displays "Time is up!" Users can reset or go back to menu
        if top > 480:
            times_up      = True
            time_left     = 0
            time_spent    = math.floor(timer / 60)
            time_elapsed  = math.ceil(timer / 60)
            pg.draw.rect(screen, d_grey, [150, 6, 500, 480], border_radius=15)
            pg.draw.rect(screen, black, [150, 0, 500, 480], 6, border_radius=10)

            # If only one minute is set, the grammar will still be correct (and correctly spaced)
            if time_elapsed == 1:
                elapsed_minute  = ' minute elapsed)'
                elapsed_spacing = 270
            else:
                elapsed_minute  = ' minutes elapsed)'
                elapsed_spacing = 260

            # Shows how long the timer has been done for when it runs out
            if time_finished == 0:
                pg.draw.rect(screen, d_grey, [320, 300, 200, 100])
                time_finished_start = math.floor(time.time())
                seconds_displayed = '00'
                minutes_displayed = '0'
                time_finished = 1
            else:
                pg.draw.rect(screen, d_grey, [320, 300, 200, 100])
                seconds_finished  = math.floor(time.time()) - time_finished_start
                minutes_displayed = str(math.floor(seconds_finished / 60))
                seconds_displayed = str(math.floor(seconds_finished) % 60)

                if len(seconds_displayed) == 1:
                    seconds_displayed = '0' + seconds_displayed

                print_line(minutes_displayed + ':' + seconds_displayed, 30, 365, 350)

            print_line('Time is up!', 50, 270, 180)
            print_line('(' + str(time_elapsed) + elapsed_minute, 30, elapsed_spacing, 250)

        # Handles closing the window or any button presses
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()

                if button_menu.collidepoint(pos):
                    menu_counter += 1
                    menu_time = float(time.time())

                    if menu_counter == 1:
                        menu_tick_one = black
                    if menu_counter == 2:
                        menu_tick_two = black
                    if menu_counter == 3:
                        main_screen(done=False)

                if button_reset.collidepoint(pos):
                    reset_counter += 1
                    reset_time = float(time.time())

                    if reset_counter == 1:
                        reset_tick_one = black
                    if reset_counter == 2:
                        reset_tick_two = black
                    if reset_counter == 3:
                        reset_tick_three = black
                        draw_gradient(green[0], green[1], green[2])
                        top = 1
                        check = 0.00
                        time_finished = 0
                        reset_counter = 0
                        times_up = False

        pg.display.flip()   # Updates the screen


# On this screen you can input a custom time in minutes and set the timer to that
def custom_time(done=False):
    screen.fill(l_grey)
    timer_custom = ''

    while not done:
        print_line('Enter your time (minutes):', 50, 100, 50)

        pg.draw.rect(screen, white, [290, 150, 220, 60], border_radius=10)
        pg.draw.rect(screen, black, [290, 150, 220, 60], 6, border_radius=10)

        print_line(timer_custom, 30, 300, 157)

        button_one = pg.draw.rect(screen, d_grey, [310, 220, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [310, 220, 60, 60], 2, border_radius=10)
        print_line('1', 30, 333, 230)

        button_two = pg.draw.rect(screen, d_grey, [370, 220, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [370, 220, 60, 60], 2, border_radius=10)
        print_line('2', 30, 393, 230)

        button_three = pg.draw.rect(screen, d_grey, [430, 220, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [430, 220, 60, 60], 2, border_radius=10)
        print_line('3', 30, 453, 230)

        button_four = pg.draw.rect(screen, d_grey, [310, 280, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [310, 280, 60, 60], 2, border_radius=10)
        print_line('4', 30, 333, 290)

        button_five = pg.draw.rect(screen, d_grey, [370, 280, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [370, 280, 60, 60], 2, border_radius=10)
        print_line('5', 30, 393, 290)

        button_six = pg.draw.rect(screen, d_grey, [430, 280, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [430, 280, 60, 60], 2, border_radius=10)
        print_line('6', 30, 453, 290)

        button_seven = pg.draw.rect(screen, d_grey, [310, 340, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [310, 340, 60, 60], 2, border_radius=10)
        print_line('7', 30, 333, 350)

        button_eight = pg.draw.rect(screen, d_grey, [370, 340, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [370, 340, 60, 60], 2, border_radius=10)
        print_line('8', 30, 393, 350)

        button_nine = pg.draw.rect(screen, d_grey, [430, 340, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [430, 340, 60, 60], 2, border_radius=10)
        print_line('9', 30, 453, 350)

        button_del = pg.draw.rect(screen, red,    [310, 400, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [310, 400, 60, 60], 2, border_radius=10)
        print_line('Del', 30, 317, 410)

        button_zero = pg.draw.rect(screen, d_grey, [370, 400, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [370, 400, 60, 60], 2, border_radius=10)
        print_line('0', 30, 393, 410)

        button_go = pg.draw.rect(screen, green,  [430, 400, 60, 60], border_radius=10)
        pg.draw.rect(screen, black,  [430, 400, 60, 60], 2, border_radius=10)
        print_line('Go', 30, 445, 410)

        button_menu  = pg.draw.circle(screen, white, [725, 400], 40)
        button_outl2 = pg.draw.circle(screen, black, [725, 400], 40, 4)
        print_line('Menu', 30, 700, 385)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()
                if button_menu.collidepoint(pos):
                    main_screen(done=False)

                if button_one.collidepoint(pos):
                    timer_custom += '1'

                if button_two.collidepoint(pos):
                    timer_custom += '2'

                if button_three.collidepoint(pos):
                    timer_custom += '3'

                if button_four.collidepoint(pos):
                    timer_custom += '4'

                if button_five.collidepoint(pos):
                    timer_custom += '5'

                if button_six.collidepoint(pos):
                    timer_custom += '6'

                if button_seven.collidepoint(pos):
                    timer_custom += '7'

                if button_eight.collidepoint(pos):
                    timer_custom += '8'

                if button_nine.collidepoint(pos):
                    timer_custom += '9'

                if button_del.collidepoint(pos):
                    timer_custom = timer_custom[:-1]

                if button_zero.collidepoint(pos):
                    timer_custom += '0'

                if button_go.collidepoint(pos):
                    if timer_custom != '':
                        timer_screen(False, 0.00, 1, 60 * int(timer_custom))
                    else:
                        pass

                if len(timer_custom) > 6:
                    timer_custom = timer_custom[:-1]

        pg.display.flip()


# Displays information about how to use, how to charge, who to contact, etc.
def help_screen(done=False):
    screen.fill(l_grey)

    uml = pg.image.load('uml.jpg').convert()
    bw  = pg.image.load('bw.jpg').convert()

    print_line('Bridgewell Visual Timer', 50, 130, 80)

    print_line('This visual timer was designed in the spring of 2021 by capstone engineering students at the University', 15, 40, 180)
    print_line('of Massachusetts Lowell for the clients at Bridgewell.', 15, 40, 195)

    print_line('To enter a time, either select a time on the main menu screen, or input a custom time via the number pad', 15, 40, 230)
    print_line('on the "Custom Time" screen.', 15, 40, 245)

    print_line('To reset the timer at the last given time or go back to the main menu from the timer screen, press either', 15, 40, 280)
    print_line('button three times within three seconds.', 15, 40, 295)

    print_line('To charge the device, use a USB-C cable connected to a wall wart (most normal phone charger blocks,', 15, 40, 330)
    print_line('including those for iPhones, will work).', 15, 40, 345)

    print_line('For any questions not answered in the manual, please contact the creator at:', 15, 40, 380)
    print_line('Phone: (978) 763-5124', 15, 40, 395)
    print_line('Email: arbowl@tutanota.com', 15, 40, 410)

    button_menu = pg.draw.circle(screen, white, [725, 400], 40)
    button_outl2 = pg.draw.circle(screen, black, [725, 400], 40, 4)

    print_line('Menu', 20, 700, 385)

    screen.blit(uml, [0, 0])
    screen.blit(bw, [700, 0])

    while not done:
        # Event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
                exit()

            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                pos = pg.mouse.get_pos()

                if button_menu.collidepoint(pos):
                    main_screen(done=False)

        pg.display.flip()


# Main function. Pressing a button with a time on it sets the timer to that time, or you can set a custom time
def main_screen(done=False):
    screen.fill(l_grey)

    # Draws the buttons
    button_10min   = pg.draw.circle(screen, white, [160, 260], 60)
    button_10bor   = pg.draw.circle(screen, black, [160, 260], 60, 4)
    button_15min   = pg.draw.circle(screen, white, [320, 260], 60)
    button_15bor   = pg.draw.circle(screen, black, [320, 260], 60, 4)
    button_30min   = pg.draw.circle(screen, white, [480, 260], 60)
    button_30bor   = pg.draw.circle(screen, black, [480, 260], 60, 4)
    button_60min   = pg.draw.circle(screen, white, [640, 260], 60)
    button_60bor   = pg.draw.circle(screen, black, [640, 260], 60, 4)
    button_custom  = pg.draw.rect(screen, white,   [240, 380, 320, 75], border_radius=15)
    button_cusbor  = pg.draw.rect(screen, black,   [240, 380, 320, 75], 4, border_radius=15)
    button_help    = pg.draw.circle(screen, white, [50, 430], 30)
    button_helpbor = pg.draw.circle(screen, black, [50, 430], 30, 4)

    # Creates the text
    print_line('10 min', 20, 130, 245)
    print_line('15 min', 20, 290, 245)
    print_line('30 min', 20, 450, 245)
    print_line('60 min', 20, 610, 245)
    print_line('Custom Time', 20, 340, 400)
    print_line('Help', 20, 29, 415)

    # Large splash screen text
    print_line('Please select a time:', 50, 170, 80)

    while not done:
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

                if button_help.collidepoint(pos):
                    help_screen()

        pg.display.flip()


main_screen()

pg.quit()   # IDLE-friendly exit line
