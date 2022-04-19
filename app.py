import re
from time import sleep
import pygame

from pygame.display import flip

#initialize Pygame
pygame.init()

class State:
    def __init__(self):
        self.x = 250
        self.y = 250

    def update(self, xinc, yinc):
        self.x += xinc
        self.y += yinc

    def render(self,surface):
        clear_surface(surface)
        pygame.draw.circle(surface,(0,255,255),[self.x,self.y],100)
        flip()


def main():
    pos = State()
    surface = create_main_surface()
    looper = 0
    while(looper == 0):
        pos.render(surface)
        paused = False
        
        if event_listener(1,1,pos) == False:
            return
        sleep(1/60)
       
def event_listener(xmov, ymov, pos):
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            return False  
        if (event.type == pygame.KEYDOWN):    
            if(event.key==pygame.K_DOWN):
                pos.update(0, 100)
            elif(event.key==pygame.K_UP):
                pos.update(0, -100)
            elif(event.key==pygame.K_RIGHT):
                pos.update(100, 0)
            elif(event.key==pygame.K_LEFT):
                pos.update(-100, 0)
            else:
               pos.update(0,0)
    return True


def create_main_surface():
    #set size of window
    screen_size = (1024, 768)
    #create display window
    return pygame.display.set_mode(screen_size)

def clear_surface(surface):
    surface.fill((0,0,0,0))

main()