import ecs
from data.components.texture_rendering.TextureStorage import TextureStorage


class TextureComponent(ecs.Component):
    def __init__(self, texture_path: str):
        self.textureID = TextureStorage.load_texture(texture_path= texture_path)

    def get_texture(self):
        return TextureStorage.get_texture(self.textureID)

class TextureScale(ecs.Component):
    def __init__(self, scale):
        self.scale = scale
