import ecs
from data.systems.DQNSystems.DQNStateUpdateSystem import DQNStateUpdateSystem
# from data.systems.DQNSystems.DQNStateUpdateSystem import DQ
import data.systems.game_state_system as game_state_system
import data.components.DQNComponents as DQNComponents
import data.components.car_control as car_control


class DQNRememberSystem(ecs.System):
    BATCH_SIZE = 512
    MAX_LIFETIME = 6000

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

            DQNAgentData_component.lifetime += dt

            DQNAgent_component.remember(DQNAgentData_component.get_data_to_remember())
            if DQNAgentData_component.done or DQNAgentData_component.lifetime > DQNRememberSystem.MAX_LIFETIME:
                self.system_manager.get_system(DQNStateUpdateSystem).revert_starting_position(entity)
                DQNAgent_component.replay(DQNRememberSystem.BATCH_SIZE)
