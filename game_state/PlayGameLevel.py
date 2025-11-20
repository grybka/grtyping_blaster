import pygame
from game_state.GameManagerBase import GameState, GameManagerBase, GameStatus
from game_world.GameWorld import GameWorld
from graphics.Graphics import Graphics
from game_state.GameLevels import get_levelone_script, get_leveltwo_script
from sound.Sound import get_sound_store

class PlayGameLevel(GameState):
    def __init__(self,screen,level_name="LevelOne"):
        # Initialize graphics first and pass to world
        self.graphics = Graphics(screen)
        get_sound_store().load_sounds()
        self.world = GameWorld(self.graphics)
        #self.level_script = get_levelone_script(self.world)
        self.level_script = get_levelone_script(self.world)

    def start(self):
        self.graphics.show_overlay=True

    def handle_event(self, event):
        if event.type==pygame.TEXTINPUT:
            #event.text contains the character typed
            self.world.text_typed(event.text)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.world.text_typed('\n')
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
                return GameStatus(True, "LevelDoneState")
            else:
                return GameStatus(True, "GameOverState")
        return GameStatus(False)
        #if self.world.game_on==False:   
        ##    if self.world.player_alive==False:
        #        return "GameOver"
        #    else:
        #        return "LevelDone"
        #return "PlayingLevel"



class LevelDoneState(GameState):
    def __init__(self,screen,score):
        self.screen=screen
        self.font=pygame.font.Font(None,48)
        self.text=self.font.render(f"Level Complete!\n   Score: {score}",True,(255,255,255))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        self.score=score
        self.should_quit=False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.should_quit=True        

    def update(self, time_delta):
        ...

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.text,self.text_rect)
    
    def get_status(self):
        if self.should_quit:
            return GameStatus(True, "LevelSelectState")
        return GameStatus(False)

class GameOverState(GameState):
    def __init__(self,screen,score):
        self.screen=screen
        self.font=pygame.font.Font(None,48)
        self.text=self.font.render(f"Game Over!\n   Score: {score}",True,(255,0,0))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        self.score=score
        self.should_quit=False

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            self.should_quit=True            

    def update(self, time_delta):
        ...

    def draw(self,screen):
        screen.fill((0,0,0))
        screen.blit(self.text,self.text_rect)

    def get_status(self):
        if self.should_quit:
            return GameStatus(True, "LevelSelectState")
        return GameStatus(False)
