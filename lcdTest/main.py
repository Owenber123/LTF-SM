import pygame
from enum import Enum
import time

class State(Enum):
    INIT = 1
    LCD = 2
    CAP_OVERLAY = 3
    PASSED = 4
    FAILED = 5
    
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
display_surface = pygame.display.set_mode((screen_X, screen_Y))
 
# set the pygame window name
pygame.display.set_caption('LCD and Capacitive Overlay Test')
 
# Create Test objets to display during test
font = pygame.font.Font('freesansbold.ttf', 32)
small_font = pygame.font.Font('freesansbold.ttf', 15)

# Generate Backgroudn image
picture = pygame.image.load("testImage2.png")
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


# Init params
clock = pygame.time.Clock()
state = State.INIT
screen.fill(black)
while not done:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        done = True
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        continue_test = True
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                        continue_test = False
        pressed = pygame.key.get_pressed()
        
        if continue_test:
            if state == State.INIT:
                if pressed[pygame.K_SPACE]:
                    state = State.LCD
                    time.sleep(1)
                screen.fill(blue)
                display_surface.blit(intro_text, introRect)
                display_surface.blit(instruction, instructionRect)

            elif state == State.LCD:
                screen.fill(blue)
                if pressed[pygame.K_SPACE]:
                    state = State.CAP_OVERLAY
                    screen.fill(blue)
                    time.sleep(1)
                screen.blit(background_image, [0, 0])
                display_surface.blit(lcd_instructions, lcd_instructionsRect)

            elif state == State.CAP_OVERLAY:
                screen.fill(blue)
                if pressed[pygame.K_SPACE]:
                    state = State.PASSED
                    time.sleep(1)
                screen.fill(blue)
                if quadrant_to_tap == 1:
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

                pygame.draw.rect(screen, black, pygame.Rect(quadrant_coordinates))
                target_center = cap_overlay_instructionsRect.center
                pygame.draw.circle(screen, red, target_center, target_radius)
                display_surface.blit(cap_overlay_instructions, cap_overlay_instructionsRect)


            elif state == State.PASSED:
                screen.fill(green)
                display_surface.blit(passed_text, passed_textRect)

            elif state == State.FAILED:
                # Attempt to retry conneciton if during Capacitive Overlay Test
                screen.fill(red)
                display_surface.blit(failed_text, failed_textRect)

        else:
                screen.fill(red)
                display_surface.blit(failed_text, failed_textRect)

        # Update Frame
        pygame.display.update()

        # 30 frames a second
        clock.tick(30)