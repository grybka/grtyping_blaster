import pygame
from game_state.GlobalPlayerState import GlobalPlayerState


class GameStatus:
    def __init__(self,change_state: bool, new_state: str = "", data = None):
        self.change_state = change_state
        self.new_state = new_state
        self.data = data

class GameState: #abstract base class
    def __init__(self, global_player_state=None):
        self.global_player_state= global_player_state

    def set_global_player_state(self, global_player_state: GlobalPlayerState):
        self.global_player_state=global_player_state

    def start(self):
        #called when it first starts updating
        ...

    def handle_event(self, event):
        ...

    def update(self, time_delta):
        ...

    def draw(self,screen):
        ...

    def get_status(self):
        #Returns a string indicating what the next state should be if finished
        return GameStatus(False)


class GameManagerBase(GameState):
    def __init__(self,on_game_state=None):
        self.on_game_state=on_game_state

    def handle_event(self, event):
        self.on_game_state.handle_event(event)

    def update(self, time_delta):
        self.on_game_state.update(time_delta)
        self.next_state(self.on_game_state.get_status())

    def draw(self,screen):
        self.on_game_state.draw(screen)

    def next_state(self, status):
        pass