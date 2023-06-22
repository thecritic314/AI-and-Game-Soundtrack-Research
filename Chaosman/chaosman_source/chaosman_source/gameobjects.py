import random
import time

import pygame

import utilities

first_timestamp = round(1000 * time.time())

class GameObject(pygame.sprite.Sprite):
    def __init__(self,image,pos,game):
        pygame.sprite.Sprite.__init__(self)
        if image == 0:
            self.image = pygame.Surface((8,8))
            self.image.fill((20,30,40))
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.game = game
        self.collision_group = self.game.colgroup
    def raninto(self,block,direction = 0):
        pass
    def onhit(self,object,direction = 0):
        object.raninto(self)
    def update(self):
        pass
    def render(self, camera):
        camera.draw_sprite(self.game.screen , self)

class Block(GameObject):
    def __init__(self,image,pos,game):
        GameObject.__init__(self,image,pos,game)
    def onhit(self,object,direction = 0):
        if True:
            if direction == 0:
                object.rect.right = self.rect.left
            if direction == 1:
                object.rect.left = self.rect.right
            if direction == 2:
                object.rect.bottom = self.rect.top
            if direction == 3:
                object.rect.top = self.rect.bottom
            object.raninto(self,direction)
class Player(GameObject):
    def __init__(self,game):
        GameObject.__init__(self,0,(50,50),game)
        self.speed = 1
        self.xaccel = 0
        self.yaccel = 0
        self.maxaccel = 1.5
        self.state = "idle"
        self.jumptimer = 0
        self.grounded = True
        self.faceing = "right"
        self.shoot = False
        self.invincible = 30

        self.frame = 0
        self.images = self.game.game.images[4]
        self.idlerightanim = [self.images[0],self.images[4]]
        self.runrightanim = [self.images[0], self.images[1], self.images[2]]
        self.jumprightimg = self.images[3]

        self.idleleftanim = utilities.flipimages(self.idlerightanim)
        self.runleftanim = utilities.flipimages(self.runrightanim)
        self.jumpleftimg = pygame.transform.flip(self.jumprightimg,True,False)

        self.living = True
    def movesingle(self,x,y):
        self.rect.move_ip(x, y)
        hit = pygame.sprite.spritecollide(self, self.collision_group, False)
        for block in hit:
            if x > 0:
                block.onhit(self, 0)
            if x < 0:
                block.onhit(self, 1)
            if y > 0:
                block.onhit(self, 2)
                if isinstance(block, Block):
                    self.grounded = True
            if y < 0:
                block.onhit(self, 3)
    def raninto(self,block,direction = 0):
        if isinstance(block,Baddies):
            self.baddiehit()
    def baddiehit(self):
        if self.invincible < 0:
            self.game.playerhitsound.play()
            self.invincible = 30
            self.game.charge += 10
            self.xaccel = 0
            self.yaccel = 0
            if self.faceing == "left":
                self.movesingle(1,-5)
            else:
                self.movesingle(-1,-5)
    def die(self):
        Playerexplode(self.rect.center,self.game)
        self.game.playerdeathsound.play()
        self.kill()
        self.living = False
        self.game.lives -= 1
    def update(self):
        if self.living:
            self.state = "idle"
            if self.game.game.actions["b"]:
                if self.shoot == False:
                    self.game.shootsound.play()
                    self.collision_group.add(Bullet(self.rect.center,self.game,self.faceing,100))
                    self.game.charge += 2
                    self.shoot = True
            else:
                self.shoot = False
            if self.game.game.actions["right"]:
                self.xaccel += .5
                self.state = "running"
                self.faceing = "right"
            if self.game.game.actions["left"]:
                self.xaccel -= .5
                self.state = "running"
                self.faceing = "left"
            if self.game.game.actions["a"] and self.grounded == True:
                self.game.jumpsound.play()
                self.yaccel = 0
                self.jumptimer = 14
            if not self.game.game.actions["a"]:
                self.jumptimer = 0

            self.grounded = False

            #drag
            if self.xaccel > 0:
                self.xaccel -= .2
                if self.xaccel < 0:
                    self.xaccel = 0
            if self.xaccel < 0:
                self.xaccel += .2
                if self.xaccel > 0:
                    self.xaccel = 0


            #accel limit
            if self.xaccel > self.maxaccel:
                self.xaccel = self.maxaccel
            if self.xaccel < -self.maxaccel:
                self.xaccel = -self.maxaccel
            if self.yaccel > self.maxaccel:
                self.yaccel = self.maxaccel
            if self.yaccel < -self.maxaccel:
                self.yaccel = -self.maxaccel
            self.yaccel +=.5
            if self.grounded:
                self.yaccel = 0
            if self.jumptimer > 0:
                self.state = "jumping"
                self.jumptimer -= 1
                self.yaccel = -2

            xmov = self.xaccel * self.speed * self.game.game.dt
            ymov = self.yaccel * self.speed * self.game.game.dt
            self.movesingle(round(xmov),0)
            self.movesingle(round(0),ymov)

            self.frame += 1
            self.invincible -= 1

            if self.faceing == "right":
                if self.state == "idle":
                    self.image = self.idlerightanim[int(self.frame / 30 % 2)]
                if self.state == "running":
                    self.image = self.runrightanim[int(self.frame / 10 % 3)]
                if self.state == "jumping":
                    self.image = self.jumprightimg
            if self.faceing == "left":
                if self.state == "idle":
                    self.image = self.idleleftanim[int(self.frame / 20 % 2)]
                if self.state == "running":
                    self.image = self.runleftanim[int(self.frame / 10 % 3)]
                if self.state == "jumping":
                    self.image = self.jumpleftimg
class Bullet(GameObject):
    def __init__(self,pos, game, direction, duration):
        GameObject.__init__(self,pygame.Surface((2,2)),pos,game)
        self.image.fill((128,128,128))
        self.direction = direction
        self.duration = duration
        self.game.bullets.add(self)
    def movesingle(self,x,y):
        self.rect.move_ip(x, y)
        hit = pygame.sprite.spritecollide(self, self.collision_group, False)
        for block in hit:
            if x > 0:
                block.onhit(self, 0)
            if x < 0:
                block.onhit(self, 1)
            if y > 0:
                block.onhit(self, 2)
            if y < 0:
                block.onhit(self, 3)
    def raninto(self,block,direction = 0):
        if isinstance(block,Block):
            self.kill()
        if isinstance(block,Baddies):
            block.hp -= 1
            self.kill()

    def update(self):
        if self.duration > 0:
            if self.direction == "right":
                self.movesingle(3 * self.game.game.dt,0)
            if self.direction == "left":
                self.movesingle(-3 * self.game.game.dt,0)
            self.duration -= 1
        else:
            self.kill()
class Spike(GameObject):
    def __init__(self,pos,game):
        GameObject.__init__(self,pygame.Surface((8,8)),pos,game)
        self.image = self.game.game.images[1][5]
    def onhit(self,object,direction = 0):
        if isinstance(object,Player):
            object.die()
class Bridge(GameObject):
    def __init__(self,pos,game):
        GameObject.__init__(self,pygame.Surface((8,8)),pos,game)
        self.image = self.game.game.images[3][5]
    def onhit(self,object,direction = 0):
        if isinstance(object,Player):
            if direction == 2 and not self.game.game.actions["down"]:
               if object.rect.bottom < self.rect.top + 3:
                    object.rect.bottom = self.rect.top
                    object.grounded = True
        else:
             if direction == 2:
                 if object.rect.bottom < self.rect.top + 3:
                     object.rect.bottom = self.rect.top

class Baddies(GameObject):
    def __init__(self, image, pos, game):
        GameObject.__init__(self, image, pos, game)
        self.hp = 0

class Delk(Baddies):
    def __init__(self,pos, game):
        Baddies.__init__(self,pygame.Surface((8,8)),pos,game)
        self.images = self.game.game.images[6][0:3]
        self.direction = True
        self.speed = 1
        self.game.baddies.add(self)
        self.frame = 0
        self.hp = 2
    def die(self):
        Explode(self.rect.center,self.game)
        self.kill()
        self.game.score += 10

    def movesingle(self, x, y):
        self.rect.move_ip(x, y)
        hit = pygame.sprite.spritecollide(self, self.collision_group, False)
        for block in hit:
            if x > 0:
                block.onhit(self, 0)
                if isinstance(block, Block):
                    self.direction = not self.direction
            if x < 0:
                block.onhit(self, 1)
                if isinstance(block, Block):
                    self.direction = not self.direction
            if y > 0:
                block.onhit(self, 2)
            if y < 0:
                block.onhit(self, 3)
    def update(self):
        self.frame += 1
        self.movesingle(0,1)
        if self.direction:
            self.movesingle(round(self.speed * self.game.game.dt), 0)
        if not self.direction:
            self.movesingle(round(-self.speed * self.game.game.dt), 0)
        self.image = self.images[int(self.frame / 10 % 3)]

        if self.hp <= 0:
            self.die()
class Ghost(Baddies):
    def __init__(self,pos, game):
        Baddies.__init__(self,pygame.Surface((8,8)),pos,game)
        self.images = self.game.game.images[6][3:5]
        self.direction = True
        self.speed = 1
        self.game.baddies.add(self)
        self.frame = 0
        self.hp = 3
        self.distance = 0
    def die(self):
        Explode(self.rect.center,self.game)
        self.kill()
        self.game.score += 20

    def movesingle(self, x, y):
        self.rect.move_ip(x, y)
        hit = pygame.sprite.spritecollide(self, self.collision_group, False)
        for block in hit:
            if x > 0:
                block.onhit(self, 0)
                if isinstance(block, Block):
                    self.direction = not self.direction
            if x < 0:
                block.onhit(self, 1)
                if isinstance(block, Block):
                    self.direction = not self.direction
            if y > 0:
                block.onhit(self, 2)
            if y < 0:
                block.onhit(self, 3)


    def update(self):
        self.frame += 1
        if self.frame % 3 == 0:
            if self.direction:
                self.movesingle(round(self.speed * self.game.game.dt), 0)
            if not self.direction:
                self.movesingle(round(-self.speed * self.game.game.dt), 0)
        self.image = self.images[int(self.frame / 20 % 2)]

        if self.hp <= 0:
            self.die()
        self.distance += 1
        if self.distance > 100:
            self.distance = 0
            self.direction = not self.direction

class Decharger(GameObject):
    def __init__(self,pos,game):
        GameObject.__init__(self,pygame.Surface((8,8)),pos,game)
        self.image = self.game.game.images[2][5]
        self.soundtimer = 10
    def onhit(self,object,direction = 0):
        if isinstance(object,Player):
            self.game.charge -= .2
            self.soundtimer -= 1
            if self.soundtimer < 0:
                self.game.dischargesound.play()
                self.soundtimer = 10
class Explode():
    def __init__(self, pos, game):
        self.game = game
        self.particals = []
        self.game.enemydeathsound.play()
        self.pos = pos
        self.timer = 0
        self.emittimer = 5
        self.game.particals.append(self)
    def update(self):
        self.timer += 1
        self.emittimer -= 1
        if self.emittimer <= 0 :
            self.particals.append([(utilities.add_pos(self.pos,(random.randint(-5,5),random.randint(-5,5)))),random.choice((True,False))])
            self.emittimer = random.randint(5,25)
        if self.timer == 100:
            self.game.particals.remove(self)
        for i in self.particals:
            if i[1]:
                i[0]=utilities.add_pos(i[0],(.1,.1))
            else:
                i[0] = utilities.add_pos(i[0], (-.1, .1))
    def render(self,screen,camera):
        for i in self.particals:
            pygame.draw.circle(screen,(128,128,128),utilities.add_pos(i[0],camera.offset),3,1)
class Playerexplode(Explode):
    def __init__(self,pos, game):
        Explode.__init__(self,pos,game)
    def update(self):
        Explode.update(self)
        if self.timer == 100:
            if self.game.lives > 0:
                self.game.game.deathscreen.enter()
            else:
                self.game.game.gameoverscreen.enter()
            self.game.exit()
class Door(GameObject):
    def __init__(self,pos,game):
        GameObject.__init__(self,pygame.Surface((8,8)),pos,game)
        self.image = self.game.game.images[0][6]

    def onhit(self,object,direction = 0):
        if isinstance(object,Player):
            global first_timestamp
            first_timestamp = round(1000 * time.time())
            self.game.currentlvl += 1
            if self.game.currentlvl == len(self.game.levels):
                self.game.exit()
                self.game.game.victoryoverscreen.enter()
            else:
                self.game.reload()
class Coins(GameObject):
    def __init__(self,pos,game):
        GameObject.__init__(self,pygame.Surface((8,8)),pos,game)
        self.image = self.game.game.images[0][5]
    def onhit(self,object,direction = 0):
        if isinstance(object,Player):
            self.game.score += 1
            self.kill()
            self.game.coinsound.play()






