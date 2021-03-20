import ecs
import pygame as pg
import data.components.segment as segment
import data.systems.rendering as rendering
import data.systems.game_state_system as game_state_system
from data.systems.entity_spawner_system import EntitySpawnerSystem
from enum import Enum
import map_saver


class EditorTools(Enum):
    WALL = "Wall"
    CHECKPOINT = "Checkpoint"
    MOVE_CAR = "Move car (use arrow keys)"
    ROTATE_CAR = "Rotate car (use arrow keys)"

pg.font.init()

class EditorSystem(ecs.System):
    def __init__(self):
        super().__init__()

        self.FONT = pg.font.SysFont('Arial', 30)
        self.CURRENT_TOOL = EditorTools.WALL

        self.segment_start = None

    def update(self, dt):
        self.system_manager : ecs.SystemManager
        game_state_system_instance = self.system_manager.get_system(game_state_system.GameStateSystem)

        if game_state_system_instance.MODE == game_state_system.GameModes.EDITOR:

            rendering.RenderingSystem.schedule(0, EditorSystem.render_background)
            rendering.RenderingSystem.schedule(3, self.render_current_tool)

            events = game_state_system_instance.EVENTS

            for event in events:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        self.CURRENT_TOOL = EditorTools.WALL
                    if event.key == pg.K_2:
                        self.CURRENT_TOOL = EditorTools.CHECKPOINT
                    if event.key == pg.K_3:
                        self.CURRENT_TOOL = EditorTools.ROTATE_CAR
                    if event.key == pg.K_4:
                        self.CURRENT_TOOL = EditorTools.MOVE_CAR
                    if event.key == pg.K_RETURN:
                        map_saver.MapSaver.save_current_map(self.entity_manager)

                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        print(f"msb down = {self.segment_start}")
                        if self.segment_start is None:
                            print("setting seg start")
                            self.segment_start = pg.mouse.get_pos()
                            print(f"seg_start = {self.segment_start}")
                        else:
                            if self.CURRENT_TOOL == EditorTools.WALL:
                                mouse_pos = pg.mouse.get_pos()
                                print("spawning")
                                EntitySpawnerSystem.spawn_segment(segment.SegmentTypes.WALL, self.segment_start,
                                                                  mouse_pos)
                                self.segment_start = mouse_pos
                            elif self.CURRENT_TOOL == EditorTools.CHECKPOINT:
                                EntitySpawnerSystem.spawn_segment(segment.SegmentTypes.CHECKPOINT,
                                                                  self.segment_start,
                                                                  pg.mouse.get_pos())
                                self.segment_start = None
                    if event.button == 3:
                        self.segment_start = None


            if self.segment_start is not None:
                render_lambda = lambda screen,\
                                       color = (50,255,50),\
                                       start = self.segment_start,\
                                       end = pg.mouse.get_pos() \
                                        :rendering.SegmentRenderingSystem.renderSegment_2(screen,color,start,end)
                rendering.RenderingSystem.schedule(3,render_lambda)

    def render_current_tool(self,screen):
        text_surface = self.FONT.render(self.CURRENT_TOOL.value, False, (0,0,0))
        screen.blit(text_surface,(0,0))

    @staticmethod
    def render_background(screen):
        screen.fill((150, 150, 150))
