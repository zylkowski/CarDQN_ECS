import ecs
import data.systems.game_state_system as game_state_system
import data.components.DQNComponents as DQNComponents
import data.components.car_control as car_control
import itertools
import torch
import numpy as np

class DQNActSystem(ecs.System):
    GAS_ACTIONS = [0,1]
    STEER_ACTIONS = [-1,0,1]
    ALL_ACTIONS = list(itertools.product(GAS_ACTIONS,STEER_ACTIONS))


    def update(self, dt):
        self.entity_manager : ecs.EntityManager

        game_state_system_instance = self.system_manager.get_system(game_state_system.GameStateSystem)
        if game_state_system_instance.MODE != game_state_system.GameModes.LEARNING:
            return

        for entity, [DQNAgent_component,
                     DQNAgentData_component,
                     CarControl_component] in self.entity_manager.pairs_for_types(DQNComponents.DQNAgent,
                                                                           DQNComponents.DQNAgentData,
                                                                                  car_control.CarControllerComponent):
            DQNAgent_component: DQNComponents.DQNAgent
            DQNAgentData_component: DQNComponents.DQNAgentData
            CarControl_component: car_control.CarControllerComponent

            action_index = DQNAgent_component.act(DQNAgentData_component.state)
            DQNAgentData_component.action = action_index

            CarControl_component.gas = DQNActSystem.ALL_ACTIONS[action_index][0]
            CarControl_component.steering = DQNActSystem.ALL_ACTIONS[action_index][1]
