import polygon
import pygamedraw
import vmath

class Polygon():
    def get_bounds(self):
        self.top_left = []
        self.bottom_right = []
        print("p:", self.p.point_array)
        for i in (0, 1):
            minimum = min(self.p.point_array, key=lambda point:point[i])[i]
            maximum = max(self.p.point_array, key=lambda point:point[i])[i]
            self.top_left.append(minimum)
            self.bottom_right.append(maximum)
    
    def __init__(self, p: polygon.Polygon):
        self.p = p
        self.position = vmath.Vector([0, 0])
        self.size = 1
        self.get_bounds()
    
    def transform(self, transform_vector: vmath.Vector = vmath.Vector([0, 0])):
        new_point_array = []
        for point in self.p.point_array:
            new_point_array.append(point + transform_vector)
        self.p = polygon.Polygon(new_point_array)
        self.get_bounds()
    
    def set_top_left(self, top_left_vector: vmath.Vector = vmath.Vector([0, 0])):
        tl = vmath.Vector(self.top_left)
        transform_vector = top_left_vector - tl
        self.transform(transform_vector)

    # scale across dimension (0 or 1) relative to minimum point in dimension
    def scale_dim(self, dim: int = 1, scale_multiplier: float = 1.0, relative_to: list[vmath.Decimal] | None = None):
        if relative_to == None:
            relative_to = self.top_left
        
        if dim not in (0, 1):
            raise ValueError("dim can be 0 or 1")
        new_point_array = []
        for point in self.p.point_array:
            if dim == 0:
                new_point_array.append(vmath.Vector([ (point[0] - relative_to[0]) * scale_multiplier + relative_to[0] , point[1]]))
            if dim == 1:
                new_point_array.append(vmath.Vector([point[0], (point[1] - relative_to[1]) * scale_multiplier + relative_to[1] ]))
        self.p = polygon.Polygon(new_point_array)
        self.get_bounds()
    
    def scale(self, scale_multiplier: float = 1.0, relative_to: list[vmath.Decimal] | None = None):
        for i in (0, 1):
            self.scale_dim(i, scale_multiplier, relative_to)
    
    def draw(self, screen):
        self.p.draw(screen)
    

class ConvexPolygonGroup():
    def get_bounds(self):
        self.top_left = []
        self.bottom_right = []
        print("tltype: ", type(self.poly_array[0].top_left[0]))
        for i in (0, 1):
            minimum = min(self.poly_array, key=lambda p:p.top_left[i]).top_left[i]
            maximum = max(self.poly_array, key=lambda p:p.bottom_right[i]).top_left[i]
            self.top_left.append(minimum)
            self.bottom_right.append(maximum)

    
    def __init__(self, cpg: polygon.Polygon):
        self.poly_array = [Polygon(cp.sp.p) for cp in cpg.group]
        self.position = vmath.Vector([0, 0])
        self.size = 1
        self.get_bounds()
    
    def transform(self, transform_vector: vmath.Vector = vmath.Vector([0, 0])):
        for p in self.poly_array:
            p.transform(transform_vector)
        self.get_bounds()

    def set_top_left(self, top_left_vector: vmath.Vector = vmath.Vector([0, 0])):
        tl = vmath.Vector(self.top_left)
        transform_vector = top_left_vector - tl
        self.transform(transform_vector)

    # scale across dimension (0 or 1) relative to minimum point in dimension
    def scale_dim(self, dim: int = 1, scale_multiplier: float = 1.0):
        for p in self.poly_array:
            p.scale_dim(dim, scale_multiplier, self.top_left)
        self.get_bounds()
    
    def scale(self, scale_multiplier: float = 1.0):
        for i in (0, 1):
            self.scale_dim(i, scale_multiplier)
    
    def draw(self, screen):
        for p in self.poly_array:
            p.draw(screen)
