import pygame
from game_state.GameManagerBase import GameState,GameStatus
from graphics.Graphics import Graphics
from graphics.GraphicsBase import Camera
from sprite.TextBox import TextBox


#Primarily a list of things you can buy, cost / sold out
#also a chance to switch ships

class StoreItem:
    def __init__(self,name,description,cost):
        self.name=name
        self.description=description
        self.cost=cost
        self.sold_out=False

class TheStore(GameState):
    def __init__(self,screen, global_player_state=None):
        super().__init__(global_player_state)
        self.graphics = Graphics(screen)        
        self.screen=screen
        self.should_quit=False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.should_quit=True

    def update_text(self):
        #update the text box with things you can buy
        pass

    def update(self, time_delta):
        pass

    def draw(self,screen):
        #screen.fill((0,0,0))
        self.graphics.draw(screen)

        

    def get_status(self):
        if self.should_quit:
            return GameStatus(True, "ReturnToGame")
        return GameStatus(False)