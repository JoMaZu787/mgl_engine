import pygame as pg


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {0: self.get_texture(path='textures/img.png'), 1: self.get_texture(path='textures/img_1.png'),
                         2: self.get_texture(path='textures/img_2.png'), "2_n": self.get_texture(path='textures/img_2_n.png')}

    def get_texture(self, path):
        texture = pg.image.load(path).convert()
        texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.ctx.texture(size=texture.get_size(), components=3,
                                   data=pg.image.tostring(texture, 'RGB'))
        return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
