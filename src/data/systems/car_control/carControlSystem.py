import ecs
from data.components import car_control
import data.components.physics as physics
import numpy as np
import math


class CarControlSystem(ecs.System):
    def update(self, dt):
        self.entity_manager: ecs.EntityManager
        for entity, control_component in self.entity_manager.pairs_for_type(car_control.CarControllerComponent):
            control_component: car_control.CarControllerComponent

            try:
                rot_component: physics.Rotation = \
                    self.entity_manager.component_for_entity(entity, physics.Rotation)
                vel_component: physics.Velocity = \
                    self.entity_manager.component_for_entity(entity, physics.Velocity)

                rot_component.rotation += dt * \
                                          control_component.steering * \
                                          control_component.max_angular_speed * \
                                          CarControlSystem.sigmoid(vel_component.magnitude())

                if control_component.gas != 0:
                    new_velocity = (control_component.gas * control_component.max_speed, 0)
                    vel_component.vel = CarControlSystem.rotate(new_velocity,degrees= 90 - rot_component.rotation)
                    control_component.last_steering = control_component.gas
                else:
                    new_velocity = (control_component.last_steering * vel_component.magnitude(), 0)
                    vel_component.vel = CarControlSystem.rotate(new_velocity,degrees= 90 - rot_component.rotation)

                if vel_component.magnitude() > control_component.speed_falloff * control_component.speed_falloff:
                    dir_vec = np.divide(-vel_component.vel,vel_component.magnitude())
                    falloff = np.multiply(dir_vec,control_component.speed_falloff)
                    vel_component.vel += falloff
                else:
                    vel_component.vel = np.array((0,0))

            except:
                print("carControlSystem error")
                pass

    @staticmethod
    def rotate(p, origin=(0, 0), degrees=0):
        angle = np.deg2rad(degrees)
        R = np.array([[np.cos(angle), -np.sin(angle)],
                      [np.sin(angle), np.cos(angle)]])
        o = np.atleast_2d(origin)
        p = np.atleast_2d(p)
        return np.squeeze((R @ (p.T - o.T) + o.T).T)

    @staticmethod
    def rotate_vector(vector, angle):
        radians = math.radians(angle)
        return (vector[0] * math.cos(radians) - vector[1] * math.sin(radians),
            vector[0] * math.sin(radians) + vector[1] * math.cos(radians))


    @staticmethod
    def sigmoid(x):
        return 2 / (1 + math.exp(-x)) - 1
