import pygame
from game_state.GameManager import GameState
from game_world.GameWorld import GameWorld
from graphics.Graphics import Graphics
from game_state.GameLevels import get_levelone_script

class PlayGameLevel(GameState):
    def __init__(self,screen):
        # Initialize graphics first and pass to world
        self.graphics = Graphics(screen)
        self.world = GameWorld(self.graphics)
        self.level_script = get_levelone_script(self.world)

    def handle_event(self, event):
        if event.type==pygame.TEXTINPUT:
            #event.text contains the character typed
            self.world.text_typed(event.text)
        ...

    def update(self, time_delta):
        self.world.update(time_delta)
        self.graphics.update(time_delta)
        self.level_script.update(time_delta)

    def draw(self,screen):
        self.graphics.draw(screen)