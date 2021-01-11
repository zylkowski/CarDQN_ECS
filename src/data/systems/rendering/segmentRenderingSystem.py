import data.components.segment as segment
from data.systems.rendering.renderingSystem import RenderingSystem
import pygame
import ecs


class SegmentRenderingSystem(ecs.System):

    def update(self, dt):
        for entity, segment_component in self.entity_manager.pairs_for_type(segment.SegmentComponent):

            try:
                segment_type = self.entity_manager.component_for_entity(entity, segment.SegmentTypeComponent)

                render_lambda = lambda screen, \
                                       seg_comp=segment_component, \
                                       seg_type=segment_type \
                    : SegmentRenderingSystem.renderSegment(screen, seg_comp, seg_type)

                RenderingSystem.schedule(1, render_lambda)

            except:
                pass

    @staticmethod
    def renderSegment(screen: pygame.Surface,
                      segmentComponent: segment.SegmentComponent,
                      segmentType: segment.SegmentTypeComponent):
        pygame.draw.line(screen, segmentType.type.value, segmentComponent.start, segmentComponent.end, 3)

    @staticmethod
    def renderSegment_2(screen: pygame.Surface,
                      color,
                      start,
                      end):
        pygame.draw.line(screen, color, start, end, 3)