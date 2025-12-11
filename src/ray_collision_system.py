import ecs
import data.components.segment as segment
import data.components.physics as physics
import data.systems.rendering as rendering
import numpy as np
from numba import njit
import pygame


class RayCollisionSystem(ecs.System):
    def update(self, dt):
        self.entity_manager: ecs.EntityManager
        # try:
        for ray_entity, ray_component in self.entity_manager.pairs_for_type(segment.SegmentRayComponent):
            ray_component: segment.SegmentRayComponent
            ray_segment_component: segment.SegmentComponent = self.entity_manager \
                .component_for_entity(ray_entity,
                                      segment.SegmentComponent)

            closest_collision, closest_collision_point, _ = RayCollisionSystem.get_closest_ray_intersection(self.entity_manager,
                                                                                                            ray_segment_component,
                                                                                                            ray_component,
                                                                                                            segment.SegmentTypes.WALL)
            ray_component.collision_distance = closest_collision
            ray_component.collision_point = closest_collision_point
            RayCollisionSystem.render_collision_point(closest_collision_point)
    # except:
    #     print("error in RayCollisionSystem")

    @staticmethod
    def get_closest_ray_intersection(entity_manager, ray_segment_component, ray_component, intersection_segment_type):
        collision_dict = {}
        for segment_entity, segment_type_component in entity_manager.pairs_for_type(
                segment.SegmentTypeComponent):
            segment_type_component: segment.SegmentTypeComponent

            if segment_type_component.type == intersection_segment_type:
                segment_component: segment.SegmentComponent = entity_manager \
                    .component_for_entity(segment_entity,
                                          segment.SegmentComponent)

                if RayCollisionSystem.intersect(ray_segment_component.start,
                                                ray_segment_component.end,
                                                segment_component.start,
                                                segment_component.end):
                    collision_point = RayCollisionSystem.calculate_collision_point(ray_segment_component.start,
                                                                                   ray_segment_component.end,
                                                                                   segment_component.start,
                                                                                   segment_component.end)
                    distance = np.linalg.norm(np.subtract(collision_point, ray_segment_component.start))
                    collision_dict[distance] = (collision_point, segment_entity)

        if len(collision_dict) is not 0:
            closest_collision = min(list(collision_dict.keys()))
            closest_collision_point = collision_dict[closest_collision][0]
            closest_collision_entity = collision_dict[closest_collision][1]
            return closest_collision/ray_component.length, closest_collision_point, closest_collision_entity
        return 1.0, ray_segment_component.end, None


    @staticmethod
    def render_collision_point(point):
        render_lambda = lambda screen, point=point: \
            RayCollisionSystem.render_point(screen, point)
        rendering.RenderingSystem.schedule(4, render_lambda)


    @staticmethod
    def render_point(screen: pygame.Surface,
                     point):
        pygame.draw.circle(screen, (255, 100, 60), (int(point[0]), int(point[1])), 5)


    @staticmethod
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])


    @staticmethod
    def intersect(A, B, C, D):
        return RayCollisionSystem.ccw(A, C, D) != RayCollisionSystem.ccw(B, C, D) and \
               RayCollisionSystem.ccw(A, B, C) != RayCollisionSystem.ccw(A, B, D)


    @staticmethod
    @njit(fastmath=True)
    def calculate_collision_point(A, B, C, D):
        xdiff = (A[0] - B[0], C[0] - D[0])
        ydiff = (A[1] - B[1], C[1] - D[1])

        def det(a, b):
            return a[0] * b[1] - a[1] * b[0]

        div = det(xdiff, ydiff)
        if div == 0:
            raise Exception('lines do not intersect')
        d = (det(A, B), det(C, D))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return (x, y)
