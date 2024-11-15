import ecs
import math
import numpy as np

class Velocity(ecs.Component):
    def __init__(self,vel: np.array):
        self.vel = vel

    def magnitude(self) -> float:
        return np.linalg.norm(self.vel)

