import pygame as pg


class TextureStorage:
    current_id = 0

    pathIDDictionary = {}
    textureStorage = {}

    @staticmethod
    def get_texture(texture_id):
        return TextureStorage.textureStorage[texture_id]

    @staticmethod
    def load_texture(texture_path):
        if TextureStorage.pathIDDictionary.__contains__(texture_path):
            return TextureStorage.pathIDDictionary[texture_path]
        else:
            TextureStorage.store_texture(texture_path)

            TextureStorage.current_id +=1
            return TextureStorage.current_id - 1

    @staticmethod
    def store_texture(texture_path):
        TextureStorage.pathIDDictionary[texture_path] = TextureStorage.current_id

        texture = pg.image.load(texture_path)
        texture.set_colorkey((255,255,255))

        TextureStorage.textureStorage[TextureStorage.current_id] = texture
