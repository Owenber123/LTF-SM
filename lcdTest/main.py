
import pygame
import smbus
import time
import RPi.GPIO as GPIO
#from pynput.mouse import Listener
import os
import sys
sys.path.append("MCP23017-python/src/")
from mcp23017 import *
from enum import Enum
from i2c import I2C

class State(Enum):
    INIT = 1
    LCD = 2
    CAP_OVERLAY = 3
    PASSED = 4
    FAILED = 5

# Initialize LCD BACKLIGHT PWM
#lcdpwmpin = 18
#global pwm
#GPIO.setmode(GPIO.BOARD)
#GPIO.setup(lcdpwmpin, GPIO.OUT)
#GPIO.output(lcdpwmpin, GPIO.LOW)
#pwm = GPIO.PWM(lcdpwmpin, 1000)
#pwm.start(0)

# Define Pins
REDLED = GPA0
GREENLED = GPA1
PASSSW = GPA2
FAILSW = GPA3

# Initialize I2C bus for expander board use
i2c = I2C(smbus.SMBus(11))
mcp = MCP23017(0x20, i2c) # MCP23017

# Configure led gpios as outputs
mcp.pin_mode(REDLED, OUTPUT)
mcp.pin_mode(GREENLED, OUTPUT)

# Configure pullup resistors on button ios
mcp.pin_mode(PASSSW, INPUT)
mcp.pin_mode(FAILSW, INPUT)

pygame.init()
screen_X = 800
screen_Y = 480
half_screen_X = screen_X // 2
half_screen_Y = screen_Y // 2
screen = pygame.display.set_mode((screen_Y, screen_X))
done = False
continue_test = True

red = (100,0,0)
blue = (0,50,100)
green = (0,100,0)
white = (255,255,255)
black = (0,0,0)
quadrant_color = black

quadrant_to_tap = 1
quadrant_1_coordinates = (5, 5, 390, 230)
quadrant_2_coordinates = (405, 5, 390, 230)
quadrant_3_coordinates = (5, 245, 390, 230)
quadrant_4_coordinates = (405, 245, 390, 230)
quadrant_coordinates = quadrant_1_coordinates

target_radius = 40

# create the display surface object
# of specific dimension..e(X, Y).
#display_surface = pygame.display.set_mode((screen_X, screen_Y))
display_surface = pygame.display.set_mode((screen_X, screen_Y), pygame.FULLSCREEN)


# set the pygame window name
pygame.display.set_caption('LCD and Capacitive Overlay Test')
 
# Create Test objets to display during test
font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 15)

# Generate Backgroudn image
#path = "/home/pi/Pictures"
picture = pygame.image.load("/home/pi/Pictures/testImage.png")
background_image = pygame.transform.scale(picture, (screen_X, screen_Y))

# Test Location
intro_text = font.render('LCD and Capacitive Overlay Test Starting', True, white, blue)
introRect = intro_text.get_rect()
introRect.center = (screen_X // 2, screen_Y // 3)

instruction = font.render('Press Green Button To Start', True, white, blue)
instructionRect = instruction.get_rect()
instructionRect.center = (screen_X // 2, screen_Y // 2 + screen_Y // 4)

lcd_instructions = font.render('Press Green Button if Image is Displayed', True, white, black)
lcd_instructionsRect = lcd_instructions.get_rect()
lcd_instructionsRect.center = (screen_X // 2, screen_Y // 2)

cap_overlay_instructions = small_font.render('Click Here', True, white, red)
cap_overlay_instructionsRect = cap_overlay_instructions.get_rect()

failed_text = font.render('Test Failed', True, white, red)
failed_textRect = failed_text.get_rect()
failed_textRect.center = (screen_X // 2, screen_Y // 2)

passed_text = font.render('Test Passed', True, white, green)
passed_textRect = passed_text.get_rect()
passed_textRect.center = (screen_X // 2, screen_Y // 2)


# define listener for touch screen presses
click_coordinates = [0] * 2

def set_xy(x, y):
    click_x = x
    click_y = y

#def on_click(x, y, button, pressed):
#    print("Pressed: ", pressed)
#    if (not pressed):
#        print("NOT PRESSED...Stop LIstener")
#        return False
#    print("XTYPE: ", type(x))
#    click_coordinates[0] = x
#    click_coordinates[1] = y
#    #click_x = x
#    #click_y = y
#    print ('Mouse clicked at ({0}, {1}) with {2}'.format(x, y, button))

#def listen_for_click():
#    with Listener(on_click=on_click) as listener:
#        listener.join()

def is_valid_click(quadrant_to_tap):
    print(quadrant_to_tap)
    coords = [0] * 4
    if quadrant_to_tap == 1:
        coords = quadrant_1_coordinates
    elif quadrant_to_tap == 2:
        coords = quadrant_2_coordinates
    elif quadrant_to_tap == 3:
        coords = quadrant_3_coordinates
    elif quadrant_to_tap == 4:
        coords = quadrant_4_coordinates

    if (((click_x > coords[0]) and (click_x < (coords[0] + coords[2]))) and ((click_y > coords[1]) and (click_y < (coords[1] + coords[3])))):
        print(coords)
        print(click_x)
        print(click_y)
        return True
    else:
        return False

# Init params
clock = pygame.time.Clock()
state = State.INIT
screen.fill(black)
update_screen = 0
restart_test = False

def reset_test():
        restart_test = False
        state = State.INIT
        quadrant_to_tap = 1
        quadrant_color = black
#        time.sleep(1)

while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        continue_test = True
                        if state == State.PASSED or state == State.FAILED:
                                restart_test = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        state = State.FAILED
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
                        done = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        click_x = mouse[0]
                        click_y = mouse[1]
                        print("click: ", mouse[0], " ", mouse[1]);
        
        pressed = pygame.key.get_pressed()
        if mcp.digital_read(FAILSW) == HIGH:
                state = State.FAILED
        if continue_test:
            if state == State.INIT:
                if pressed[pygame.K_SPACE] or mcp.digital_read(PASSSW) == HIGH:
                    state = State.LCD
                    time.sleep(1)
                screen.fill(blue)
                display_surface.blit(intro_text, introRect)
                display_surface.blit(instruction, instructionRect)
                mcp.digital_write(REDLED, LOW)
                mcp.digital_write(GREENLED, LOW)

            elif state == State.LCD:
                screen.fill(blue)
                if pressed[pygame.K_SPACE] or mcp.digital_read(PASSSW) == HIGH:
                    state = State.CAP_OVERLAY
                    screen.fill(blue)
                    time.sleep(1)
                screen.blit(background_image, [0, 0])
                display_surface.blit(lcd_instructions, lcd_instructionsRect)

            elif state == State.CAP_OVERLAY:
                screen.fill(blue)
                if quadrant_to_tap == 1:
                    quadrant_coordinates = quadrant_1_coordinates
                    cap_overlay_instructionsRect.center = (screen_X // 4, screen_Y // 4)
                    if pressed[pygame.K_UP]:
                        quadrant_color = green
                        quadrant_to_tap += 1
                        time.sleep(1)
                elif quadrant_to_tap == 2:
                    cap_overlay_instructionsRect.center = (screen_X * 3 // 4, screen_Y // 4)
                    quadrant_coordinates = quadrant_2_coordinates
                    quadrant_color = black
                    pygame.draw.rect(screen, green, pygame.Rect(quadrant_1_coordinates))
                    if pressed[pygame.K_UP]:
                        quadrant_color = green
                        quadrant_to_tap += 1
                        time.sleep(1)
                elif quadrant_to_tap == 3:
                    cap_overlay_instructionsRect.center = (screen_X // 4, screen_Y * 3 // 4)
                    quadrant_coordinates = quadrant_3_coordinates
                    quadrant_color = black
                    pygame.draw.rect(screen, green, pygame.Rect(quadrant_1_coordinates))
                    pygame.draw.rect(screen, green, pygame.Rect(quadrant_2_coordinates))
                    if pressed[pygame.K_UP]:
                        quadrant_color = green
                        quadrant_to_tap += 1
                        time.sleep(1)
                elif quadrant_to_tap == 4:
                    cap_overlay_instructionsRect.center = (screen_X * 3 // 4, screen_Y * 3 // 4)
                    quadrant_coordinates = quadrant_4_coordinates
                    quadrant_color = black
                    pygame.draw.rect(screen, green, pygame.Rect(quadrant_1_coordinates))
                    pygame.draw.rect(screen, green, pygame.Rect(quadrant_2_coordinates))
                    pygame.draw.rect(screen, green, pygame.Rect(quadrant_3_coordinates))
                    if pressed[pygame.K_UP]:
                        quadrant_color = green
                        quadrant_to_tap += 1
                        time.sleep(1)
                else:
                    state = State.PASSED
                    
                if(update_screen):
                    if event.type == pygame.MOUSEBUTTONDOWN:
                    #listen_for_click()
	                    if is_valid_click(quadrant_to_tap):
	                        print("valid Tap")
	                        quadrant_to_tap += 1
	                        update_screen = 0
                else:
                    update_screen = 1

                pygame.draw.rect(screen, black, pygame.Rect(quadrant_coordinates))
                target_center = cap_overlay_instructionsRect.center
                pygame.draw.circle(screen, red, target_center, target_radius)
                display_surface.blit(cap_overlay_instructions, cap_overlay_instructionsRect)


            elif state == State.PASSED:
                screen.fill(green)
                display_surface.blit(passed_text, passed_textRect)
                mcp.digital_write(GREENLED, HIGH)
                mcp.digital_write(REDLED, LOW)
                if(mcp.digital_read(PASSSW) == HIGH):
                       restart_test = 1

            elif state == State.FAILED:
                # Attempt to retry conneciton if during Capacitive Overlay Test
                screen.fill(red)
                display_surface.blit(failed_text, failed_textRect)
                mcp.digital_write(REDLED, HIGH)
                mcp.digital_write(GREENLED, LOW)
                if(mcp.digital_read(PASSSW) == HIGH):
                       restart_test = 1

        else:
#                if (state == State.CAP_OVERLAY):
#                        state = State.INIT
                screen.fill(red)
                display_surface.blit(failed_text, failed_textRect)
                mcp.digital_write(REDLED, HIGH)

        if restart_test:
                restart_test = False
                state = State.INIT
                quadrant_to_tap = 1
                quadrant_color = black
                time.sleep(1)
                #reset_test()
	# Update Frame
        pygame.display.update()

        # 30 frames a second
        clock.tick(30)

#        if state == State.PASSED or state == State.FAILED:
#                while(1):
#                        if (mcp.digital_read(PASSSW) == HIGH):
#                                reset_test()

print("QUITTING TEST")
