import ecs
import pygame as pg
import data.components.physics as physics
import data.systems.physics as physics_s
import data.systems.rendering as rendering
import data.systems.car_control as car_control_s
import data.systems.mode_systems as mode_systems
import data.systems.game_state_system as game_state_system
import data.systems.DQNSystems as DQNSystems
from data.systems.entity_spawner_system import EntitySpawnerSystem
from rayPositionUpdateSystem import RayPositionUpdateSystem
from ray_collision_system import RayCollisionSystem
import map_saver
import data.constants


class Window:
    def __init__(self, window_size, window_title):
        self.surface = pg.display.set_mode(window_size)
        pg.display.set_caption(window_title)


class Game:
    pg.init()
    pg.font.init()

    def __init__(self):
        self.entityManager = ecs.EntityManager()
        self.systemManager = ecs.SystemManager(self.entityManager)

        self.WINDOW = Window(data.constants.SCREEN_SIZE, data.constants.WINDOW_TITLE)
        self.clock = pg.time.Clock()

        self.add_systems_to_world()
        if data.constants.MAP_PATH.exists():
            print("loading")
            map_saver.MapSaver.load_map(data.constants.MAP_PATH.__str__())
        else:
            EntitySpawnerSystem.spawn_car_entity(physics.Position((500, 500)),
                                                 physics.Rotation(0),
                                                 data.constants.CAR_TEXTURE_PATH)

    
    def add_systems_to_world(self):
        self.systemManager.add_system(EntitySpawnerSystem())

        self.systemManager.add_system(game_state_system.GameStateSystem())
        self.systemManager.add_system(mode_systems.EditorSystem())
        self.systemManager.add_system(mode_systems.ControlModeSystem())

        self.systemManager.add_system(DQNSystems.DQNStateUpdateSystem())
        self.systemManager.add_system(DQNSystems.DQNActSystem())

        self.systemManager.add_system(car_control_s.CarControlSystem())
        self.systemManager.add_system(physics_s.VelocitySystem())
        self.systemManager.add_system(RayPositionUpdateSystem())
        self.systemManager.add_system(RayCollisionSystem())

        self.systemManager.add_system(DQNSystems.DQNRewardSystem())
        self.systemManager.add_system(DQNSystems.DQNRememberSystem())

        self.systemManager.add_system(rendering.TextureRenderingSystem())
        self.systemManager.add_system(rendering.SegmentRenderingSystem())
        self.systemManager.add_system(rendering.RenderingSystem(self.WINDOW.surface))



    def start_game_loop(self):
        game_state_quit = False
        while not game_state_quit:
            game_state_quit = self.systemManager.get_system(game_state_system.GameStateSystem).QUIT
            dt = self.clock.tick(60)
            self.update(dt)

    def update(self,dt):
        self.systemManager.update(dt)
