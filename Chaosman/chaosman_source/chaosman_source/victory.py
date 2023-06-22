import pygame

import scene

class Victoryscreen(scene.Scene):
    def __init__(self,game):
        scene.Scene.__init__(self,game)
        self.titlefont = pygame.font.SysFont('arial', 20)
        self.title = self.titlefont.render("you Win",False,(128,128,128))
        self.titlerect = self.title.get_rect(center = (self.screen.get_width()/ 2,self.screen.get_height() / 2))

        self.startfont = pygame.font.SysFont("arial", 12)
        self.start = self.startfont.render("press start",False,(128,128,128))
        self.startrect = self.start.get_rect(center = self.titlerect.center)
        self.startrect.top = self.titlerect.bottom
    def update(self):
        if self.game.actions["start"] and self.game.actions_cooldowns["start"] < 20:
            self.game.platformer.colgroup.add(self.game.platformer.player)
            self.game.platformer.player.living = True
            self.game.platformer.currentlvl = 0
            self.game.platformer.reload()
            self.game.platformer.lives = 3
            self.game.platformer.score = 0
            self.game.startscreen.enter()
            self.exit()
            self.game.actions_cooldowns["start"] = 20

    def render(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.title,self.titlerect)
        self.screen.blit(self.start,self.startrect)