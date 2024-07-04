from vbo import BaseVBO
from shader_program import ShaderProgram


class VAO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.program = ShaderProgram(ctx)
        self.vaos = {}

    def get_vao(self, program, vbo):
        vao = self.ctx.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attributes)])
        return vao
    
    def set_vao(self, vbo: BaseVBO, name: str, program: str):
        self.vaos[name] = self.get_vao(
            program=self.program.get_program(program),
            vbo=vbo)

    def destroy(self):
        for vao in self.vaos.values():
            vao.release()
        self.program.destroy()