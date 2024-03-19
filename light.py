import glm


class Light:
    def __init__(self, position=(3, 3, -3), color=(1, 1, 1), intensity=1):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        self.intensity = intensity * self.color
