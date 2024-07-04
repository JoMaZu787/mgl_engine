import model


class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app

        self.add_object(model.ObjModel(app, vao_name="cat", tex_path="textures/img_2.png", normal_tex_path="textures/img_2_n.png", path="objects/cat/20430_Cat_v1_NEW.obj" , pos=(0, 0, 0)))

        #add(model.Cube(app))
        #add(model.Cube(app, tex_id=1, pos = (-2.5, 0, 0), rot=(45, 0, 0), scale=(1, 2, 1)))
        #add(model.Cube(app, tex_id=2, pos = (2.5, 0, 0), rot=(0, 0, 45), scale=(1, 1, 2)))
        #add(model.Cube(app, tex_id=3, pos = (0, 5, 0), rot=(0, 0, 0), scale=(2, 2, 2)))

    def render(self):
        for obj in self.objects:
            obj.render()

