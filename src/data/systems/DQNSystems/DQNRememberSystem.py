from data.components.DQNComponents.DQNAgent import DQNAgentData
import ecs
from data.systems.DQNSystems.DQNStateUpdateSystem import DQNStateUpdateSystem
# from data.systems.DQNSystems.DQNStateUpdateSystem import DQ
import data.systems.game_state_system as game_state_system
import data.components.DQNComponents as DQNComponents
import data.components.car_control as car_control


class DQNRememberSystem(ecs.System):
    BATCH_SIZE = 1024
    MAX_LIFETIME = 6000
    EPISODE = 0
    REWARD_SUM = 0

    def update(self, dt):
        self.entity_manager: ecs.EntityManager

        game_state_system_instance = self.system_manager.get_system(game_state_system.GameStateSystem)
        if game_state_system_instance.MODE != game_state_system.GameModes.LEARNING:
            return

        DQNStateUpdateSystem.set_DQN_state(self.entity_manager, True)

        for entity, [DQNAgent_component,
                     DQNAgentData_component,
                     _] in self.entity_manager.pairs_for_types(DQNComponents.DQNAgent,
                                                                           DQNComponents.DQNAgentData,
                                                                           car_control.CarControllerComponent):
            DQNAgent_component: DQNComponents.DQNAgent
            DQNAgentData_component: DQNComponents.DQNAgentData

            DQNAgentData_component.lifetime += 1

            
            to_remember = DQNAgentData_component.get_data_to_remember()
            DQNRememberSystem.REWARD_SUM += to_remember[2]
            DQNAgent_component.remember(to_remember)
            if DQNAgentData_component.done or DQNAgentData_component.lifetime > DQNRememberSystem.MAX_LIFETIME:
                DQNRememberSystem.EPISODE += 1
                print(f"Episode: {DQNRememberSystem.EPISODE} Epsilon: {DQNAgent_component.EPSILON:.3}, Reward sum: {DQNRememberSystem.REWARD_SUM }")
                self.system_manager.get_system(DQNStateUpdateSystem).revert_starting_position(entity)
                DQNAgentData_component.passed_checkpoints = {}
                DQNAgentData_component.last_checkpoint_time = 0
                DQNRememberSystem.REWARD_SUM = 0 
                DQNAgent_component.replay(DQNRememberSystem.BATCH_SIZE)
                if DQNRememberSystem.EPISODE % 100 == 0:
                    DQNAgent_component.save(DQNRememberSystem.EPISODE)
