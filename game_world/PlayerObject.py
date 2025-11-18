from game_world.GameWorld import WorldObject

class PlayerObject(WorldObject):
    def __init__(self, sprite=None, position=(0, 0)):
        self.sprite=sprite
        super().__init__(position=position)
        

    def get_sprites(self):
        return [self.sprite] if self.sprite else []
