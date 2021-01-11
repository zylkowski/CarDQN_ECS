import data.components.texture_rendering as texture_rendering
import data.components.physics as physics
from data.systems.rendering.renderingSystem import RenderingSystem
import pygame
import ecs


class TextureRenderingSystem(ecs.System):
    def update(self, dt):
        for entity, textureComponent in self.entity_manager.pairs_for_type(texture_rendering.TextureComponent):

            try:
                pos = self.entity_manager.component_for_entity(entity, physics.Position)
                try:
                    rot = self.entity_manager.component_for_entity(entity, physics.Rotation)
                except:
                    rot = None
                try:
                    scale = self.entity_manager.component_for_entity(entity, texture_rendering.TextureScale)
                except:
                    scale = None

                RenderingSystem.schedule(2,
                                         lambda screen, pos=pos, rot=rot, scale=scale: self.render(screen,
                                                                                                   textureComponent.get_texture(),
                                                                                                   pos,
                                                                                                   rot,
                                                                                                   scale))
            except:
                print("TextureRenderingSystem error")
                pass

    def render(self, screen: pygame.Surface,
               texture: pygame.Surface,
               pos,
               rot: physics.Rotation,
               scale: texture_rendering.TextureScale):

        if rot is not None:
            texture = pygame.transform.rotate(texture, rot.rotation)
        if scale is not None:
            texture = pygame.transform.scale(texture, (int(texture.get_width() * scale.scale),
                                                       int(texture.get_height() * scale.scale)))

        rect = texture.get_rect()
        rect.center = pos.pos
        screen.blit(texture, rect)
