import pygame, sys
from pygame.locals import *

from speechyesno import *
from pye import *
import os


from pye import *
BLACK =    (0,  0,  0)
WHITE =    (255,255,255)#white color in RGB format

FPS = 5
 
def main():
    pygame.init()
    pygame.font.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((700,500)) 
    start=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath('__file__')),"st.png")).convert_alpha()
    start=pygame.transform.scale(start, (100, 50))
    mouseClicked = False
    mousex = 0
    mousey = 0
    pygame.display.set_caption('FACE_RECOGNITION') 
    image=pygame.image.load(os.path.join(os.path.dirname(os.path.realpath('__file__')),"lk.jpg")).convert_alpha()
    image=pygame.transform.scale(image, (700, 500))
    
    DISPLAYSURF.fill(WHITE)#for white backgorund
    DISPLAYSURF.blit(image,(0,0))
  
    DISPLAYSURF.blit(start,(100,300))
    while True: #main game loop
        
        for event in pygame.event.get():
            
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        if mouseClicked == True:
         if Rect(100,300,100,50).collidepoint(mousex,mousey):
          pygame.quit()
          xmain()
          main()  
        pygame.display.update()
       
        FPSCLOCK.tick(FPS)
if __name__=='__main__':
  
 main()           
        