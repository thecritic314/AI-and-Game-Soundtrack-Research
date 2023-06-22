import pygame, os, utilities

import deathscreen
import gameover
import platformer
import startscreen
import victory

import time
import csv
import math
import queue
from data_man import model1 as regint, model2 as regwin, normal_input_scaled

with open("chaos.csv", "w", newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(["Timestamp", "Score", "Lives", "Chaos", "Level", "Enemies", "Bullets", "AvgBtnFreq", "GoalDist",
                     "StartDist", "TimeElapsed", "AtTower"])
start = round(1000 * time.time())
past_timestamp = start
button_press_queue = queue.Queue()
past_chaos = 0
past_enemy_dist = 400.0
normal_mins = normal_input_scaled.data_min_
normal_maxs = normal_input_scaled.data_max_

p_int = 0
p_win = 0

SCREENWIDTH = 800
SCREENHEIGHT = 640
TEMPSCREENWIDTH = 200  # 200
TEMPSCREENHEIGHT = 160  # 160
IMGDIR = os.path.join("data", "images")
SOUNDDIR = os.path.join("data", "sounds")
MUSICDIR = os.path.join("data", "music")
LEVELDIR = os.path.join("data", "levels")

button_presses = 0


class Game():
    def __init__(self):

        # pygame setup
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), pygame.RESIZABLE | pygame.SCALED)
        pygame.display.set_caption("ChaosMan Overloaded", "ChaosNan Overloaded")
        pygame.display.set_icon(utilities.loadImage(IMGDIR, "icon.png"))
        self.temp_screen = pygame.Surface((TEMPSCREENWIDTH, TEMPSCREENHEIGHT))

        self.clock = pygame.time.Clock()

        self.dt = 0
        self.actions = {"a": False, "b": False, "up": False, "down": False, "left": False, "right": False,
                        "start": False, "select": False}
        self.action_mapping = {"a": pygame.K_a, "b": pygame.K_s, "up": pygame.K_UP, "down": pygame.K_DOWN,
                               "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "start": pygame.K_RETURN,
                               "select": pygame.K_BACKSPACE}
        self.actions_cooldowns = {"a": 0, "b": 0, "up": 0, "down": 0, "left": 0, "right": 0,
                                  "start": 0, "select": 0}

        self.images = utilities.loadSpriteSheet(utilities.loadImage(IMGDIR, "imgsheet.png", 1), (8, 8))

        # game set up
        self.platformer = platformer.Platformer(self)
        self.startscreen = startscreen.Startsceen(self)
        self.deathscreen = deathscreen.Deathscreen(self)
        self.gameoverscreen = gameover.Gameoverscreen(self)
        self.victoryoverscreen = victory.Victoryscreen(self)

        self.curr_scene = self.startscreen
        self.prev_scene = None
        self.running = True

        global button_presses
        button_presses = 0

    def update_actions(self):
        # gets keys pressed from pygame
        keys = pygame.key.get_pressed()

        # resets all keys to false
        for k in self.actions:
            self.actions[k] = False
        # sets any key to true if its pressed
        for k in self.action_mapping.values():
            if keys[k]:
                global button_presses
                button_presses += 1
                self.actions[utilities.get_key(self.action_mapping, k)] = True
        for k in self.actions_cooldowns:
            if self.actions_cooldowns[k] > 0:
                self.actions_cooldowns[k] -= 1
        if keys[pygame.K_ESCAPE]:
            self.running = False
            pygame.quit()

    def update(self):
        global past_timestamp, past_chaos, past_enemy_dist, p_int, p_win
        
        pygame.mixer.Channel(0).set_volume(p_int)
        pygame.mixer.Channel(1).set_volume(1 - p_int)

        pygame.mixer.Channel(2).set_volume(p_win)

        if p_int > 0.5 and p_win > 0.5:
            pygame.mixer.Channel(3).set_volume((p_win - 0.5) + (p_int - 0.5))

        timestamp = round(1000 * time.time())
        # DATA COLLECTION-----------------------------------------------------------------------------------------------
        if timestamp - past_timestamp >= 100:
            scoreVal = self.platformer.score
            livesVal = self.platformer.lives
            chaosVal = self.platformer.charge
            levelNum = self.platformer.currentlvl
            enemyNum = 0
            bulletNum = len(self.platformer.bullets)

            self_x = self.platformer.player.rect.left
            self_y = self.platformer.player.rect.top
            you = [self_x, self_y]
            goal = [self.platformer.goal_x, self.platformer.goal_y]
            spawn = [self.platformer.start_x, self.platformer.start_y]
            goalDist = math.dist(you, goal)
            spawnDist = math.dist(you, spawn)

            min_enemy_dist = 10000
            for enemy in self.platformer.baddies:
                e_x = enemy.rect.left
                e_y = enemy.rect.top
                enemy_coords = [e_x, e_y]
                enemy_dist = math.dist(you, enemy_coords)
                if enemy_dist < min_enemy_dist:
                    min_enemy_dist = enemy_dist

                if enemy_dist <= 80:
                    enemyNum += 1

            import gameobjects
            if past_enemy_dist == min_enemy_dist:
                gameobjects.first_timestamp = timestamp
            timeElapsed = timestamp - gameobjects.first_timestamp

            if chaosVal - past_chaos <= 0:
                tower = 1
            else:
                tower = 0

            global button_presses
            if button_press_queue.qsize() >= 10:
                button_press_queue.get()
            button_press_queue.put(button_presses)
            button_presses = 0
            avg_button_freq = 0
            for i in tuple(button_press_queue.queue):
                avg_button_freq += i
            avg_button_freq /= button_press_queue.qsize()

            with open("chaos.csv", "a", newline='') as csvfile2:
                writer2 = csv.writer(csvfile2, delimiter=',')
                curr_inputs = [scoreVal, livesVal, chaosVal, levelNum, enemyNum, bulletNum, avg_button_freq, goalDist,
                               spawnDist, timeElapsed, tower]
                if past_enemy_dist != min_enemy_dist:
                    writer2.writerow([timestamp] + curr_inputs)

            for i in range(len(curr_inputs)):
                curr_inputs[i] = (float(curr_inputs[i]) - normal_mins[i]) / (normal_maxs[i] - normal_mins[i])

            pred_int = regint.predict([curr_inputs])[0]
            pred_win = regwin.predict([curr_inputs])[0]
            past_timestamp = timestamp
            past_chaos = chaosVal
            past_enemy_dist = min_enemy_dist

            print(pred_int, pred_win)
            p_int = pred_int
            p_win = pred_win

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
        self.update_actions()
        self.curr_scene.update()
        self.dt = self.clock.tick(60) * .001 * 60

    def render(self):
        self.curr_scene.render()

    def gameloop(self):
        loops = 0
        while self.running:
            self.update()
            self.render()
            self.screen.blit(pygame.transform.scale(self.temp_screen, (800, 640)), (0, 0))
            pygame.display.flip()
            loops += 1
