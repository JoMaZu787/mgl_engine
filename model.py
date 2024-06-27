import glm


class BaseModel:
    def __init__(self, app, vao_name, tex_id, pos = glm.vec3(0, 0, 0), rot = glm.vec3(0, 0, 0), scale=glm.vec3(1, 1, 1)):
        self.app = app
        self.pos = pos
        self.rot = glm.vec3([glm.radians(a) for a in rot])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.tex_id = tex_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, self.rot.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rot.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rot.z, glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, self.scale)
        return m_model

    def render(self):
        self.update()
        self.vao.render()


class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', tex_id=0, pos = glm.vec3(0, 0, 0), rot = glm.vec3(0, 0, 0), scale = glm.vec3(1, 1, 1)):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        self.texture = None
        self.normal_texure = None
        self.on_init()

    def update(self):
        self.program['u_texture_0'] = 0
        self.texture.use(0)
        self.program['n_texture_0'] = 1
        self.normal_texure.use(1)
        self.program['m_model'].write(self.m_model)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['camPos'].write(self.app.camera.position)

    def on_init(self):
        # texture
        self.texture = self.app.mesh.texture.textures[self.tex_id]

        if self.tex_id == 2:
            self.normal_texure = self.app.mesh.texture.textures["2_n"]
        
        # mvp
        self.program['m_proj'].write(self.app.camera.m_proj)
        self.program['m_view'].write(self.app.camera.m_view)
        self.program['m_model'].write(self.m_model)
        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.intensity'].write(self.app.light.intensity)
        # material
        self.program['material.Ka'].write(glm.vec3(1.0))
        self.program['material.Kd'].write(glm.vec3(1.0))
        self.program['material.Ks'].write(glm.vec3(1.0))


class OBJ(BaseModel):
    def __init__(self, app, vao_name, tex_id, pos = glm.vec3(0, 0, 0), rot = glm.vec3(0, 0, 0), scale=glm.vec3(1, 1, 1), filename: str):
        super().__init__(app, vao_name, tex_id, pos, rot, scale)
        
        self.on_init()