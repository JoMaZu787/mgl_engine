import pygame as pg
import moderngl as mgl
import sys
import model
from camera import Camera
from light import Light
from mesh import Mesh
from scene import Scene


class GraphicsEngin:
    def __init__(self, win_size=(1600, 900)):
        # init pygame modules
        pg.init()
        # window size
        self.WIN_SIZE = win_size
        # set opengl attr
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 4)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE, flags=pg.OPENGL | pg.DOUBLEBUF)
        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use existing opengl context
        self.ctx = mgl.create_context()
        self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE)
        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # light
        self.light = Light(intensity=2)
        # camera
        self.camera = Camera(self)
        # mesh
        self.mesh = Mesh(self)
        # scene
        self.scene = Scene(self)

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                self.mesh.destroy()
                pg.quit()
                sys.exit()

    def render(self):
        self.ctx.clear(color=(0.08, 0.16, 0.18, 1.0))

        self.scene.render()

        pg.display.flip()

    @staticmethod
    def get_time():
        return pg.time.get_ticks()*0.001

    def run(self):
        while True:
            self.time = self.get_time()
            self.check_events()
            self.camera.update()
            pg.mouse.set_pos(pg.Vector2(pg.display.get_surface().get_size())/2)
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == "__main__":
    app = GraphicsEngin()
    app.run()
