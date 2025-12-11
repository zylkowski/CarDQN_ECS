import ecs
import data.systems.game_state_system as game_state_system
from data.systems.DQNSystems.DQNActSystem import DQNActSystem
import data.components.DQNComponents as DQNComponents
import data.components.segment as segment
from ray_collision_system import RayCollisionSystem


class DQNRewardSystem(ecs.System):
    def __init__(self):
        super(DQNRewardSystem, self).__init__()
        self.timer = 0

    def update(self, dt):
        self.entity_manager: ecs.EntityManager

        game_state_system_instance = self.system_manager.get_system(game_state_system.GameStateSystem)
        if game_state_system_instance.MODE != game_state_system.GameModes.LEARNING:
            return

        self.timer += dt

        for entity, [DQNAgentData_component,
                     SegmentRayHolder_component] in self.entity_manager.pairs_for_types(DQNComponents.DQNAgentData,
                                                                               segment.SegmentRayHolder):
            DQNAgentData_component: DQNComponents.DQNAgentData
            SegmentRayHolder_component: segment.SegmentRayHolder
            # reward = 10
            action_index = DQNAgentData_component.action 
            # reward = 10 if DQNActSystem.ALL_ACTIONS[action_index][0] != 0 else 0
            reward = 0

            if self.detect_wall_collision(SegmentRayHolder_component):
                reward = -200
                DQNAgentData_component.reward = reward
                DQNAgentData_component.done = True
                self.timer = 0
                continue

            middle_ray_entity = DQNRewardSystem.get_entity_middle_ray(SegmentRayHolder_component)
            middle_ray_component = self.entity_manager.component_for_entity(middle_ray_entity,segment.SegmentRayComponent)

            middle_ray_segment_component = self.entity_manager.component_for_entity(middle_ray_entity,
                                                                                    segment.SegmentComponent)

            closest_checkpoint_collision, _, closest_collision_entity = \
                RayCollisionSystem.get_closest_ray_intersection(self.entity_manager,
                                                                middle_ray_segment_component,
                                                                middle_ray_component,
                                                                segment.SegmentTypes.CHECKPOINT)

            if closest_collision_entity not in DQNAgentData_component.passed_checkpoints and closest_collision_entity is not None:
                DQNAgentData_component.passed_checkpoints[closest_collision_entity] = self.timer
                time_since_last_checkpoint = self.timer-DQNAgentData_component.last_checkpoint_time
                reward += min(1e4/time_since_last_checkpoint,120)
                print(f"hit checkpoint, reward = {reward}")

                DQNAgentData_component.last_checkpoint_time = self.timer


            DQNAgentData_component.reward = reward
            DQNAgentData_component.done = False


    def detect_wall_collision(self, SegmentRayHolder_component):
        for ray in SegmentRayHolder_component.rays:
            ray_component: segment.SegmentRayComponent = self.entity_manager.component_for_entity(ray,
                                                                                                  segment.SegmentRayComponent)
            if ray_component.collision_distance < 0.05:
                return True


    @staticmethod
    def get_entity_middle_ray(SegmentRayHolder_component: segment.SegmentRayHolder):
        half_len = len(SegmentRayHolder_component.rays) / 2
        half_len = int(half_len)
        return SegmentRayHolder_component.rays[half_len]
