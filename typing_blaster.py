import pygame
from game_state.LevelSelect import LevelSelectState
#from game_state.PlayGameLevel import PlayGameLevel,GameManager
from game_state.GameManager import GameManager

pygame.init()
pygame.font.init()

clock=pygame.time.Clock()

#set up the window to draw
displayinfo=pygame.display.Info()
max_x=2*1024
max_y=2*768
if displayinfo.current_w*0.9<max_x:
    max_x=int(displayinfo.current_w*0.9)
if displayinfo.current_h*0.8<max_y:
    max_y=int(displayinfo.current_h*0.8)
resolution=(max_x,max_y)
screen=pygame.display.set_mode(resolution,pygame.DOUBLEBUF | pygame.HWSURFACE) 


#set up game manager
#game_manager=GameManager(screen,PlayGameLevel(screen))
game_manager=GameManager(screen,LevelSelectState(screen))

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
        if event.type==pygame.QUIT:
            running=False
        #Tell manager to handle event
        game_manager.handle_event(event)
    #tell manager to update
    time_delta=clock.tick(60)/1000.0
    game_manager.update(time_delta)
    #tell manager to draw
    game_manager.draw(screen)
    pygame.display.flip()

pygame.quit()