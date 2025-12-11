import ecs
import data.components.DQNComponents as DQNComponents
import data.systems.game_state_system as game_state_system
import data.components.segment as segment
import data.components.physics as physics
import data.components.car_control as control
import torch
import numpy as np


class DQNStateUpdateSystem(ecs.System):
    def __init__(self):
        super(DQNStateUpdateSystem, self).__init__()
        self.first_loop= True
        self.starting_entity_manager = None
        self.starting_system_manager = None

    def update(self, dt):
        self.entity_manager: ecs.EntityManager
        self.system_manager: ecs.SystemManager

        game_state_system_instance = self.system_manager.get_system(game_state_system.GameStateSystem)
        if game_state_system_instance.MODE == game_state_system.GameModes.LEARNING:
            if self.first_loop:
                for entity, [DQNAgentData_component,
                             Position_component,
                             Rotation_component] in self.entity_manager.pairs_for_types(DQNComponents.DQNAgentData,
                                                             physics.Position,
                                                             physics.Rotation):
                    DQNAgentData_component : DQNComponents.DQNAgentData
                    Position_component: physics.Position
                    Rotation_component: physics.Rotation

                    DQNAgentData_component.starting_position = Position_component.pos
                    DQNAgentData_component.starting_rotation = Rotation_component.rotation

                self.first_loop = False

            DQNStateUpdateSystem.set_DQN_state(self.entity_manager)

    def revert_starting_position(self,entity):
        self.entity_manager: ecs.EntityManager
        Position_component = self.entity_manager.component_for_entity(entity, physics.Position)
        Rotation_component = self.entity_manager.component_for_entity(entity, physics.Rotation)
        Velocity_component: physics.Velocity = self.entity_manager.component_for_entity(entity, physics.Velocity)
        DQNAgentData_component: DQNComponents.DQNAgentData = self.entity_manager.component_for_entity(entity, DQNComponents.DQNAgentData)

        DQNAgentData_component.done = False
        DQNAgentData_component.lifetime = 0

        Velocity_component.vel = [0,0]
        Position_component.pos = DQNAgentData_component.starting_position
        Rotation_component.rotation = DQNAgentData_component.starting_rotation


    @staticmethod
    def set_DQN_state(entity_manager: ecs.EntityManager, update_next_state=False):
        try:
            for DQNEntity, DQNAgentData_component in entity_manager.pairs_for_type(DQNComponents.DQNAgentData):

                DQNAgentData_component: DQNComponents.DQNAgentData
                ray_holder: segment.SegmentRayHolder = entity_manager.component_for_entity(DQNEntity,
                                                                                           segment.SegmentRayHolder)
                vel_component: physics.Velocity = entity_manager.component_for_entity(DQNEntity,
                                                                                      physics.Velocity)
                controler_component: control.CarControllerComponent = entity_manager.component_for_entity(DQNEntity,
                                                                                      control.CarControllerComponent)
                rot_component: physics.Rotation = entity_manager.component_for_entity(DQNEntity,
                                                                                      physics.Rotation)

                state = []
                for ray_entity in ray_holder.rays:
                    ray_component: segment.SegmentRayComponent = entity_manager.component_for_entity(
                        ray_entity, segment.SegmentRayComponent)
                    state.append(ray_component.collision_distance)

                state.append((vel_component.vel[0] + controler_component.max_speed)/(2*controler_component.max_speed))
                state.append((vel_component.vel[1] + controler_component.max_speed)/(2*controler_component.max_speed))
                state.append((rot_component.rotation % 360)/360)
                state = DQNStateUpdateSystem.state_to_pytorch(state)

                if update_next_state:
                    DQNAgentData_component.next_state = state
                else:
                    DQNAgentData_component.state = state

        except:
            pass

    @staticmethod
    def state_to_pytorch(state):
        return torch.from_numpy(np.reshape(state, [-1, len(state)])).float()
