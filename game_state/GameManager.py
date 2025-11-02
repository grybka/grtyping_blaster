import pygame


class GameState: #abstract base class
    def __init__(self):
        ...

    def handle_event(self, event):
        ...

    def update(self, time_delta):
        ...

    def draw(self,screen):
        ...

    def get_status(self):
        #Returns a string indicating what the next state should be if finished
        return "Generic Game State"    


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