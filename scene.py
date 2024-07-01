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
        add = self.add_object

        self.add_object(model.Cube(app, tex_path="textures/img_2.png", normal_tex_path="textures/img_2_n.png" , pos=(0, 0, 0)))

        #add(model.Cube(app))
        #add(model.Cube(app, tex_id=1, pos = (-2.5, 0, 0), rot=(45, 0, 0), scale=(1, 2, 1)))
        #add(model.Cube(app, tex_id=2, pos = (2.5, 0, 0), rot=(0, 0, 45), scale=(1, 1, 2)))
        #add(model.Cube(app, tex_id=3, pos = (0, 5, 0), rot=(0, 0, 0), scale=(2, 2, 2)))

    def render(self):
        for obj in self.objects:
            obj.render()

