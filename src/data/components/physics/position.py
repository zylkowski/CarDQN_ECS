import ecs
import numpy as np

class Position(ecs.Component):
    def __init__(self,pos:np.ndarray):
        self.pos = pos

    def __getstate__(self):
        return (int(self.pos[0]),int(self.pos[1]))

    def __setstate__(self, state:np.ndarray):
        self.pos = state

