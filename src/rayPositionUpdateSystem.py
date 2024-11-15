import ecs
import data.components.segment as segment
import data.components.physics as physics
import numpy as np

class RayPositionUpdateSystem(ecs.System):
    def update(self, dt):
        self.entity_manager : ecs.EntityManager
        for e,ray_component in self.entity_manager.pairs_for_type(segment.SegmentRayComponent):
            ray_component : segment.SegmentRayComponent
            try:
                parent_entity = ray_component.parent
                segment_component: segment.SegmentComponent = self.entity_manager.component_for_entity(e,segment.SegmentComponent)
                origin_pos : physics.Position = self.entity_manager.component_for_entity(parent_entity,physics.Position)
                origin_rot : physics.Rotation = self.entity_manager.component_for_entity(parent_entity,physics.Rotation)

                segment_component.start = np.add(origin_pos.pos,ray_component.offset)
                segment_component.end = RayPositionUpdateSystem.rotate(np.add(segment_component.start,(ray_component.length,0)),
                                                                       origin=segment_component.start,
                                                                       degrees=90-origin_rot.rotation-ray_component.relative_angle)

            except:
                print("Error in RayPositionUpdateSystem")

    @staticmethod
    def rotate(p, origin=(0, 0), degrees=0):
        angle = np.deg2rad(degrees)
        R = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle), np.cos(angle)]])
        o = np.atleast_2d(origin)
        p = np.atleast_2d(p)
        return np.squeeze((R @ (p.T - o.T) + o.T).T)