from graphics.Graphics import Graphics
from game_world.Target import Target
from sprite.SpriteFactory import SpriteFactory

class GameWorld:
    def __init__(self,graphics: Graphics):
        self.graphics=graphics
        self.targets=[]
        self.on_target=None
        self.player_health=100
        self.player_score=0
        self.procedures=[]
        self.some_bool=False
        self.player_sprite=None
        print("Game World initialized as ", self)

    def get_player_sprite(self):
        return self.player_sprite

    def set_player_sprite(self,sprite):
        self.player_sprite=sprite
        print("screen position:", self.graphics.screen_size[0]//2, self.graphics.screen_size[1]-100)
        self.player_sprite.set_screen_position((self.graphics.screen_size[0]//2, self.graphics.screen_size[1]-100),self.graphics.camera)       
        self.graphics.add_sprite(sprite)

    def add_target(self,target: Target):
        self.targets.append(target)

    def add_procedure(self,procedure):
        self.procedures.append(procedure)
        self.some_bool=True

    def text_typed(self,text):
        if self.on_target is None:
            #figure out which to target
            if len(self.targets)==1:
                self.on_target=self.targets[0]
            else:
                for target in self.targets:
                    if target.text.startswith(text):
                        self.on_target=target
                        break
                if self.on_target is None:
                    #no target found
                    return
        self.on_target.text_typed(text)

    def update(self, time_delta):
        for target in self.targets:
            target.update(time_delta)
            if target.should_remove:
                if self.on_target==target:
                    self.on_target=None
                target.finalize()
                self.player_score+=len(target.text)
        #update procedures
        for procedure in self.procedures:
            procedure.update(time_delta)
        self.procedures=[p for p in self.procedures if not p.is_done()]
        #remove any completed targets
        self.targets=[t for t in self.targets if not t.should_remove]
        self.graphics.overlay.player_health=self.player_health
        self.graphics.overlay.player_score=self.player_score

    def get_player_world_position(self):
        return self.get_player_sprite().get_world_position(None)
