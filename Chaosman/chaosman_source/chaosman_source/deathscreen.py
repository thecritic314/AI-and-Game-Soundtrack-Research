import pygame

import scene

class Deathscreen(scene.Scene):
    def __init__(self,game):
        scene.Scene.__init__(self,game)
        self.titlefont = pygame.font.SysFont('arial', 20)
        self.title = self.titlefont.render("You Died",False,(128,128,128))
        self.titlerect = self.title.get_rect(center = (self.screen.get_width()/ 2,self.screen.get_height() / 2))

        self.startfont = pygame.font.SysFont("arial", 12)
        self.start = self.startfont.render("press start",False,(128,128,128))
        self.startrect = self.start.get_rect(center = self.titlerect.center)
        self.startrect.top = self.titlerect.bottom
    def update(self):
        if self.game.actions["start"]:
            self.game.platformer.enter()
            self.game.platformer.colgroup.add(self.game.platformer.player)
            self.game.platformer.player.living = True
            self.game.platformer.reload()
            self.exit()

    def render(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.title,self.titlerect)
        self.screen.blit(self.start,self.startrect)