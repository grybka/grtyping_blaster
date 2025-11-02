from game_world.Procedure import ProcedureStep
from sound.Sound import get_sound_store

class WP_Wait(ProcedureStep):
    def __init__(self, duration):
        super().__init__()
        self.duration = duration
        self.elapsed_time = 0

    def update(self, time_delta):
        self.elapsed_time += time_delta

    def step_done(self):
        return self.elapsed_time >= self.duration

class WP_DamagePlayer(ProcedureStep):
    def __init__(self, game_world, damage_amount):
        super().__init__()
        self.game_world = game_world
        self.damage_amount = damage_amount
        self.done = False

    def update(self, time_delta):
        print("WPDAMAGEPLACE: Damaging player by", self.damage_amount)
        self.game_world.player_health -= self.damage_amount
        self.done = True

    def step_done(self):
        return self.done
    
class WP_PlayerDead(ProcedureStep):
    def __init__(self, game_world,explosion_anim):
        super().__init__()
        self.game_world = game_world
        self.done = False
        self.explosion_anim=explosion_anim
    
    def update(self, time_delta):
        if self.explosion_anim.should_remove:
            self.done=True
            self.game_world.game_on=False

    def step_done(self):
        return self.done
    
class WP_PlaySound(ProcedureStep):
    def __init__(self, sound_name):
        super().__init__()
        self.sound_name = sound_name
        self.done = False

    def update(self, time_delta):
        get_sound_store().play_sound(self.sound_name)
        self.done = True

    def step_done(self):
        return self.done
    
class WP_PlayAnimation(ProcedureStep):
    def __init__(self, graphics, animation):
        super().__init__()
        self.graphics = graphics
        self.animation = animation
        self.is_done = False

    
    def update(self, time_delta):
        self.graphics.add_sprite(self.animation)        
        self.is_done = True

    def step_done(self):
        return self.is_done