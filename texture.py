import pygame as pg
import moderngl as mgl


class Texture:
    def __init__(self, ctx):
        self.ctx = ctx
        self.textures = {}

    def get_texture(self, path):
        if path in self.textures.keys():
            return self.textures[path]
        else:
            texture = pg.image.load(path).convert()
            texture = pg.transform.flip(texture, flip_x=False, flip_y=True)
            texture = self.ctx.texture(size=texture.get_size(), components=3,
                                    data=pg.image.tostring(texture, 'RGB'))
            
            # mipmaps
            texture.filter = (mgl.LINEAR_MIPMAP_LINEAR, mgl.LINEAR)
            texture.build_mipmaps()
            # AF
            texture.anisotropy = 32.0
            self.textures[path] = texture
            return texture

    def destroy(self):
        [tex.release() for tex in self.textures.values()]
