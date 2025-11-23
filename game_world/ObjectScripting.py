
import math
from game_world.Procedure import ProcedureStep
from game_world.GameWorld import WorldObject
from sound.Sound import get_sound_store

class ObjectScriptStep(ProcedureStep):
    def __init__(self, object: WorldObject= None):
        super().__init__()
        self.object = object

    def set_property(self, property_name, value):
        if property_name == "object":
            self.object = value
            return True
        return super().set_property(property_name, value)

class SetObjectPosition(ObjectScriptStep):
    # This motion script element sets the object to a specific position instantly
    def __init__(self, object: WorldObject=None, position=None):
        super().__init__(object)
        self.position = position

    def is_done(self):
        return self.object.get_position(None) == self.position

    def update(self, time_delta):
        self.object.set_position(self.position)


class SetObjectPositionToOtherObject(ObjectScriptStep):
    # This motion script element sets the object to a specific position instantly
    def __init__(self, object: WorldObject=None, target: WorldObject=None):
        super().__init__(object)
        self.target = target
        self.is_done_flag = False

    def is_done(self):
        return self.is_done_flag

    def update(self, time_delta):
        self.object.set_position(self.target.get_position())
        self.is_done_flag = True

class MoveObjectToPosition(ObjectScriptStep):
    # This motion script element moves the object to a target position at a given speed
    def __init__(self, end_position, object: WorldObject=None, duration=None):
        super().__init__(object)
        self.end_position = end_position or (0,0)
        self.duration = duration or 1.0
        self.elapsed_time = 0

    def start_step(self):
        self.elapsed_time = 0
        self.start_position = self.object.get_position()

    def step_done(self):
        return self.elapsed_time >= self.duration

    def update(self, time_delta):
        self.elapsed_time += time_delta
        new_x = self.start_position[0] + (self.end_position[0] - self.start_position[0]) * min(self.elapsed_time / self.duration, 1.0)
        new_y = self.start_position[1] + (self.end_position[1] - self.start_position[1]) * min(self.elapsed_time / self.duration, 1.0)
        self.object.set_position((new_x, new_y))

class MoveObjectToPosition_Smooth(ObjectScriptStep):
    # This motion script element moves the sprite to a target position with a max acceleration and max speed
    def __init__(self, end_position, object: WorldObject=None, initial_velocity=(0,0),final_velocity=(0,0), duration=1.0):
        super().__init__(object)
        self.initial_position = None
        self.final_position = end_position
        self.initial_velocity = initial_velocity
        self.final_velocity = final_velocity
        self.duration = duration
        self.elapsed_time = 0

    def start_step(self):
        super().start_step()
        # write out the math
        self.elapsed_time = 0
        initial_position=self.object.get_position()
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
            self.object.set_position(self.final_position)
            return True
        return False

    def update(self, time_delta):
        # Update the sprite's position based on a smooth interpolation
        self.elapsed_time += time_delta
        t = min(self.elapsed_time / self.duration, 1.0)
        x = self.ax[0] + self.ax[1]*t + self.ax[2]*t**2 + self.ax[3]*t**3
        y = self.ay[0] + self.ay[1]*t + self.ay[2]*t**2 + self.ay[3]*t**3
        self.object.set_position((x, y))
        return True
    
class MoveObjectToObject(ObjectScriptStep):
    # This motion script element moves the object to another object's position over a duration
    def __init__(self, target_object: WorldObject, object: WorldObject=None, duration=1.0):
        super().__init__(object)
        self.target_object = target_object
        self.duration = duration
        self.elapsed_time = 0
        self.start_position = None

    def start_step(self):
        self.elapsed_time = 0
        self.start_position = self.object.get_position()

    def step_done(self):
        return self.elapsed_time >= self.duration

    def update(self, time_delta):
        self.elapsed_time += time_delta
        target_position = self.target_object.get_position()
        new_x = self.start_position[0] + (target_position[0] - self.start_position[0]) * min(self.elapsed_time / self.duration, 1.0)
        new_y = self.start_position[1] + (target_position[1] - self.start_position[1]) * min(self.elapsed_time / self.duration, 1.0)
        self.object.set_position((new_x, new_y))

class WobbleObject(ObjectScriptStep):
    def __init__(self, object: WorldObject=None, amplitude_x: float = 0, amplitude_y: float = 0, frequency_x: float = 0, frequency_y: float = 0, duration: float = 0):
        super().__init__(object)
        self.amplitude_x = amplitude_x
        self.amplitude_y = amplitude_y
        self.frequency_x = frequency_x
        self.frequency_y = frequency_y
        self.duration = duration
        self.elapsed_time = 0

    def start_step(self):
        self.start_position = self.object.get_position()

    def step_done(self):    
        return self.duration>0 and self.elapsed_time >= self.duration

    def update(self, time_delta):
        self.elapsed_time += time_delta
        #if self.elapsed_time > self.duration:
            #self.sprite.set_position(self.start_position)
            #return
        new_x = self.start_position[0] + self.amplitude_x * math.sin(2 * math.pi * self.frequency_x * self.elapsed_time)
        new_y = self.start_position[1] + self.amplitude_y * math.sin(2 * math.pi * self.frequency_y * self.elapsed_time)
        self.object.set_position((new_x, new_y))

class SpawnSpriteAtObject(ObjectScriptStep):
    def __init__(self, sprite, object: WorldObject=None, graphics=None):
        super().__init__(object)
        self.sprite = sprite
        self.spawned_sprite = None
        self.is_done_flag = False
        self.graphics = graphics

    def step_done(self):
        return self.is_done_flag

    def update(self, time_delta):
        if self.spawned_sprite is None:
            self.spawned_sprite = self.sprite
            position = self.object.get_position()
            print("spawning sprite at ", position)
            self.spawned_sprite.set_world_position(position)
            self.graphics.add_sprite(self.spawned_sprite)
            self.is_done_flag = True

class DespawnSelfObject(ObjectScriptStep):
    def __init__(self, object: WorldObject=None):
        super().__init__(object)
        self.is_done_flag = False

    def step_done(self):
        return self.is_done_flag

    def update(self, time_delta):
        print("Despawning object ", self.object)
        self.object.schedule_for_removal()
        self.is_done_flag = True

class DespawnOtherObject(ObjectScriptStep):
    def __init__(self, target_object: WorldObject, object: WorldObject=None):
        super().__init__(object)
        self.target_object = target_object
        self.is_done_flag = False

    def step_done(self):
        return self.is_done_flag

    def update(self, time_delta):
        print("Despawning object ", self.target_object)
        self.target_object.schedule_for_removal()
        self.is_done_flag = True
        
class DamagePlayer(ObjectScriptStep):
    def __init__(self, damage_amount: int, object: WorldObject=None):
        super().__init__(object)
        self.damage_amount = damage_amount
        self.is_done_flag = False

    def step_done(self):
        return self.is_done_flag

    def update(self, time_delta):
        game_world = self.object.game_world
        game_world.damage_player(self.damage_amount)
        self.is_done_flag = True

class StartTimer(ObjectScriptStep):
    # This starts the timer on targets that have a timer
    def __init__(self, object: WorldObject=None):
        super().__init__(object)
        #self.time_amount = time_amount
        self.is_done_flag = False

    def step_done(self):
        return self.is_done_flag

    def update(self, time_delta):
        if not self.is_done_flag:
            #self.object.start_timer(self.time_amount)
            self.object.start_timer()
            self.is_done_flag = True

class PlaySound(ObjectScriptStep):
    def __init__(self, sound_name: str, object: WorldObject=None):
        super().__init__(object)
        self.sound_name = sound_name
        self.is_done_flag = False

    def step_done(self):
        return self.is_done_flag

    def update(self, time_delta):
        if not self.is_done_flag:
            get_sound_store().play_sound(self.sound_name)
            self.is_done_flag = True