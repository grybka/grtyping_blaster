
from game_world.Procedure import ProcedureStep
from graphics.GraphicsBase import WorldSprite
from sprite.SpriteWithTextWindow import SpriteWithTextWindow

#TODO make a SpriteMotionScriptElement that is derived from ProcedureStep
# it specifically has a sprite associated with it

class SpriteMotionScriptElement(ProcedureStep):
    def __init__(self, sprite: WorldSprite):
        super().__init__()
        self.sprite = sprite

    def set_property(self, property_name, value):
        if property_name == "sprite":
            self.sprite = value
            return True
        return super().set_property(property_name, value)


class SMSE_SetPosition(SpriteMotionScriptElement):
    # This motion script element sets the sprite to a specific position instantly
    def __init__(self, sprite: WorldSprite=None, position=None):
        super().__init__(sprite)
        self.position = position

    def is_done(self):
        return self.sprite.get_world_position(None) == self.position

    def update(self, time_delta):
        self.sprite.set_position(self.position)

class SMSE_MoveToPosition(SpriteMotionScriptElement):
    # This motion script element moves the sprite to a target position at a given speed
    def __init__(self, sprite: WorldSprite=None, end_position=None, duration=None):
        super().__init__(sprite)
        self.end_position = end_position or (0,0)
        self.duration = duration or 1.0
        self.elapsed_time = 0

    def start_step(self):
        self.start_position = self.sprite.get_world_position(None)

    def step_done(self):
        return self.elapsed_time >= self.duration

    def update(self, time_delta):
        self.elapsed_time += time_delta
        new_x = self.start_position[0] + (self.end_position[0] - self.start_position[0]) * min(self.elapsed_time / self.duration, 1.0)
        new_y = self.start_position[1] + (self.end_position[1] - self.start_position[1]) * min(self.elapsed_time / self.duration, 1.0)
        self.sprite.set_position((new_x, new_y))
       

class SMSE_MoveToSprite(SpriteMotionScriptElement):
    # This motion script element moves the sprite to a target sprite over a given duration
    def __init__(self, sprite: WorldSprite, target_sprite: WorldSprite, duration):
        super().__init__(sprite)
        self.target_sprite = target_sprite
        self.duration = duration
        self.elapsed_time = 0
        
    def start_step(self):
        self.start_position = self.sprite.get_world_position(None)

    def step_done(self):
        return self.elapsed_time >= self.duration
    
    def update(self, time_delta):
        self.end_position = self.target_sprite.get_world_position(None)
        self.elapsed_time += time_delta
        new_x = self.start_position[0] + (self.end_position[0] - self.start_position[0]) * min(self.elapsed_time / self.duration, 1.0)
        new_y = self.start_position[1] + (self.end_position[1] - self.start_position[1]) * min(self.elapsed_time / self.duration, 1.0)
        self.sprite.set_position((new_x, new_y))


class SMSE_MoveToPosition_Smooth(SpriteMotionScriptElement):
    # This motion script element moves the sprite to a target position with a max acceleration and max speed
    def __init__(self, sprite: WorldSprite, initial_position, final_position, initial_velocity=(0,0),final_velocity=(0,0), duration=1.0):
        super().__init__(sprite)
        self.initial_position = initial_position
        self.final_position = final_position
        self.initial_velocity = initial_velocity
        self.final_velocity = final_velocity
        self.duration = duration
        self.elapsed_time = 0

    def start_step(self):
        super().start_step()
        # write out the math
        if self.initial_position:
            initial_position=self.initial_position
        else:
            initial_position=self.sprite.get_world_position(None)
        final_position=self.final_position
        initial_velocity=self.initial_velocity
        final_velocity=self.final_velocity
        duration=self.duration
        x0=initial_position[0]
        x1=final_position[0]
        vx0=initial_velocity[0]*duration
        vx1=final_velocity[0]*duration
        y0=initial_position[1]
        y1=final_position[1]
        vy0=initial_velocity[1]*duration
        vy1=final_velocity[1]*duration
        nx1 = x1 - x0 - vx0
        nx2 = vx1 - vx0
        ny1 = y1 - y0 - vy0
        ny2 = vy1 - vy0
        self.ax = ( x0, vx0, 3*nx1 - nx2, -2*nx1 + nx2)
        self.ay = ( y0, vy0, 3*ny1 - ny2, -2*ny1 + ny2)


    def step_done(self):
        # Check if the sprite has reached the target position
        if self.elapsed_time >= self.duration:
            self.sprite.set_position(self.final_position)
            return True
        return False

    def update(self, time_delta):
        # Update the sprite's position based on a smooth interpolation
        self.elapsed_time += time_delta
        t = min(self.elapsed_time / self.duration, 1.0)
        x = self.ax[0] + self.ax[1]*t + self.ax[2]*t**2 + self.ax[3]*t**3
        y = self.ay[0] + self.ay[1]*t + self.ay[2]*t**2 + self.ay[3]*t**3
        self.sprite.set_position((x, y))
        return True

class SMSE_ChangeTextboxVisibility(SpriteMotionScriptElement):
    def __init__(self, sprite: SpriteWithTextWindow, target_visibility: bool):
        super().__init__(sprite)
        self.target_visibility = target_visibility
   
    def step_done(self):
        return self.sprite.get_text_window_visibility() == self.target_visibility

    def update(self, time_delta):
        self.sprite.set_text_window_visibility(self.target_visibility)
        return True
    
class SMSE_Wait(SpriteMotionScriptElement):
    def __init__(self, sprite: SpriteWithTextWindow, duration: float):
        super().__init__(sprite)
        self.duration = duration
        self.elapsed_time = 0
    def step_done(self):
        return self.elapsed_time >= self.duration
    def update(self, time_delta):
        self.elapsed_time += time_delta
        return True
    
class SMSE_RemoveSprite(SpriteMotionScriptElement):
    def __init__(self, sprite: WorldSprite):
        super().__init__(sprite)
        self.is_done=False

    def step_done(self):
        return self.is_done
    
    def update(self, time_delta):
        self.sprite.schedule_for_removal()
        self.is_done=True
        return True
