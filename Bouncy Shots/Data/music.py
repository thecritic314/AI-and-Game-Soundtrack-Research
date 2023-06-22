import pygame, sys
from pygame.locals import *

pygame.mixer.init()

startX = 1200
startY = 800

WIN = pygame.display.set_mode((int(startX), int(startY)))
pygame.display.set_caption("Music")

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

pygame.mixer.music.load('data/music/Intense.mp3')
pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/music/Intense.mp3'), loops=-1)
pygame.mixer.Channel(0).set_volume(0.5)
pygame.mixer.music.load('data/music/Calm.mp3')
pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/music/Calm.mp3'), loops=-1)
pygame.mixer.Channel(1).set_volume(0.5)

pygame.mixer.music.load('data/music/Win.mp3')
pygame.mixer.Channel(2).play(pygame.mixer.Sound('data/music/Win.mp3'), loops=-1)
pygame.mixer.Channel(2).set_volume(0.5)

pygame.mixer.music.load('data/music/WinIntense.mp3')
pygame.mixer.Channel(3).play(pygame.mixer.Sound('data/music/WinIntense.mp3'), loops=-1)
pygame.mixer.Channel(3).set_volume(0.0)

intensity = 0.5
winning = 0.5

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
                intensity = (1 - event.value) / 2
            if event.axis == 3:
                winning = (1 - event.value) / 2

    pygame.mixer.Channel(0).set_volume(intensity)
    pygame.mixer.Channel(1).set_volume(1 - intensity)

    pygame.mixer.Channel(2).set_volume(winning)

    if intensity > 0.5 and winning > 0.5:
        pygame.mixer.Channel(3).set_volume((winning-0.5) + (intensity-0.5))

