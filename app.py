from random import randint
import re
from sqlite3 import enable_callback_tracebacks
from time import sleep
from tkinter import Frame
from venv import create
from winsound import PlaySound
import pygame
import math
from pygame.time import *
from pygame.display import flip
import os
import music
import Sounds
from pygame import MOUSEBUTTONDOWN
from pygame import K_ESCAPE
from pygame import KEYDOWN

from pygame import K_RETURN

from pygame import K_SPACE


def create_main_surface():
    width = 1024
    height = 768
    screen_size = (width, height)
    return pygame.display.set_mode(screen_size)


#initialize Pygame
pygame.init()
surface = create_main_surface()
menu_font = pygame.font.SysFont(None,120)
gameover_font = pygame.font.SysFont(None,150)
soundlib = Sounds.SoundLibrary.find_audio_files()
scrollspeed = 150
running = False

def draw_text(text,font,color,surface,x,y):
    textobj = font.render(text,1,color)
    textrect = textobj.get_rect()
    textrect.topleft = (x,y)
    surface.blit(textobj,textrect)

def draw_sprite(surface,hitbox,sprite,xpos,ypos,xscale,yscale,flipbool):
    pygame.draw.rect(surface,(255,0,0),hitbox,-1)
    button = load_image(f"assets/images/{sprite}")
    button = pygame.transform.scale(button,(xscale,yscale))
    if flipbool:
        button = pygame.transform.flip(button,True,False)
    draw_centered(surface,button,xpos,ypos)

def main_menu():
    menu_background = Background()
    clock = pygame.time.Clock()
    character_number = 2
    #music_player()
    click = False

    button_back_hitbox = pygame.Rect(345,350,65,105)
    button_next_hitbox = pygame.Rect(614,350,65,105)
    button_start_hitbox = pygame.Rect(410,490,202,70)

    while(True):
        elapsed_seconds = clock.tick() / 1000
        menu_background.update(elapsed_seconds)
        menu_background.render(surface)

        draw_text('Choose your raccoon!',menu_font,(255,255,255),surface,70,100)

        mx, my = pygame.mouse.get_pos()

        if button_back_hitbox.collidepoint((mx,my)):
            if click:
                character_number-=1
        if button_next_hitbox.collidepoint((mx,my)):
            if click:
                character_number+=1
        if button_start_hitbox.collidepoint((mx,my)):
            if click:
                game(skins[character_number%5])
                pygame.mixer.music.stop()


        draw_sprite(surface,button_back_hitbox,"menu/arrow.svg",375,400,100,100,False)
        
        draw_sprite(surface,button_next_hitbox,"menu/arrow.svg",650,400,100,100,True)
        
        draw_sprite(surface,button_start_hitbox,"menu/start.png",513,525,250,120,False)
        
        skins = ["brown","darkgray","gray","orange","red"]
        sprite = load_image(f"assets/images/menu/character/{skins[character_number%5]}.png")
        sprite = pygame.transform.scale(sprite,(144,144))
        draw_centered(surface,sprite,512,384)

        click = False
        paused = False
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pressed = pygame.key.get_pressed()
        if pressed[K_RETURN]:
            game(skins[character_number%5])
            
        flip()

#main function
def game(skin):
    running = True
    state = State(skin)
        
    clock = pygame.time.Clock()
    
    music_player = music.music_player()
    music_player
    
    while(running):
        mine_chance = randint(0,120)
        if mine_chance==4:
            state.mines.append(Mine())
        enemy_chance = randint(0,120)
        match enemy_chance:
            case 1:
                state.enemies.append(Enemy(1))
            case 2:
                state.enemies.append(Enemy(2))
        elapsed_seconds = clock.tick() / 1000
        state.update(elapsed_seconds)
        render_frame(surface,state)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
        
        event_listener(state,elapsed_seconds)

def game_over():
    gameover_background = Background()
    clock = pygame.time.Clock()
    #music_player()
    click = False
    button_restart_hitbox = pygame.Rect(408,490,208,71)
    
    while(True):
        
        elapsed_seconds = clock.tick() / 1000
        gameover_background.update(elapsed_seconds)
        gameover_background.render(surface)

        draw_text('Game Over',gameover_font,(255,255,255),surface,220,300)
        draw_sprite(surface,button_restart_hitbox,"gameover/restart.png",508,525,230,90,False)
        mx, my = pygame.mouse.get_pos()

        if button_restart_hitbox.collidepoint((mx,my)):
            if click:
                main_menu()
                pygame.mixer.music.stop()
        

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        pressed = pygame.key.get_pressed()
        if pressed[K_RETURN]:
            main_menu()
            
        flip()

def event_listener(state,elapsed_seconds):

    pressed = pygame.key.get_pressed()
    speed = 500
    
    if pressed[pygame.K_DOWN]:
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_LEFT]:
            speed = speed/1.41  
        if state.player.y+36 > 768:
            speed = 0 
        state.player.y += speed * elapsed_seconds
    if pressed[pygame.K_UP]:
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_LEFT]:
            speed = speed/1.41
        if state.player.y-36 < 0:
            speed = 0
        state.player.y -= speed * elapsed_seconds
    if pressed[pygame.K_RIGHT]:
        if state.player.x+16 > 1024:
            speed = 0
        state.player.x += speed * elapsed_seconds
    if pressed[pygame.K_LEFT]:
        if state.player.x-36 < 0:
            speed = 0
        state.player.x -= speed * elapsed_seconds
    if pressed[pygame.K_SPACE]:
        if state.cooldown.ready:
            state.bullets.append(Bullet(state.player.x,state.player.y))
            state.cooldown.reset()
    #if pressed[pygame.K_a]:
    #    noise = randint(0, 5)
    #    Sounds.SoundLibrary.play_random_explosion(soundlib, noise)

def create_main_surface():
    width = 1024
    height = 768
    screen_size = (width, height)
    return pygame.display.set_mode(screen_size)

def clear_surface(surface):
    surface.fill((0,0,0,0))

def render_frame(surface,state):
    state.render(surface)
    flip()

def load_image(path):
    return pygame.image.load(path)

def draw_centered(surface,image,x,y):
    (width, height) = image.get_size()
    surface.blit(image,[x-(width/2),y-(height/2)])

def update_objects(elapsed_seconds,list):
    j = 0
    while j < len(list):
        object = list[j]
        object.update(elapsed_seconds)
        if object.disposed:
            list.remove(object)
        else: 
            j += 1

def process_collisions(spaceship,mines,enemies,bullets,enemybullets,frames=[]):
    frames_explosion = [load_image(f'assets/images/sprites/explosion/{i}.png') for i in range(1,10)]
    for bullet in bullets:
        for enemy in enemies:
            if bullet.hitbox.colliderect(enemy.hitbox):
                bullet.disposed = True
                enemy.disposed = True
                frames.append(FrameBasedAnimation(frames_explosion,0.1,enemy.x,enemy.y))
                Sounds.SoundLibrary.play_random_explosion(soundlib, randint(0,5))

    for bullet in enemybullets:
        if bullet.hitbox.colliderect(spaceship.hitbox):
            frames.append(FrameBasedAnimation(frames_explosion,0.1,spaceship.x,spaceship.y))
            Sounds.SoundLibrary.play_random_explosion(soundlib, randint(0,5))
            game_over()
        

    mine_hitbox = [mine.hitbox for mine in mines]
    enemy_hitbox = [enemy.hitbox for enemy in enemies]

    ship_hits_mine = spaceship.hitbox.collidelist(mine_hitbox)
    ship_hits_enemy = spaceship.hitbox.collidelist(enemy_hitbox)

    if ship_hits_mine !=-1 or ship_hits_enemy!=-1:
        Sounds.SoundLibrary.play_random_explosion(soundlib, randint(0,5))
        frames.append(FrameBasedAnimation(frames_explosion,0.1,spaceship,spaceship.y))
        pygame.mixer.music.stop()
        game_over()       

class State:
    def __init__(self,skin):
        self.background = Background()
        self.player = Spaceship(skin)
        self.bullets = []
        self.cooldown = Cooldown(0.2)
        self.mines = [Mine()]
        self.enemies = [Enemy(1)]
        self.enemybullets = [EnemyBullet(500,50)]
        self.explosions = []
        
    def update(self, elapsed_seconds):
        self.player.update(elapsed_seconds)
        update_objects(elapsed_seconds,self.explosions)
        self.background.update(elapsed_seconds)
        self.cooldown.update(elapsed_seconds)
        process_collisions(self.player,self.mines,self.enemies,self.bullets,self.enemybullets,self.explosions)
        update_objects(elapsed_seconds,self.enemybullets)
        update_objects(elapsed_seconds,self.bullets)
        update_objects(elapsed_seconds,self.enemies)
                
        for mine in self.mines:
            mine.update(elapsed_seconds)
            if mine.disposed:
                self.mines.pop(0)

    def render(self,surface):
        self.background.render(surface)
        for enemy in self.enemies:
            enemy.render(surface)
        self.player.render(surface)
        for mine in self.mines:
            mine.render(surface)
        for bullet in self.bullets:
            bullet.render(surface)
        for explosion in self.explosions:
            explosion.render(surface)
        for bullet in self.enemybullets:
            bullet.render(surface)
        
        
    
class Background:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.imageheight = 1875
        self.imagewidth = 1024
        self.__image = self.__create_image()
        
    def __create_image(self):
        background = pygame.image.load("assets/images/backgrounds/background3.jpg")
        background = pygame.transform.scale(background, (self.imagewidth, self.imageheight))
        return background

    def update(self,elapsed_seconds):
        #scrollspeed = 300
        self.y += elapsed_seconds*scrollspeed
         
    def render(self,surface):
        surface.fill((0,0,0))
        surface.blit(self.__image,[self.x,self.y])
        surface.blit(self.__image,[self.x,self.y-self.imageheight])
        if self.y >= self.imageheight:
            surface.blit(self.__image,[self.x,self.y-self.imageheight])
            self.y = 0


class Spaceship:
    def __init__(self,skin):
        
        self.skin = skin
        self.player_images = [pygame.transform.scale(load_image(f'assets/images/sprites/ship/{self.skin}{i}.png'),(144,144)) for i in range(1,5)]
        self.animation_raccoon = CircularFrameBasedAnimation(self.player_images,0.2)
        self.x = 512
        self.y = 680
        self.hitbox = pygame.Rect(self.x-31,self.y+50-72,53,94)

    def resize_images(self):
        for img in self.player_images:
            pygame.transform.scale(img,(144,144))

    def update(self, elapsed_seconds):
        self.animation_raccoon.update(elapsed_seconds)

    def render(self,surface):
        self.hitbox = pygame.Rect(self.x-31,self.y+50-72,53,94)
        pygame.draw.rect(surface,(0,0,0),self.hitbox,-1)
        self.animation_raccoon.render(surface,self.x,self.y)
        
class FrameBasedAnimation:
    def __init__(self,frames,seconds_per_frame,x=0,y=0):
        self.x = x
        self.y = y
        self.time_passed = 0
        self.frames = frames
        self.seconds_per_frame = seconds_per_frame
        self.counter = 0
        self.__disposed = False
        
    def dispose(self):
        self.__disposed = True
    
    @property
    def disposed(self):
        return self.__disposed

    def render(self,surface):
        frame_index = math.floor(self.time_passed / self.seconds_per_frame)
        if frame_index < len(self.frames):
            frame = self.frames[frame_index]
            draw_centered(surface,frame,self.x,self.y)
        else:
            self.dispose()
    
    def update(self,elapsed_seconds):
        self.time_passed += elapsed_seconds


class CircularFrameBasedAnimation(FrameBasedAnimation):
    def render(self,surface,x,y):
        frame_index = math.floor(self.time_passed / self.seconds_per_frame) % len(self.frames)
        frame = self.frames[frame_index]
        draw_centered(surface,frame,x,y)

class Bullet():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        Sounds.SoundLibrary.play_random_explosion(soundlib, 6)
        self.speed = 300
        self.bullet = load_image("assets/images/sprites/bullets/small.png")
        self.__time_left = 5
        self.disposed = False
        self.hitbox = pygame.Rect(self.x-10,self.y-30,20,20)

    def update(self,elapsed_seconds):
        self.y -= self.speed * elapsed_seconds
        self.__time_left -= elapsed_seconds
        if self.__time_left < 0:
            self.disposed = True
    
    def render(self,surface):
        draw_centered(surface,self.bullet,self.x+1,self.y-20)
        self.hitbox = pygame.Rect(self.x-9,self.y-29,19,19)
        pygame.draw.rect(surface,(0,0,0),self.hitbox,-1)
        
class Cooldown:
    def __init__(self,cooldown):
        self.ready = True
        self.time_passed = 0
        self.cooldown = cooldown

    def update(self,elapsed_seconds):
        self.time_passed += elapsed_seconds
        if self.time_passed > self.cooldown:
            self.ready = True

    def reset(self):
        self.time_passed = 0
        self.ready = False

class Mine():
    def __init__(self):
        self.x = randint(50,950)
        self.y = -100
        self.mine = load_image("assets/images/sprites/tree.png")
        self.disposed = False
        self.__time_left = 12.8
        self.hitbox = pygame.Rect(self.x-44,self.y-50,88,125)

    def update(self,elapsed_seconds):
        #scrollspeed = 300
        self.y += elapsed_seconds*scrollspeed
        self.__time_left -= elapsed_seconds
        if self.__time_left < 0:
            self.disposed = True

    def render(self,surface):
        draw_centered(surface,self.mine,self.x,self.y)
        self.hitbox = pygame.Rect(self.x-44,self.y-40,88,115)
        pygame.draw.rect(surface,(0,0,0),self.hitbox,-1)

class Enemy():
    def __init__(self,enemyid):
        self.x = randint(100,900)
        self.y = -100
        self.enemyid = enemyid
        self.enemy1 = [pygame.transform.scale(load_image(f'assets/images/sprites/enemies/enemy1/fox{i}.png'),(144,144)) for i in range(1,5)]        
        self.animation_enemy1 = CircularFrameBasedAnimation(self.enemy1,0.2)

        self.enemy2 = [pygame.transform.scale(load_image(f'assets/images/sprites/enemies/enemy2/croc{i}.png'),(144,144)) for i in range(1,5)]        
        self.animation_enemy2 = CircularFrameBasedAnimation(self.enemy2,0.2)

        self.disposed = False
        self.__time_left = 14
        self.hitbox = pygame.Rect(self.x-20,self.y-60,50,125)
        self.total_seconds = 0

    def update(self,elapsed_seconds):
        self.total_seconds += elapsed_seconds
        self.x += math.cos(self.total_seconds)*3
        self.y += elapsed_seconds*scrollspeed*1.1
        self.__time_left -= elapsed_seconds
        if self.__time_left < 0:
            self.disposed = True
        match self.enemyid:
            case 1: 
                self.animation_enemy1.update(elapsed_seconds)
            case 2:
                self.animation_enemy2.update(elapsed_seconds)       
        

    def render(self,surface):
        #draw_centered(surface,self.enemy,self.x,self.y)
        self.hitbox = pygame.Rect(self.x-20,self.y-60,50,125)
        pygame.draw.rect(surface,(0,0,0),self.hitbox,-1)
        match self.enemyid:
                case 1: 
                    self.animation_enemy1.render(surface,self.x,self.y)
                case 2:
                    self.animation_enemy2.render(surface,self.x,self.y) 

class EnemyBullet():
    def __init__(self,x,y):
        self.x = x
        self.y = y
        
        Sounds.SoundLibrary.play_random_explosion(soundlib, 6)
        self.speed = 300
        self.bullet = load_image("assets/images/sprites/bullets/small.png")
        self.__time_left = 5
        self.disposed = False
        self.hitbox = pygame.Rect(self.x-10,self.y-30,20,20)

    def update(self, elapsed_seconds):
        self.y += self.speed * elapsed_seconds
        self.__time_left -= elapsed_seconds
        if self.__time_left < 0:
            self.disposed = True
    
    def render(self,surface):
        draw_centered(surface,self.bullet,self.x+1,self.y-20)
        self.hitbox = pygame.Rect(self.x-9,self.y-29,19,19)
        pygame.draw.rect(surface,(0,0,0),self.hitbox,-1)


main_menu()