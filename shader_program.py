

class ShaderProgram:
    def __init__(self, ctx):
        self.ctx = ctx

    def get_program(self, shader_program_name):
        if shader_program_name in self.programs.keys():
            return self.programs[shader_program_name]
        with open(f'shaders/{shader_program_name}.vert') as f:
            vertex_shader = f.read()

        with open(f'shaders/{shader_program_name}.frag') as f:
            fragment_shader = f.read()

        program = self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        self.programs[shader_program_name] = program
        return program

    def destroy(self):
        [program.release() for program in self.programs.values()]