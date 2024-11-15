import ecs

class CarControllerComponent(ecs.Component):
    def __init__(self,max_speed,speed_falloff):
        self.max_speed = max_speed
        self.max_angular_speed = 1.8
        self.speed_falloff = speed_falloff

        self.last_steering = 0

        self.steering = 0
        self.gas = 0