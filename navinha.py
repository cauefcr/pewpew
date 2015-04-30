import pygame, sys
from random import randint
from pygame.locals import *
from math import sin,cos

pygame.init()

from score import *

# set up the display
FPS = 60
fpsClock = pygame.time.Clock()
graphwidth = 640
graphheight = 480
DISPLAYSURF = pygame.display.set_mode((graphwidth, graphheight))
DISPLAYSURF2 = pygame.display.set_mode((graphwidth, graphheight))
pygame.mouse.set_visible(0)
pygame.display.set_caption("PEW PEW!")

#set up sound
pygame.mixer.pre_init(44100,-16,2, 4096)
pygame.mixer.init()
endgame_snd = pygame.mixer.Sound('farewell.ogg')
shot_snd = pygame.mixer.Sound('shot.ogg')
take_dmg_snd = pygame.mixer.Sound('snare.ogg')
boss_is_dead_snd = pygame.mixer.Sound('boss_dies.ogg')
ost_snd = pygame.mixer.Sound('timbre_-6db.ogg')
give_dmg_snd = pygame.mixer.Sound('jump.ogg')
player_died_snd = pygame.mixer.Sound('ghost.ogg')
game_start_snd = pygame.mixer.Sound('fallingufo.ogg')
exploding_snd = pygame.mixer.Sound('explosion.ogg')

#set up the colors
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = ( 0, 255, 0)
BLUE = ( 0, 0, 255)

#set up sprites
bg = pygame.image.load('BG.jpg')
playerImg = pygame.image.load('nave.png')
playershotImg = pygame.image.load('shotp.png')
bossImg = pygame.image.load('bigboss.png')
radial_shot = pygame.image.load('boss_shot.png')
straightshot = pygame.image.load('shote.png')
mob1Img = pygame.image.load('mob1.png')
curvedshotImg = pygame.image.load('circleshote.png')
mob2Img = pygame.image.load('mob2.png')
mob3Img = pygame.image.load('mob3.png')
whipImg = pygame.image.load('whip.png')

#explosions
ex1 = pygame.image.load('explosion1.png')
ex2 = pygame.image.load('explosion2.png')
ex3 = pygame.image.load('explosion3.png')
ex4 = pygame.image.load('explosion4.png')
ex5 = pygame.image.load('explosion5.png')
ex6 = pygame.image.load('explosion6.png')
ex7 = pygame.image.load('explosion7.png')
ex8 = pygame.image.load('explosion8.png')
ex9 = pygame.image.load('explosion9.png')
ex10 = pygame.image.load('explosion10.png')
ex11 = pygame.image.load('explosion11.png')
ex12 = pygame.image.load('explosion12.png')
ex13 = pygame.image.load('explosion13.png')
ex14 = pygame.image.load('explosion14.png')

#set up classes
class shot(pygame.sprite.Sprite): #creates shot as a class, which ships will use with their methods
    def __init__(self,x,y,spd,dmg,type,sprite,team):
        pygame.sprite.Sprite.__init__(self)
        self.spd = spd
        self.dmg = dmg
        self.type = type
        self.image = sprite
        self.team = team
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.cont = 0
        if self.team == 'red':
            enemy_shots.add(self)
        else:
            player_shots.add(self)
        shot_snd.play()
    def move(self): #defines how the shots will move, so ships can call them at will
        if self.type == 'simple':
            self.rect.y += self.spd
        elif self.type == 'curved':
            self.rect.y += self.spd
            self.rect.x += self.spd*2*sin(self.cont) - self.spd*2*cos(self.cont)
            self.cont += 0.2
        elif self.type == 'whip':
            self.rect.y += self.spd*sin(self.cont) + self.spd*cos(self.cont) + 1.5
            self.rect.x += self.spd*sin(self.cont) - self.spd*cos(self.cont)
            self.cont += 0.1
        elif self.type == 'boss':
            self.rect.y += self.spd
            if self.rect.y > 320:
                pi = 3.14159265359
                cont = 0
                for i in range(1,9):
                    spd = self.spd * cos(cont)
                    spdy = self.spd * sin(cont)
                    instance = shot(self.rect.x,self.rect.y,spd,2/dif,'radial',radial_shot,'red')
                    instance.spdy = spdy
                    cont += pi/4
                self.kill()
        elif self.type == 'radial':
            self.rect.y += self.spdy
            self.rect.x += self.spd
    
class ship(pygame.sprite.Sprite): #sets up the class ship, which is the main class that has movement.
    cont = 0 #controls direction
    state = 'hunting'
    def __init__(self,x,y,hp,spd,shotspd,shotdmg,shottype,delay,sprite,spriteshot,team):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        self.spd = 0
        self.maxspd = spd
        self.accel = spd/5
        self.shotspd = shotspd
        self.shotdmg = shotdmg
        self.shottype = shottype
        self.delay = delay
        self.spriteshot = spriteshot
        self.maxdelay = delay
        self.team = team
        if self.team == 'red':
            enemy_list.add(self)
        else:
            player_list.add(self)

    def shoot(self): #creates an object using the class shot, using the definitions on how to call it that were given to it on start
        if self.team == 'red':
            instance = shot(self.rect.x+(0.8*self.rect.width/2),self.rect.y+(self.rect.height),self.shotspd,self.shotdmg,self.shottype,self.spriteshot,self.team)
        else:
            instance = shot(self.rect.x+(0.7*(self.rect.width/2)),self.rect.y-(self.rect.height/2),self.shotspd,self.shotdmg,self.shottype,self.spriteshot,self.team)
        
    def aimov(self): #uses states as the mean of choosing how the ships will move
        if self.state == "hunting":
            if player.rect.centerx > self.rect.centerx+self.maxspd+self.rect.width/4 \
               and self.spd <= self.maxspd:
                self.spd += self.accel
              #  self.rect.x += self.spd/4
            elif player.rect.centerx < self.rect.centerx-(self.maxspd+self.rect.width/4) \
               and self.spd > -self.maxspd:
                self.spd -= self.accel
              #  self.rect.x -= self.spd/4
            self.rect.x += self.spd
        if self.state == "fleeing":
            if player.rect.centerx > self.rect.centerx \
               and self.rect.x+self.rect.width < graphwidth \
               and self.rect.x > 0\
               and self.spd >= self.maxspd:
                self.spd += self.accel
            if player.rect.centerx < self.rect.centerx \
               and self.rect.x+self.rect.width < graphwidth \
               and self.rect.x > 0\
               and self.spd < self.maxspd:
                self.spd -= self.accel
            self.rect.x += self.spd
            if self.rect.centerx < 0 \
               or self.rect.centerx > graphwidth:
                self.state = "hunting"
            
    def aishoot(self): #the method which is used for calling the shots, and only if it's an member of the AI team
        if self.team == "red":
            self.delay -= 1
        if self.delay <= 0:
                self.shoot()
                self.delay = self.maxdelay
    def explode(self): #method called when the ship dies, which plays the sound and creates an object explosion, where the ship was
        exploding_snd.play()
        self.exploding = True
        instance = explos(self.rect.x-self.rect.width,self.rect.y-self.rect.height,ex1)
        self.kill()
        return

class boss(ship): #creates a special instance of the 
    def explode(self):
        boss_is_dead_snd.play()
        instance = explos(self.rect.x,self.rect.y,ex1)
        instance = explos(self.rect.x+self.rect.width/2,self.rect.y,ex1)
        instance = explos(self.rect.x+self.rect.width,self.rect.y,ex1)
        self.kill()
    def aimov(self):
        if self.rect.centery < self.rect.height+5:
            self.rect.centery += self.accel
        if player.rect.centerx > self.rect.centerx+self.maxspd+self.rect.width/4 and self.spd <= self.maxspd/2:
            self.spd += self.accel
            self.rect.x += self.spd/4
        elif player.rect.centerx < self.rect.centerx-(self.maxspd+self.rect.width/4) and self.spd > -self.maxspd/2:
           self.spd -= self.accel
           self.rect.x += self.spd/4
        self.rect.x += self.spd

class explos(pygame.sprite.Sprite):
    explode_frame = 0
    explodeimg = [ex2,ex3,ex4,ex5,ex6,ex7,ex8,ex9,ex10,ex11,ex12,ex13,ex14]
    def __init__(self,x,y,sprite):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        explosions.add(self)
    def cycle(self):
        if self.explode_frame == len(self.explodeimg):
            self.kill()
            return
        self.image = self.explodeimg[self.explode_frame]
        self.explode_frame += 1
        
#set up the variables
mousex = 0
mousey = 0
mouseClicked = False #Player variables
delay = 0
game_finish = 0
time_game_finished = 0

enemy_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
enemy_shots = pygame.sprite.Group()
player_shots = pygame.sprite.Group()
explosions = pygame.sprite.Group()

dif = 0
kills = 0
score = Score()
font = pygame.font.SysFont('impact', 50, False, False)

    #          x,y,hp,spd,shotspd,shotdmg,shottype,delay,sprite,spriteshot,team
player = ship(mousex,mousey,100,0,-10,10,'simple',15,playerImg,playershotImg,"green")
boss_spawned = False

#draw
def draw():
    DISPLAYSURF.blit(bg,(0,0))
    drawships(enemy_list)
    drawships(player_list)
    drawshots()
    drawexplosions()
    drawhp()
    spawn()
    pygame.display.update()
    fpsClock.tick(FPS)
    
def drawhp():
    if boss_spawned == True and (boss.rect.x >= -boss.rect.width/2 and boss.rect.x <= graphwidth-boss.rect.width/2):
        pygame.draw.rect(DISPLAYSURF, RED,(0,0,((graphwidth*boss.hp)/300),5))#vidaboss                                         
    pygame.draw.rect(DISPLAYSURF, GREEN, (0,graphheight-5,(graphwidth*player.hp)/100,graphheight))

def drawships(shipt):
    for i in shipt:
        DISPLAYSURF.blit(i.image, (i.rect.x, i.rect.y))

def drawshots():
    for shot in enemy_shots:
        shot.move()
        DISPLAYSURF.blit(shot.image, (shot.rect.x, shot.rect.y))
        if shot.rect.centery <= 0 or shot.rect.centery >= graphheight or shot.rect.centerx <= 0 or shot.rect.centerx >= graphwidth:
            enemy_shots.remove(shot)
            shot.kill()
            continue
        for ship in player_list:
            if shot.rect.centery in range(ship.rect.top,ship.rect.bottom) \
            and shot.rect.centerx in range(ship.rect.left,ship.rect.right):
                ship.hp -= shot.dmg
                #enemy_shots.remove(shot)
                take_dmg_snd.play()
                shot.kill()
        
    for shot in player_shots:
        shot.move()
        DISPLAYSURF.blit(shot.image, (shot.rect.x, shot.rect.y))
        if shot.rect.centery <= 0 or shot.rect.centery >= graphheight or shot.rect.centerx <= 0 or shot.rect.centerx >= graphwidth:
            enemy_shots.remove(shot)
            shot.kill()
            continue
        for ship in enemy_list:
            if shot.rect.centery in range(ship.rect.top,ship.rect.bottom) \
            and shot.rect.centerx in range(ship.rect.left,ship.rect.right):
                ship.hp -= shot.dmg
                ship.state = "fleeing"
                #player_shots.remove(shot)
                shot.kill()

def drawexplosions():
    for explosion in explosions:
        DISPLAYSURF.blit(explosion.image, (explosion.rect.x, explosion.rect.y))

def spawn():
    time = pygame.time.get_ticks() + 30
    global boss_spawned
    global boss
    if (time - time_game_begun) % (1000 + (1000*dif)) < 17:
        if randint(-1,1) == 1:
            spawnrand = randint(0,2)
            if spawnrand == 0:
                mob1 = ship(graphwidth+30,randint(15,graphheight/3),20,6,3,7/dif,'simple',15,mob1Img,straightshot,"red")
            elif spawnrand == 1:
                mob2 = ship(graphwidth+30,randint(15,graphheight/3),20,5,3,7/dif,'curved',30,mob2Img,curvedshotImg,'red')
            elif spawnrand == 2:
                mob3 = ship(graphwidth+30,randint(15,graphheight/3),20,5,3,7/dif,'whip',25,mob3Img,whipImg,'red')
        else:
            spawnrand = randint(0,2)
            if spawnrand == 0:
                mob1 = ship(-30,randint(15,graphheight/3),20,6,3,7/dif,'simple',15,mob1Img,straightshot,"red")
            elif spawnrand == 1:
                mob2 = ship(-30,randint(15,graphheight/3),20,5,3,7/dif,'curved',30,mob2Img,curvedshotImg,'red')
            elif spawnrand == 2:
                mob3 = ship(-30,randint(15,graphheight/3),20,5,3,7/dif,'whip',25,mob3Img,whipImg,'red')
                
    if (time - time_game_begun) > 30000 and boss_spawned == False:
        boss_spawned = True
        if randint(0,1) == 1:
            boss = boss(graphwidth/2+90,-22,300,5,4,10/dif,'boss',70,bossImg,straightshot,"red")
        else:
            boss = boss(graphwidth/2-90,-22,300,5,4,10/dif,'boss',70,bossImg,straightshot,"red")

def inprint(inputs,scoreint):
    global namestr
    global font
    DISPLAYSURF2.fill(BLACK)
    DISPLAYSURF2.blit(font.render(("Your score: " + str(scoreint)),True, WHITE),(graphwidth/2-(font.size(("Your score: " + str(scoreint)))[0])/2,(graphheight/2)-(font.size(("Your score: " + str(scoreint)))[1]/2)))
    DISPLAYSURF2.blit(font.render("Type your name: " + inputs,True, WHITE),(graphwidth/2-(font.size("Type your name: " + inputs)[0])/2,(graphheight/2)+(font.size("Type your name: " + inputs)[1])/2))
    pygame.display.update()
    return

def prnt(dicti):
    DISPLAYSURF2.fill(BLACK)
    height = graphheight/1.6
    for dicto in dicti:
        for key in dicto:
            height -= (font.size(dicto[key])[1])/2
    height -= font.size("High scores:")[1]
    DISPLAYSURF2.blit(font.render("High scores:",True, WHITE),(graphwidth/2-(font.size("High scores:")[0])/2,height-(font.size("High scores:")[1])/2))
    height += font.size("High scores:")[1]
    for dicto in dicti:
        for key in dicto:
            string = str(key) + ": " + str(dicto[key])
            DISPLAYSURF2.blit(font.render(string,True, WHITE),(graphwidth/2-(font.size(string)[0])/2,height-(font.size(string)[1])/2))
            height += (font.size(dicto[key])[1])
    pygame.display.update()

def endgame(scoreint):
    name = []
    namestr = ''
    inprint(namestr, scoreint)
    while True:
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key != K_RETURN and event.key != K_BACKSPACE and event.key != K_MINUS and event.key != K_KP_MINUS:
                    name.append(pygame.key.name(event.key))
                if event.key == K_BACKSPACE and len(name)>0:
                    name.pop() 
                for i in name:
                    namestr += i
                inprint(namestr,scoreint)
                namestr = ''
                if event.key == K_RETURN and len(name)>=0:
                    for i in name: #chamar setscore e mostrar o highscore
                        namestr += i
                    score.setScore(namestr, scoreint)
                    prnt(score.getScore())
                    pygame.time.delay(3600)
                    pygame.quit()
                    sys.exit()
                    
def choosedif():
    global dif
    global mousex
    global mousey
    pygame.mouse.set_visible(1)
    DISPLAYSURF2.fill(BLACK)
    mouseClicked = False
    while True:
        DISPLAYSURF2.blit(font.render("Easy", True, WHITE),(graphwidth/2 - font.size("Easy")[0]/2, graphheight/2 - font.size("Easy")[1]))
        DISPLAYSURF2.blit(font.render("Medium", True, WHITE),(graphwidth/2 - font.size("Medium")[0]/2, graphheight/2))
        DISPLAYSURF2.blit(font.render("Hard", True, WHITE),(graphwidth/2 - font.size("Hard")[0]/2, graphheight/2 + font.size("Hard")[1]))
        pygame.display.update()
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONDOWN:
                mousex, mousey = event.pos
                mouseClicked = True
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = False
        if mousey in range(graphheight/2 - font.size("Easy")[1],graphheight/2) \
           and mousex in range(graphwidth/2 - font.size("Easy")[0]/2,graphwidth/2 + font.size("Easy")[0]/2) \
           and mouseClicked == True:
            dif = 3
            mouseClicked = False
            return False
        if mousey in range(graphheight/2, graphheight/2 + font.size("Medium")[1]) \
           and mousex in range(graphwidth/2 - font.size("Medium")[0]/2,graphwidth/2 + font.size("Medium")[0]/2) \
           and mouseClicked == True:
            dif = 2
            mouseClicked = False
            return False
        if mousey in range(graphheight/2 + font.size("Hard")[1],graphheight/2 + font.size("Hard")[1]*2) \
           and mousex in range(graphwidth/2 - font.size("Hard")[0]/2, graphwidth/2 + font.size("Hard")[0]/2) \
           and mouseClicked == True:
            dif = 1
            mouseClicked = False
            return False

def scoreint():
    return ((player.hp*100000/(pygame.time.get_ticks()))+(kills*100))/dif
        
def menu():
    pygame.mouse.set_visible(1)
    endgame_snd.play()
    global dif
    global mousex
    global mousey
    mouseClicked = False
    if dif == 0:
        while True:
            DISPLAYSURF.fill(BLACK)
            DISPLAYSURF2.blit(font.render("PEW! PEW!",True, WHITE),(graphwidth/2-(font.size("PEW! PEW!")[0])/2,(graphheight/2)-(font.size("PEW! PEW!")[1]*3)))
            DISPLAYSURF2.blit(font.render("START",True, WHITE),(graphwidth/2-(font.size("START")[0])/2,(graphheight/2)+(font.size("START")[1])))
            DISPLAYSURF2.blit(font.render("HIGHSCORES",True, WHITE),(graphwidth/2-(font.size("HIGHSCORES")[0])/2,(graphheight/2)+(font.size("HIGHSCORES")[1]*2)))
            pygame.display.update()
            for event in pygame.event.get(): # event handling loop
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                elif event.type == MOUSEMOTION:
                    mousex, mousey = event.pos
                elif event.type == MOUSEBUTTONDOWN:
                    mousex, mousey = event.pos
                    mouseClicked = True
                elif event.type == MOUSEBUTTONUP:
                    mousex, mousey = event.pos
                    mouseClicked = False
            if mousey in range(((graphheight/2)+(font.size("START")[1])),(graphheight/2)+(font.size("START")[1]*2)) \
               and mousex in range(graphwidth/2-(font.size("START")[0])/2,graphwidth/2+(font.size("START")[0])/2) \
               and mouseClicked == True:
                mouseClicked = False
                choosedif()
                break
            if mousey in range(((graphheight/2)+(font.size("HIGHSCORE")[1]*2)),(graphheight/2)+(font.size("HIGHSCORE")[1]*3)) \
               and mousex in range(graphwidth/2-(font.size("HIGHSCORE")[0])/2,graphwidth/2+(font.size("HIGHSCORE")[0])/2) \
               and mouseClicked == True:
                prnt(score.getScore())
                pygame.time.delay(3600)
                mouseClicked = False
                
#run the game loop
if dif == 0:
    menu()
endgame_snd.fadeout(1000)
pygame.mouse.set_visible(0)
ost_snd.play()
time_game_begun = pygame.time.get_ticks()

while True:
    if time_game_finished != 0:  
        if pygame.time.get_ticks() - time_game_finished > 2000:
            endgame(scoreint())
    if player.hp <= 0 and game_finish == 0:
        game_finish = 1
        time_game_finished = pygame.time.get_ticks()
    elif boss_spawned == True and boss.hp <= 0 and game_finish == 0:
        game_finish = 1
        time_game_finished = pygame.time.get_ticks()
    for event in pygame.event.get(): # event handling loop
        if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
        elif event.type == MOUSEBUTTONUP:
            mousex, mousey = event.pos
            mouseClicked = False
        elif event.type == MOUSEBUTTONDOWN:
            mousex, mousey = event.pos
            mouseClicked = True
    if mouseClicked == True and delay <= 0 and player.hp > 0:
        player.shoot()
        delay = 15
    delay -= 1 #Player's shot delay
    player.rect.x = mousex-player.rect.width/2
    player.rect.y = mousey-player.rect.height/2 #Centers the mouse at player's ship
    draw()
    for i in enemy_list:
        if i.hp < 1:
            kills += 1
            i.explode()
            continue
        i.aishoot()
        i.aimov()
    for i in player_list:
        if i.hp <= 0:
            i.explode()
    for explosion in explosions:
        explosion.cycle()
