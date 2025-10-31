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


class GameManager(GameState):
    def __init__(self):
        ...

    def handle_event(self, event):
        ...

    def update(self, time_delta):
        ...

    def draw(self,screen):
        ...