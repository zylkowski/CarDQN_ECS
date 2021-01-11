import ecs
import pygame as pg
from enum import Enum
from abc import ABCMeta, abstractmethod
import six


class GameModes(Enum):
    EDITOR = 0
    CONTROL = 1
    LEARNING = 2


class KeyEvent:
    key = None

    @staticmethod
    def handle_event(event,key_event):
        key_event.idle()
        if event.key == key_event.key:
            if event.type == pg.KEYDOWN:
                print(f"{key_event.key} is down")
                key_event.on_key_down()
            elif event.type == pg.KEYUP:
                print(f"{key_event.key} is up")
                key_event.on_key_up()
        pass

    @abstractmethod
    def on_key_up(self):
        pass

    @abstractmethod
    def on_key_down(self):
        pass

    @abstractmethod
    def idle(self):
        pass


class GameStateSystem(ecs.System):
    def __init__(self):
        super(GameStateSystem, self).__init__()

        self.QUIT = False
        self.MODE = GameModes.CONTROL
        self.EVENTS = None

    def update(self, dt):
        current_events = pg.event.get()
        self.EVENTS = current_events

        for event in current_events:
            if event.type == pg.QUIT:
                self.QUIT = True
            if event.type == pg.KEYDOWN or event.type == pg.KEYUP:
                if event.key == pg.K_F1:
                    self.MODE = GameModes.CONTROL
                if event.key == pg.K_F2:
                    self.MODE = GameModes.EDITOR
                if event.key == pg.K_F3:
                    self.MODE = GameModes.LEARNING
