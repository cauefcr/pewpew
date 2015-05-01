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
ex4 = pygame.image.load('explosion4.png')#All explosion frames
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
class shot(pygame.sprite.Sprite): #creates shot as an object, which ships will create with their methods
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
    def move(self): #defines how each type of shots will move, each ship has a different type.
        if self.type == 'simple':
            self.rect.y += self.spd
        elif self.type == 'curved':#Sine-like movement
            self.rect.y += self.spd
            self.rect.x += self.spd*2*sin(self.cont) - self.spd*2*cos(self.cont)
            self.cont += 0.2
        elif self.type == 'whip':#Circular movement
            self.rect.y += self.spd*sin(self.cont) + self.spd*cos(self.cont) + 1.5
            self.rect.x += self.spd*sin(self.cont) - self.spd*cos(self.cont)
            self.cont += 0.1
        elif self.type == 'boss':#Explosive sort of shot
            self.rect.y += self.spd
            if self.rect.y > 320: #When it has travelled enough, explodes into 8 more different shots
                pi = 3.14159265359
                cont = 0
                for i in range(1,9):
                    spd = self.spd * cos(cont)#Each shot speed is controlled by a factor of sine and cosine
                    spdy = self.spd * sin(cont)#so that they move diagonally with the correct speed, as to mimic a circle.
                    instance = shot(self.rect.x,self.rect.y,spd,2/dif,'radial',radial_shot,'red')
                    instance.spdy = spdy
                    cont += pi/4
                self.kill()#.kill() is a method that comes with the inheritance from pygame.sprite.Sprite, it completely deletes the object
        elif self.type == 'radial':
            self.rect.y += self.spdy
            self.rect.x += self.spd
    
class ship(pygame.sprite.Sprite): #sets up the ship class, which is the main class that represents all space-ships in the game.
    state = 'hunting'
    def __init__(self,x,y,hp,spd,shotspd,shotdmg,shottype,delay,sprite,spriteshot,team):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.hp = hp
        #variables that control the movement
        self.spd = 0
        self.maxspd = spd
        self.accel = spd/5
        #variables that store the shot information
        self.shotspd = shotspd
        self.shotdmg = shotdmg
        self.shottype = shottype
        self.delay = delay
        self.spriteshot = spriteshot
        self.maxdelay = delay
        #team is used to discern whether the object is an enemy or not
        self.team = team
        if self.team == 'red':
            enemy_list.add(self)
        else:
            player_list.add(self)

    def shoot(self): #creates an shot object based on the ship's current position and which one is it
        if self.team == 'red':
            instance = shot(self.rect.x+(0.8*self.rect.width/2),self.rect.y+(self.rect.height),self.shotspd,self.shotdmg,self.shottype,self.spriteshot,self.team)
        else:
            instance = shot(self.rect.x+(0.7*(self.rect.width/2)),self.rect.y-(self.rect.height/2),self.shotspd,self.shotdmg,self.shottype,self.spriteshot,self.team)
        
    def aimov(self): #uses states as the mean of choosing how the AI ships will move
        if self.state == "hunting": #follows the player
            if player.rect.centerx > self.rect.centerx+self.maxspd+self.rect.width/4 \
               and self.spd <= self.maxspd:
                self.spd += self.accel
            elif player.rect.centerx < self.rect.centerx-(self.maxspd+self.rect.width/4) \
               and self.spd > -self.maxspd:
                self.spd -= self.accel
                
        if self.state == "fleeing": #runs from the player
            if self.rect.centerx not in range(0,graphwidth): #when ship reaches either of the screen edges, go back to hunting
                self.state = "hunting"
                return
            if player.rect.centerx > self.rect.centerx \
               and self.rect.centerx in range(0,graphwidth)\
               and self.spd > -self.maxspd:#if the player is to the right of the ship, move towards the left
                self.spd -= self.accel
            elif player.rect.centerx < self.rect.centerx \
               and self.rect.centerx in range(0,graphwidth)\
               and self.spd < self.maxspd:#if its left, move right
                self.spd += self.accel
        self.rect.x += self.spd
            
    def aishoot(self): #the method which is used for controlling shot spawns, and only if it's an member of the AI team
        if self.team == "red":
            self.delay -= 1
        if self.delay <= 0:
                self.shoot()
                self.delay = self.maxdelay
    def explode(self): #method called when the ship dies, which plays the sound and creates an object explosion, where the ship was
        exploding_snd.play()
        self.exploding = True
        instance = explos(self.rect.x-self.rect.width,self.rect.y-self.rect.height)
        self.kill()
        return

class boss(ship): #boss has some different patterns, so we created a new object that inherits all the basics from the 'ship' object
    def explode(self): #calls 3 explosions, instead of one
        global boss_spawned
        boss_is_dead_snd.play()
        boss_spawned = False
        instance = explos(self.rect.x,self.rect.y)
        instance = explos(self.rect.x+self.rect.width/2,self.rect.y)
        instance = explos(self.rect.x+self.rect.width,self.rect.y)
        self.kill()
    def aimov(self): #changes the movement for the boss, so that it can spawn in the middle
        if self.rect.centery < self.rect.height+5:#Also never flees. The boss doesn't mind taking some shots
            self.rect.centery += self.accel
        if player.rect.centerx > self.rect.centerx+self.maxspd+self.rect.width/4 and self.spd <= self.maxspd/2:
            self.spd += self.accel
            self.rect.x += self.spd/4
        elif player.rect.centerx < self.rect.centerx-(self.maxspd+self.rect.width/4) and self.spd > -self.maxspd/2:
           self.spd -= self.accel
           self.rect.x += self.spd/4
        self.rect.x += self.spd
    def shoot(self): #works in a way so that the hp affects how the boss attacks.
        if self.hp <= 300:
            instance = shot(self.rect.x+(0.8*self.rect.width/2),self.rect.y+(self.rect.height),self.shotspd,self.shotdmg,self.shottype,self.spriteshot,self.team)
        if self.hp <= 220:
            instance = shot(self.rect.x+(0.8*self.rect.width/2),self.rect.y+(self.rect.height),self.shotspd,self.shotdmg,'simple',straightshot,self.team)
        if self.hp <= 180:
            instance = shot(self.rect.x+(0.8*self.rect.width/2),self.rect.y+(self.rect.height),self.shotspd,self.shotdmg,'curved',curvedshotImg,self.team)
        if self.hp <= 120:
            instance = shot(self.rect.x+(0.8*self.rect.width/2),self.rect.y+(self.rect.height),self.shotspd,self.shotdmg,'whip',whipImg,self.team)
class explos(pygame.sprite.Sprite): #the class which one calls when it's hp is below 0, creating an explosion where it was
    explode_frame = 0
    explodeimg = [ex2,ex3,ex4,ex5,ex6,ex7,ex8,ex9,ex10,ex11,ex12,ex13,ex14]#List containing all sprites for the explosion
    def __init__(self,x,y,sprite=ex1):
        pygame.sprite.Sprite.__init__(self)
        self.image = sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        explosions.add(self)
    def cycle(self):#Everytime this method is called, it changes the current sprite to the next until its at the last one
        if self.explode_frame == len(self.explodeimg):
            self.kill()#Then it deletes the whole object.
            return
        self.image = self.explodeimg[self.explode_frame]
        self.explode_frame += 1
        
#set up the variables
#mouse variables
mousex = 0
mousey = 0
mouseClicked = False
#variables used to store time and game-state
game_finish = 0
time_game_begun = 0
time_game_finished = 0

#groups that will contain every object in the game
enemy_list = pygame.sprite.Group()
player_list = pygame.sprite.Group()
enemy_shots = pygame.sprite.Group()
player_shots = pygame.sprite.Group()
explosions = pygame.sprite.Group()

everything = [enemy_list,player_shots,enemy_shots,explosions]

gamemode = ''
dif = 1 #Difficulty, hard by standard.
kills = 0 #kills, used for the purpose of scoring
score = Score() #Score object, explained in detail at score.py
font = pygame.font.SysFont('impact', 50, False, False) #prepares a font according to pygame syntax

    #          x,y,hp,spd,shotspd,shotdmg,shottype,delay,sprite,spriteshot,team
player = ship(mousex,mousey,100,0,-10,10,'simple',15,playerImg,playershotImg,"green")
boss_spawned = False

#draw
def draw(): #calls the surface drawing functions, and updates the screen
    DISPLAYSURF.blit(bg,(0,0))
    drawships(enemy_list)
    drawships(player_list)
    drawshots()
    drawexplosions()
    drawhp()
    pygame.display.update()
    fpsClock.tick(FPS)
    
def drawhp(): #draws the hp bar for the boss and the player
    if boss_spawned == True \
        and (bigboss.rect.x >= -bigboss.rect.width/2 \
        and bigboss.rect.x <= graphwidth-bigboss.rect.width/2):
        pygame.draw.rect(DISPLAYSURF, RED,(0,0,((graphwidth*bigboss.hp)/300),5))#boss                                      
    pygame.draw.rect(DISPLAYSURF, GREEN, (0,graphheight-5,(graphwidth*player.hp)/100,graphheight)) #player

def drawships(shipt): #draws all the different ships in a given list
    for i in shipt:
        DISPLAYSURF.blit(i.image, (i.rect.x, i.rect.y))

def drawshots():  #draws all the shots and checks collision 
    for shot in enemy_shots:
        shot.move()
        DISPLAYSURF.blit(shot.image, (shot.rect.x, shot.rect.y))
        if shot.rect.centery not in range(0,graphheight)\
           or shot.rect.centerx not in range(0,graphwidth): 
            enemy_shots.remove(shot)
            shot.kill()
            continue
        for ship in player_list:
            if shot.rect.centery in range(ship.rect.top,ship.rect.bottom) \
            and shot.rect.centerx in range(ship.rect.left,ship.rect.right): #shot collision checking with the player
                ship.hp -= shot.dmg
                take_dmg_snd.play()
                shot.kill()
        
    for shot in player_shots:
        shot.move()
        DISPLAYSURF.blit(shot.image, (shot.rect.x, shot.rect.y))
        if shot.rect.centery not in range(0,graphheight)\
           or shot.rect.centerx not in range(0,graphwidth): #shot collision checking with the enemies
            shot.kill()
            continue
        for ship in enemy_list:
            if shot.rect.centery in range(ship.rect.top,ship.rect.bottom) \
            and shot.rect.centerx in range(ship.rect.left,ship.rect.right):
                ship.hp -= shot.dmg
                ship.state = "fleeing"
                shot.kill()

def cleargroup(group):
    for i in group:
        for j in i:
            j.kill()

def drawexplosions(): #draws all the explosions
    for explosion in explosions:
        DISPLAYSURF.blit(explosion.image, (explosion.rect.x, explosion.rect.y))

def spawn(): #controls where and when will the enemies appear
    time = pygame.time.get_ticks() + 30 #gets time after pygame.init was called, in ms
    global boss_spawned
    global bigboss #bigboss has to be global so that bigboss.hp and .x/.y may be checked along the code
    if (time - time_game_begun) % (1000 + (1000*dif)) < 17 and boss_spawned == False: #before the boss has spawned, spawn random mobs, from either left or right
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
                
    if (time - time_game_begun) % 30000 <= 17 and boss_spawned == False: #if a certain time has passed and the boss has not appeared, make him appear
        boss_spawned = True
        if randint(0,1) == 1:
            bigboss = boss(graphwidth/2+90,-22,300,5,4,10/dif,'boss',70,bossImg,straightshot,"red")
        else:
            bigboss = boss(graphwidth/2-90,-22,300,5,4,10/dif,'boss',70,bossImg,straightshot,"red")

def inprint(inputs,scoreint): #ui for high-score name input
    global namestr
    global font
    DISPLAYSURF2.fill(BLACK)
    DISPLAYSURF2.blit(font.render(("Your score: " + str(scoreint)),True, WHITE),(graphwidth/2-(font.size(("Your score: " + str(scoreint)))[0])/2,(graphheight/2)-(font.size(("Your score: " + str(scoreint)))[1]/2)))
    DISPLAYSURF2.blit(font.render("Type your name: " + inputs,True, WHITE),(graphwidth/2-(font.size("Type your name: " + inputs)[0])/2,(graphheight/2)+(font.size("Type your name: " + inputs)[1])/2))
    pygame.display.update()

def prnt(dicti): #ui for showing high-scores
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

def endgame(scoreint): #loop that holds what happens after either you or the boss died
    name = []#stores all the letters the user types, one by one.
    namestr = ''#empty string, will store the final name as typed by the player.
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
                    for i in name: #calls setscore and shows the highscore
                        namestr += i #concatenates every letter in name to a single string
                    score.setScore(namestr, scoreint)
                    prnt(score.getScore())
                    pygame.time.delay(3600)
                    ost_snd.fadeout(1000)
                    menu()
                    
def choosedif(): #ui for choosing difficulty 
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
            play()
            return
        if mousey in range(graphheight/2, graphheight/2 + font.size("Medium")[1]) \
           and mousex in range(graphwidth/2 - font.size("Medium")[0]/2,graphwidth/2 + font.size("Medium")[0]/2) \
           and mouseClicked == True:
            dif = 2
            mouseClicked = False
            play()
            return
        if mousey in range(graphheight/2 + font.size("Hard")[1],graphheight/2 + font.size("Hard")[1]*2) \
           and mousex in range(graphwidth/2 - font.size("Hard")[0]/2, graphwidth/2 + font.size("Hard")[0]/2) \
           and mouseClicked == True:
            dif = 1
            mouseClicked = False
            play()
            return

def choosemode(): #ui for choosing mode
    global gamemode
    global mousex
    global mousey
    pygame.mouse.set_visible(1)
    DISPLAYSURF2.fill(BLACK)
    mouseClicked = False
    while True:
        DISPLAYSURF2.blit(font.render("Arcade", True, WHITE),(graphwidth/2 - font.size("Arcade")[0]/2, graphheight/2 + font.size("Arcade")[1]))
        DISPLAYSURF2.blit(font.render("Survival", True, WHITE),(graphwidth/2 - font.size("Survival")[0]/2, graphheight/2 - font.size("Survival")[1]))
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
        if mousey in range(graphheight/2 - font.size("Survival")[1],graphheight/2) \
           and mousex in range(graphwidth/2 - font.size("Survival")[0]/2,graphwidth/2 + font.size("Survival")[0]/2) \
           and mouseClicked == True:
            gamemode = 'survival'
            play()
            mouseClicked = False
            return
        if mousey in range(graphheight/2 + font.size("Arcade")[1],graphheight/2 + font.size("Arcade")[1]*2) \
           and mousex in range(graphwidth/2 - font.size("Arcade")[0]/2, graphwidth/2 + font.size("Arcade")[0]/2) \
           and mouseClicked == True:
            gamemode = 'arcade'
            mouseClicked = False
            choosedif()
            return
        
def scoreint(): #defines how the score is calculated
    return ((player.hp*100000/(time_game_finished-time_game_begun)+(kills*100))/dif)

def menu(): #main menu
    pygame.mouse.set_visible(1)
    endgame_snd.play()
    global dif
    global mousex
    global mousey
    mouseClicked = False
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
            choosemode()
            return
        if mousey in range(((graphheight/2)+(font.size("HIGHSCORE")[1]*2)),(graphheight/2)+(font.size("HIGHSCORE")[1]*3)) \
           and mousex in range(graphwidth/2-(font.size("HIGHSCORE")[0])/2,graphwidth/2+(font.size("HIGHSCORE")[0])/2) \
           and mouseClicked == True:
            prnt(score.getScore())
            pygame.time.delay(3600)
            mouseClicked = False

def play():
    endgame_snd.fadeout(1000)
    pygame.mouse.set_visible(0)
    ost_snd.play()
    global mousex
    global mousey
    global mouseClicked
    global player

    global game_finish
    global time_game_finished
    global time_game_begun

    global kills
    global boss_spawned
    player_shot_delay = 0 #Will be used at the game-loop in order to control the player rof
    player_rof = 15 #rate of fire, how many frames has to pass until the next shot is fired
    player.hp = 100
    time_game_begun = pygame.time.get_ticks()
    time_game_finished = 0
    game_finish = 0
    boss_spawned = False
    kills = 0
    cleargroup(everything)
    while True:
        if time_game_finished != 0:  
            if pygame.time.get_ticks() - time_game_finished > 2000:
                endgame(scoreint())
        if player.hp <= 0 and game_finish == 0:
            game_finish = 1
            time_game_finished = pygame.time.get_ticks()
        elif boss_spawned == True and bigboss.hp <= 0 and game_finish == 0 and gamemode == 'arcade':
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
        if mouseClicked == True and player_shot_delay <= 0 and player.hp > 0:
            player.shoot()
            player_shot_delay = player_rof
        player_shot_delay -= 1 
        draw()
        if not boss_spawned:
            spawn()
        for shipt in enemy_list:
            if shipt.hp < 1:
                kills += 1
                shipt.explode()
                continue
            shipt.aishoot()
            shipt.aimov()
        for shipt in player_list:
            if shipt.hp <= 0:
                shipt.explode()
            else:
                shipt.rect.x = mousex-shipt.rect.width/2
                shipt.rect.y = mousey-shipt.rect.height/2 #Centers the mouse at player's ship
        for explosion in explosions:
            explosion.cycle()

#run the game loop
menu()
