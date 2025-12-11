import pygame as py
import ecs

class RenderingSystem(ecs.System):
    queue = {}
    every_frame_queue = {}
    fill_color = (0,0,0)

    def __init__(self, surface : py.Surface):
        super(RenderingSystem, self).__init__()
        self.screen = surface

    def update(self, dt):
        self.screen.fill(self.fill_color)

        self.schedule_every_frame_items()
        keys = list(RenderingSystem.queue.keys())
        keys.sort()
        try:
            if keys is not None:
                for key in keys:
                    for function in RenderingSystem.queue[key]:
                        function(self.screen)
        except:
            pass

        RenderingSystem.queue.clear()

        py.display.flip()

    def schedule_every_frame_items(self):
        for tag in RenderingSystem.every_frame_queue:
            order,function = RenderingSystem.every_frame_queue[tag]
            RenderingSystem.schedule(order,function)

    @staticmethod
    def schedule(order, function):
        if order not in RenderingSystem.queue:
            RenderingSystem.queue[order] = []
        RenderingSystem.queue[order].append(function)

    @staticmethod
    def schedule_every_frame(tag, order, function):
        RenderingSystem.every_frame_queue[tag] = (order, function)

    @staticmethod
    def deschedule_every_frame(tag):
        RenderingSystem.every_frame_queue.pop(tag)
