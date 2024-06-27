from __future__ import annotations
import numpy as np
import moderngl as mgl
import pywavefront


class VBO:
    def __init__(self, ctx):
        self.vbos = {}
        self.vbos['cube'] = CubeVBO(ctx)

    def set_vbo(self, name: str, vbo: BaseVBO):
        self.vbos[name] = vbo

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]   


class BaseVBO:
    def __init__(self, ctx):
        self.ctx = ctx
        self.vbo = self.get_vbo()
        self.format: str | None = None
        self.attributes: list | None = None

    def get_vertex_data(self): ...

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo
    
    @staticmethod
    def get_tangent_data(pos: np.ndarray, normals: np.ndarray, uvs: np.ndarray):
        pos = pos.reshape([-1, 3, 3])
        normals = normals.reshape([-1, 3, 3])
        uvs = uvs.reshape([-1, 3, 2])
        tangents = []
        
        for positions, normals, uvs in zip(pos, normals, uvs):
            p1, p2, p3 = positions
            n1, n2, n3 = normals
            uv1, uv2, uv3 = uvs
            
            dUV1 = uv2 - uv1
            dUV2 = uv3 - uv1

            e1 = p2 - p1
            e2 = p3 - p1

            if (dUV1[0] * dUV2[1] - dUV2[0] * dUV1[1]) == 0:
                t1 = np.array([0, 0, 0], dtype="f4")
                t2 = np.array([0, 0, 0], dtype="f4")
                t3 = np.array([0, 0, 0], dtype="f4")
            else:
                f = 1 / (dUV1[0] * dUV2[1] - dUV2[0] * dUV1[1])

                t_flat = np.array([
                    f * (dUV2[1] * e1[0] - dUV1[1] * e2[0]),
                    f * (dUV2[1] * e1[1] - dUV1[1] * e2[1]),
                    f * (dUV2[1] * e1[2] - dUV1[1] * e2[2])
                ], dtype="f4")

                b1, b2, b3 = np.cross(t_flat, n1), np.cross(t_flat, n2), np.cross(t_flat, n3)
                t1, t2, t3 = np.cross(b1, n1), np.cross(b2, n2), np.cross(b3, n3)
            
            tangents.extend([t1, t2, t3])
        
        return np.array(tangents)

    def destroy(self):
        self.vbo.release()


class CubeVBO(BaseVBO):
    def __init__(self, ctx):
        super().__init__(ctx)
        self.format = '2f 3f 3f 3f'
        self.attributes = ['in_texcoord_0', 'in_normal', 'in_position', 'in_tangent']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]

        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        normals = [(0, 0, 1) * 6,
                   (1, 0, 0) * 6,
                   (0, 0, -1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        tangent_data = self.get_tangent_data(vertex_data, normals, tex_coord_data)

        vertex_data = np.hstack([normals, vertex_data])
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        vertex_data = np.hstack([vertex_data, tangent_data])
        return vertex_data


class ObjVBO(BaseVBO):
    def __init__(self, ctx, path: str):
        self.path = path
        super().__init__(ctx)
        self.format = '2f 3f 3f 3f'
        self.attributes = ['in_texcoord_0', 'in_normal', 'in_position', 'in_tangent']

    def get_vertex_data(self):
        objs = pywavefront.Wavefront(self.path, cache=True, parse=True)
        obj = objs.materials.popitem()[1]
        vertex_data = obj.vertices
        vertex_data = np.array(vertex_data, dtype='f4')
        vertex_data = np.split(vertex_data, len(vertex_data)//8)
        vertex_data = np.array(vertex_data, dtype='f4')
        texcoords, normals, positions = np.hsplit(vertex_data, [2, 5])
        tangents = self.get_tangent_data(positions, normals, texcoords)
        vertex_data = np.hstack([vertex_data, tangents])
        return vertex_data
