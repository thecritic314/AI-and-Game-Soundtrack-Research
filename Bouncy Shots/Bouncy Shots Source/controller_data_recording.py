import pygame, sys
from pygame.locals import *
import time
import csv

def start_collecting_data():
    mainClock = pygame.time.Clock()

    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

    width = 600
    height = 600

    screen = pygame.display.set_mode((int(width), int(height)))
    pygame.display.set_caption("DATA")

    pygame.font.init()
    font = pygame.font.SysFont(pygame.font.get_default_font(), 32)

    bar_1 = pygame.image.load("data/bars/Level Bar/bar3.png")
    bar_2 = pygame.image.load("data/bars/Level Bar/bar4.png")
    bar_3 = pygame.image.load("data/bars/Level Bar/bar5.png")

    bar_neg1 = pygame.transform.rotate(pygame.image.load("data/bars/Level Bar/bar3.png"), 180)
    bar_neg2 = pygame.transform.rotate(pygame.image.load("data/bars/Level Bar/bar4.png"), 180)
    bar_neg3 = pygame.transform.rotate(pygame.image.load("data/bars/Level Bar/bar5.png"), 180)

    intensity = 0.5
    winning_status = 0.5

    start = round(1000 * time.time())
    past_timestamp = start

    with open("chaos_user_input.csv", "w", newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        writer.writerow(["Timestamp(ms)", "Intensity", "Winning Status"])

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == JOYAXISMOTION:
                if event.axis == 1:
                    intensity = (1-event.value)/2
                if event.axis == 3:
                    winning_status = (1-event.value)/2

        screen.fill((200, 200, 200))
        intensity_value = font.render("Intensity: " + str("{:.3f}".format(intensity)), True, (0, 0, 0))
        screen.blit(intensity_value, (0, 0))

        winning_value = font.render("Winning Status: " + str("{:.3f}".format(winning_status)), True, (0, 0, 0))
        screen.blit(winning_value, (300, 0))

        intensity_location = (0, 100)
        if intensity >= 0 and intensity < 0.17:
            screen.blit(bar_neg3, intensity_location)
        if intensity >= 0.17 and intensity < 0.33:
            screen.blit(bar_neg2, intensity_location)
        if intensity >= 0.33 and intensity < 0.50:
            screen.blit(bar_neg1, intensity_location)
        if intensity >= 0.50 and intensity < 0.66:
            screen.blit(bar_1, intensity_location)
        if intensity >= 0.66 and intensity < 0.84:
            screen.blit(bar_2, intensity_location)
        if intensity >= 0.84 and intensity <= 1.1:
            screen.blit(bar_3, intensity_location)

        winning_status_location = (200, 100)
        if winning_status >= 0 and winning_status < 0.17:
            screen.blit(bar_neg3, winning_status_location)
        if winning_status >= 0.17 and winning_status < 0.33:
            screen.blit(bar_neg2, winning_status_location)
        if winning_status >= 0.33 and winning_status < 0.50:
            screen.blit(bar_neg1, winning_status_location)
        if winning_status >= 0.5 and winning_status < 0.66:
            screen.blit(bar_1, winning_status_location)
        if winning_status >= 0.66 and winning_status < 0.84:
            screen.blit(bar_2, winning_status_location)
        if winning_status >= 0.84 and winning_status <= 1.1:
            screen.blit(bar_3, winning_status_location)

        pygame.display.update()

        timestamp = round(1000 * time.time())
        if timestamp - past_timestamp >= 100:
            with open("chaos_user_input.csv", "a", newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter='\t')
                writer.writerow([timestamp - 930, intensity, winning_status])
                # avg speed
            past_timestamp = timestamp
            # print(timestamp)
        mainClock.tick(60)

start_collecting_data()