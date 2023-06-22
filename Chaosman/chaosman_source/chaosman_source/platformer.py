import random

import pygame
import pytmx, os

import camera
import gameobjects
import scene
import utilities



IMGDIR = os.path.join("data","images")
SOUNDDIR = os.path.join("data","sounds")
MUSICDIR = os.path.join("data","music")
LEVELDIR = os.path.join("data","levels")

class Platformer(scene.Scene):
    def __init__(self,game):
        scene.Scene.__init__(self,game)

        self.levels = [pytmx.load_pygame(os.path.join(LEVELDIR,"level1.tmx")),
                       pytmx.load_pygame(os.path.join(LEVELDIR,"level2.tmx")),
                       pytmx.load_pygame(os.path.join(LEVELDIR,"level3.tmx"))]
        self.currentlvl = 0
        self.lvl = self.levels[0]
        self.colgroup = pygame.sprite.Group()
        self.particals = []
        self.lives = 3
        self.score = 0

        self.goal_x = 0
        self.goal_y = 0
        self.start_x = 0
        self.start_y = 0

        self.player = gameobjects.Player(self)
        self.colgroup.add(self.player)
        self.bullets = pygame.sprite.Group()
        self.baddies = pygame.sprite.Group()
        self.camspeed = 1
        self.camera = camera.Camera(self.player,self.screen.get_size(),(1000,10000000),self.camspeed)
        self.levelparse()
        #self.flmask = utilities.loadImage(IMGDIR,"flashlight.png",1)
        #self.flmaskrect = self.flmask.get_rect()
        self.charge = 0
        self.hud = Hud(self)
        #pygame.mixer.music.load(os.path.join(MUSICDIR,"happychaos.wav"))

        pygame.mixer.music.load(os.path.join(MUSICDIR,"Intense.mp3"))
        pygame.mixer.music.load(os.path.join(MUSICDIR,"Calm.mp3"))
        pygame.mixer.music.load(os.path.join(MUSICDIR,"Win.mp3"))
        pygame.mixer.music.load(os.path.join(MUSICDIR,"WinIntense.mp3"))


        self.jumpsound = utilities.loadSound(SOUNDDIR,"jump.wav")
        self.jumpsound.set_volume(.3)
        self.shootsound = utilities.loadSound(SOUNDDIR,"gun.wav")
        self.shootsound.set_volume(.9)
        self.playerhitsound = utilities.loadSound(SOUNDDIR,"playerhit.wav")
        self.playerdeathsound = utilities.loadSound(SOUNDDIR,"playerdeath.wav")
        self.enemydeathsound = utilities.loadSound(SOUNDDIR,"enemydeath.wav")
        self.dischargesound = utilities.loadSound(SOUNDDIR,"Silent.wav")
        self.dischargesound.set_volume(.2)
        self.coinsound = utilities.loadSound(SOUNDDIR,"coin.wav")



    def onenter(self):
        #pygame.mixer.music.play(-1)
        pygame.mixer.Channel(0).play(pygame.mixer.Sound('data/music/Intense.mp3'), loops=-1)
        pygame.mixer.Channel(0).set_volume(0.5)
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('data/music/Calm.mp3'), loops=-1)
        pygame.mixer.Channel(1).set_volume(0.5)
        pygame.mixer.Channel(2).play(pygame.mixer.Sound('data/music/Win.mp3'), loops=-1)
        pygame.mixer.Channel(2).set_volume(0.5)
        pygame.mixer.Channel(3).play(pygame.mixer.Sound('data/music/WinIntense.mp3'), loops=-1)
        pygame.mixer.Channel(3).set_volume(0.0)



    def onexit(self):
        pygame.mixer.music.stop()
    def reload(self):
        self.lvl = self.levels[self.currentlvl]
        self.colgroup.empty()
        self.baddies.empty()
        self.bullets.empty()
        self.levelparse()
        self.colgroup.add(self.player)
        self.charge = 0

    def levelparse(self):
        self.camera.levelsize = (self.lvl.width * 8, self.lvl.height * 8)
        for layer in [self.lvl.get_layer_by_name("tiles")]:
            print(layer)
            for i in layer:
                try:
                    img = self.lvl.get_tile_image_by_gid(i[2])
                    self.colgroup.add(gameobjects.Block(img, (i[0] * 8, i[1] * 8), self))
                except:
                    pass
        for a in [self.lvl.get_layer_by_name("objects")]:
            for i in a:
                print(i)
                if i.name == "spike":
                    self.colgroup.add(gameobjects.Spike((i.x,i.y),self))
                if i.name == "bridge":
                    self.colgroup.add(gameobjects.Bridge((i.x,i.y),self))
                if i.name == "playerspawn":
                    self.player.rect.topleft = (i.x,i.y)
                    self.start_x = i.x
                    self.start_y = i.y
                if i.name == "delk":
                    self.colgroup.add(gameobjects.Delk((i.x,i.y),self))
                if i.name == "decharger":
                    self.colgroup.add(gameobjects.Decharger((i.x,i.y),self))
                if i.name == "ghost":
                    self.colgroup.add(gameobjects.Ghost((i.x,i.y),self))
                if i.name == "door":
                    self.colgroup.add(gameobjects.Door((i.x,i.y),self))
                    self.goal_x = i.x
                    self.goal_y = i.y
                if i.name == "coin":
                    self.colgroup.add(gameobjects.Coins((i.x,i.y),self))



    def update(self):
        self.player.update()
        self.charge = round(self.charge +  .05,3)
        self.baddies.update()
        #self.flmaskrect.center = self.player.rect.center
        self.bullets.update()
        self.camera.speed = self.camspeed * abs(self.player.xaccel) * self.game.dt
        self.camera.update()
        self.hud.update()
        if self.charge < 0:
            self.charge = 0
        if self.charge > 100:
            self.charge = 0
            self.player.die()

        for i in self.particals:
            i.update()
    def render(self):
        randdo = pygame.Surface((200,160))
        randdo.fill((random.randint(255,255),(random.randint(255,255)),(random.randint(255,255))))
        self.screen.fill((0,0,0))
        for i in self.colgroup.sprites():
            i.render(self.camera)
        #self.screen.blit(self.flmask,utilities.add_pos(self.flmaskrect.topleft,self.camera.offset))
        for i in self.particals:
            i.render(self.screen,self.camera)
        self.hud.render(self.screen)
        self.screen.blit(randdo,(0,0),special_flags=pygame.BLEND_MULT)
class Hud():
    def __init__(self,game):
        self.game = game
        self.bg = utilities.loadImage(IMGDIR,"hudbg.png",1)
        self.hudtext = pygame.font.SysFont("arial",12)
        self.metername = self.hudtext.render("Chaos Meter",False,(128,128,128))
        self.livetext = self.hudtext.render("lives: " + str(self.game.lives),False,(128,128,128))
        self.scoretext = self.hudtext.render("score: " + str(self.game.score), False, (128, 128, 128))
    def update(self):
        self.livetext = self.hudtext.render("Lives: " + str(self.game.lives),False,(128,128,128))
        self.scoretext = self.hudtext.render("Score: " + str(self.game.score), False, (128, 128, 128))
    def render(self,screen):
        screen.blit(self.bg,(0,0))
        pygame.draw.line(screen,(128,128,128),(10,15),(int(self.game.charge) + 11,15),8)
        pygame.draw.rect(screen,(128,128,128),pygame.Rect(9,12,105,10),1,2)
        screen.blit(self.metername,(15,20))
        screen.blit(self.livetext,(135,10))
        screen.blit(self.scoretext, (135, 20))



