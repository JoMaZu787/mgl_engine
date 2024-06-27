from vbo import VBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = VBO(ctx)
        self.program = ShaderProgram(ctx)
        self.vaos = {}

        # cube vao
        self.set_vao('cube', 'default')

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attributes)])
        return vao
    
    def set_vao(self, name: str, program: str):
        self.vaos[name] = self.get_vao(
            program=self.program.programs[program],
            vbo=self.vbo.vbos[name])

    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()