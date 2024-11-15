import ecs

class Rotation(ecs.Component):
    def __init__(self,rotation):
        self.rotation = rotation
