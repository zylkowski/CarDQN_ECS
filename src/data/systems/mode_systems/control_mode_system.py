import ecs
import pygame as pg
import data.systems.game_state_system as game_state_system
import data.components.car_control as car_control


class ControlModeSystem(ecs.System):
    def update(self, dt):
        self.entity_manager: ecs.EntityManager

        game_state_system_instance = self.system_manager.get_system(game_state_system.GameStateSystem)
        if game_state_system_instance.MODE == game_state_system.GameModes.CONTROL:
            events = game_state_system_instance.EVENTS

            for entity, [_,
                         car_control_component] in self.entity_manager.query([car_control.PlayerControlTag,
                                                                              car_control.CarControllerComponent]):
                for event in events:
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_a: car_control_component.steering = 1
                        if event.key == pg.K_d: car_control_component.steering = -1

                        if event.key == pg.K_w: car_control_component.gas = 1
                        if event.key == pg.K_s: car_control_component.gas = -1
                    if event.type == pg.KEYUP:
                        if event.key == pg.K_a or event.key == pg.K_d: car_control_component.steering = 0
                        if event.key == pg.K_w or event.key == pg.K_s: car_control_component.gas = 0
