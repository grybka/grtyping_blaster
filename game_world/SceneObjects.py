from game_world.GameWorld import WorldObject

class SceneObject(WorldObject):
    #This is an object in the scene that is not a target or interactable
    def __init__(self, sprite=None, position=(0, 0)):
        self.sprite=sprite
        super().__init__(position=position)
        
    def get_sprites(self):
        return [self.sprite] if self.sprite else []
    
    def finalize(self):
        for sprite in self.get_sprites():
            sprite.schedule_for_removal()
        