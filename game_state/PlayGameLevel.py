import pygame
from game_state.GameManagerBase import GameState, GameManagerBase, GameStatus
from game_world.GameWorld import GameWorld
from graphics.Graphics import Graphics
from game_state.GameLevels import *
from sound.Sound import get_sound_store

class LevelScore:
    def __init__(self,letters_hit, letters_missed):
        self.letters_hit=letters_hit
        self.letters_missed=letters_missed

    def get_score(self):
        return self.letters_hit*10 - self.letters_missed*5

class PlayGameLevel(GameState):
    def __init__(self,screen,level_name={}):
        # Initialize graphics first and pass to world
        self.graphics = Graphics(screen)
        get_sound_store().load_sounds()
        self.world = GameWorld(self.graphics)
        if level_name["name"]=="Introduction":
            self.level_script=get_levelzero_script(self.world)
        else:        
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
            score = LevelScore(self.world.letters_hit, self.world.letters_missed).get_score()
            if self.world.player_alive==False:
                return GameStatus(True, "LevelDoneState", data=score)
            else:
                return GameStatus(True, "GameOverState", data=score)
        return GameStatus(False)
        #if self.world.game_on==False:   
        ##    if self.world.player_alive==False:
        #        return "GameOver"
        #    else:
        #        return "LevelDone"
        #return "PlayingLevel"



class LevelDoneState(GameState):
    def __init__(self,screen,score: LevelScore):
        self.screen=screen
        self.font=pygame.font.Font(None,48)
        self.text=self.font.render(f"Level Complete!\n",True,(255,255,255))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        #make a text rect that shows letters hit, letters missed, and score
        self.letters_hit_text=self.font.render(f"Letters Hit: {score.letters_hit}", True, (255,255,255))
        self.letters_missed_text=self.font.render(f"Letters Missed: {score.letters_missed}", True, (255,255,255))
        self.score_text=self.font.render(f"Score: {score.get_score()}", True, (255,255,255))
        self.letters_hit_rect=self.letters_hit_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 50))
        self.letters_missed_rect=self.letters_missed_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 100))
        self.score_rect=self.score_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 150))
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
        screen.blit(self.letters_hit_text,self.letters_hit_rect)
        screen.blit(self.letters_missed_text,self.letters_missed_rect)
        screen.blit(self.score_text,self.score_rect)
    
    def get_status(self):
        if self.should_quit:
            return GameStatus(True, "LevelSelectState")
        return GameStatus(False)

class GameOverState(GameState):
    def __init__(self,screen,score):
        self.screen=screen
        self.font=pygame.font.Font(None,48)
        self.text=self.font.render(f"You Got Exploded!",True,(255,0,0))
        self.text_rect=self.text.get_rect(center=(screen.get_width()//2,screen.get_height()//2))
        #make a text rect that shows letters hit, letters missed, and score
        self.letters_hit_text=self.font.render(f"Letters Hit: {score.letters_hit}", True, (255,255,255))
        self.letters_missed_text=self.font.render(f"Letters Missed: {score.letters_missed}", True, (255,255,255))
        self.score_text=self.font.render(f"Score: {score.get_score()}", True, (255,255,255))
        self.letters_hit_rect=self.letters_hit_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 50))
        self.letters_missed_rect=self.letters_missed_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 100))
        self.score_rect=self.score_text.get_rect(center=(screen.get_width()//2,screen.get_height()//2 + 150))
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
        screen.blit(self.letters_hit_text,self.letters_hit_rect)
        screen.blit(self.letters_missed_text,self.letters_missed_rect)
        screen.blit(self.score_text,self.score_rect)

    def get_status(self):
        if self.should_quit:
            return GameStatus(True, "LevelSelectState")
        return GameStatus(False)
