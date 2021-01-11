import ecs
from enum import Enum
import math

class SegmentComponent(ecs.Component):
    def __init__(self,start,end):
        self.start = start
        self.end = end

    def __getstate__(self):
        return ((int(self.start[0]),int(self.start[1])),
                 (int(self.end[0]),int(self.end[1])))

    def __setstate__(self, state):
        self.start = state[0]
        self.end = state[1]

    @staticmethod
    def rotate_vector(vector, angle):
        radians = math.radians(angle)
        return (vector[0] * math.cos(radians) - vector[1] * math.sin(radians),
            vector[0] * math.sin(radians) + vector[1] * math.cos(radians))

class SegmentTypes(Enum):
    WALL = (0,180,0)
    CHECKPOINT = (0,0,170)
    RAY = (255,50,50)
    COLLIDER = (255,0,0)

class SegmentTypeComponent(ecs.Component):
    def __init__(self,type: SegmentTypes):
        self.type = type

    def __getstate__(self):
        return self.type

    def __setstate__(self, state):
        self.type = state

class SegmentWallComponent(ecs.Component):
    def __init__(self):
        pass

class SegmentRayHolder(ecs.Component):
    def __init__(self,ray):
        self.rays = [ray]
    def add(self,ray):
        self.rays.append(ray)

class SegmentRayComponent(ecs.Component):
    def __init__(self,parent_entity, offset,relative_angle, length):
        self.parent = parent_entity
        self.offset = offset
        self.relative_angle = relative_angle
        self.length = length

        self.collision_point = (0, 0)
        self.collision_distance = 0