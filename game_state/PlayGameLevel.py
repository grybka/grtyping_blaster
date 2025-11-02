import pygame
from game_state.GameManager import GameState, GameManagerBase
from game_world.GameWorld import GameWorld
from graphics.Graphics import Graphics
from game_state.GameLevels import get_levelone_script
from sound.Sound import get_sound_store

class PlayGameLevel(GameState):
    def __init__(self,screen):
        # Initialize graphics first and pass to world
        self.graphics = Graphics(screen)
        get_sound_store().load_sounds()
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

    def get_status(self):
        if self.world.game_on==False:   
            if self.world.player_alive==False:
                return "GameOver"
            else:
                return "LevelDone"
        return "PlayingLevel"



class LevelDoneState(GameState):
    def __init__(self,screen,score):
        self.screen=screen
        self.font=pygame.font.Font(None,48)
        self.text=self.font.render(f"Level Complete!\n   Score: {score}",True,(255,255,255))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        self.score=score

    def handle_event(self, event):
        ...

    def update(self, time_delta):
        ...

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.text,self.text_rect)

class GameOverState(GameState):
    def __init__(self,screen,score):
        self.screen=screen
        self.font=pygame.font.Font(None,48)
        self.text=self.font.render(f"Game Over!\n   Score: {score}",True,(255,0,0))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        self.score=score

    def handle_event(self, event):
        ...

    def update(self, time_delta):
        ...

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.text,self.text_rect)

class GameManager(GameManagerBase):
    def __init__(self,screen,on_game_state=None):
        super().__init__(on_game_state)
        self.screen=screen

    def next_state(self, status):
        if status=="LevelDone":
            score=self.on_game_state.world.player_score
            #self.on_game_state.world.end_level()
            self.on_game_state=LevelDoneState(self.screen,score)
        elif status=="GameOver":
            score=self.on_game_state.world.player_score
            #self.on_game_state.world.end_level()
            self.on_game_state=GameOverState(self.screen,score)