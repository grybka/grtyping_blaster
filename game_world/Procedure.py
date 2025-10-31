# A generic class for a series of steps that need to be updated
# and may be finished

class ProcedureStep:
    def __init__(self):
        pass

    def update(self, time_delta):
        pass

    def start_step(self):
        pass

    def step_done(self):
        return True
    
    def set_property(self, property_name, value):
        #Many steps have a source sprite, or target, or something
        #So we can have generic properties, we use this
        return False



class Procedure:
    def __init__(self,steps=None):
        if steps is None:
            steps = []
        self.procedure_steps=steps
        self.on_step = -1
    
    def add_step(self,step: ProcedureStep):
        self.procedure_steps.append(step)

    def update(self, time_delta):
        if self.on_step == -1 and len(self.procedure_steps) > 0:
            self.on_step = 0
            self.procedure_steps[0].start_step()
        if self.on_step < len(self.procedure_steps):
            current_step = self.procedure_steps[self.on_step]
            current_step.update(time_delta)
            if current_step.step_done():
                self.on_step += 1
                if self.on_step < len(self.procedure_steps):
                    self.procedure_steps[self.on_step].start_step()

    def set_property(self, property_name, value):
        tf=[ step.set_property(property_name, value) for step in self.procedure_steps]
        return any(tf)
    
    def is_done(self):
        return self.on_step >= len(self.procedure_steps)