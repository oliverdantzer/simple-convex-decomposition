from __future__ import annotations # Allows hinting the return of a method with the type of the enclosing class. This call must happen before all the other imports.
from typing import Union
import math
# from decimal import *
import decimal
import numpy as np
import sys


class Decimal:
    def __init__(self, val):
        if isinstance(val, Decimal):
            self.val = val.val
        else:
            self.val = decimal.Decimal(val)
    
    def to_float(self):
        return float(self.val)
    
    def __str__(self):
        return str(self.val)
    
    def __add__(self, other: Decimal) -> Decimal:
        return Decimal(self.val + other.val)
    
    def __sub__(self, other: Decimal) -> Decimal:
        return Decimal(self.val - other.val)
    
    def __mul__(self, other: Decimal | float) -> Decimal:
        if type(other) == float:
            return Decimal(float(self.val) * other)
        return Decimal(self.val * other.val)
    
    def __rmul__(self, other: Decimal | float) -> Decimal:
        return self * other
    
    def __truediv__(self, other: Decimal) -> Decimal:
        return Decimal(self.val / other.val)
    
    def __pow__(self, pow: int) -> Decimal:
        return Decimal(self.val**pow)
    
    def __eq__(self, other: Decimal) -> bool:
        if isinstance(other, Decimal):
            return between(self.val, [other.val - decimal.Decimal(0.000001), other.val + decimal.Decimal(0.000001)])
        # elif type(other) in (float, int, decimal.Decimal)
    
    def __lt__(self, other: Decimal) -> bool:
        return self.val < other.val
    
    def __gt__(self, other: Decimal) -> bool:
        return self.val > other.val
    
    def __le__(self, other: Decimal) -> bool:
        return self < Decimal(other.val + decimal.Decimal(0.000001))
    
    def __ge__(self, other: Decimal) -> bool:
        return self > Decimal(other.val - decimal.Decimal(0.000001))
    
    def sqrt(self) -> Decimal:
        return Decimal(self.val.sqrt())
    
    def inv(self) -> Decimal:
        return Decimal(decimal.Decimal(1.0) / self.val)


def sign(x: float) -> int:
    return -1 if x < 0 else 1


def mod(x: float, n: int):
    return sign(x) * (abs(x) % n)


class Angle:
    def __init__(self, theta: float) -> None:
        """
        Restricts angle to range (-pi, pi]
        """
        theta = mod(theta, 2 * math.pi)
        if abs(theta) > math.pi:
            theta += -2 * sign(theta) * math.pi
        if theta == -math.pi:
            theta *= -1
        self.theta = theta
    
    def __str__(self):
        return str(self.theta)

    def __add__(self, other: Angle) -> Angle:
        return Angle(self.theta + other.theta)
    
    def __sub__(self, other: Angle) -> Angle:
        return Angle(self.theta - other.theta)
    
    def __eq__(self, other: Angle) -> bool:
        return self.theta == other.theta
    
    def __lt__(self, other: Angle) -> bool:
        return self.theta < other.theta
    
    def __gt__(self, other: Angle) -> bool:
        return self.theta > other.theta
    
    def to_float(self):
        return self.theta



class Side:
    def __init__(self, angle: Angle | float | int):
        if type(angle) in (float, int):
            if angle < 0:
                self.dir = -1
            elif angle == 0:
                self.dir = 0
            else:
                self.dir = 1
        elif type(angle) == Angle:
            if angle.theta == math.pi:
                self.dir = 0
            elif angle.theta == 0:
                self.dir = 0
            elif angle.theta < 0:
                self.dir = -1
            elif angle.theta > 0:
                self.dir = 1
        else:
            raise TypeError("angle must be Angle or int")

    def __eq__(self, other: Side):
        return self.dir in (0, other.dir)
    
    def __repr__(self):
        return str(self.dir)
    


class Vector:
    def __init__(self, v: list[float]) -> None:
        d = []
        for x in v: 
            d.append(Decimal(x))
        self.v = np.array(d)
    
    def __repr__(self):
        res = "["
        if len(self) == 0:
            return res
        for i in range(len(self) - 1):
            res += str(self[i]) + ", "
        res += str(self[len(self) - 1]) + "]"
        return res
    
    def __getitem__(self, index):
        return self.v[index]
    
    def __len__(self):
        return len(self.v)

    def __eq__(self, other: Vector) -> bool:
        if not isinstance(other, Vector):
            return False
        if len(self) != len(other):
            return False
        for i in range(len(self)):
            if self[i] != other[i]:
                return False
        return True
    
    def __add__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            raise TypeError("Addition between vector and non-vector is not defined")
        if len(self) != len(other):
            raise ValueError("Vectors must have equal dimension to be added")
        v = []
        for i in range(len(self)):
            v.append(self[i] + other[i])
        return Vector(v)
    
    def __sub__(self, other: Vector) -> Vector:
        if not isinstance(other, Vector):
            raise TypeError("Subtraction between vector and non-vector is not defined")
        if len(self) != len(other):
            raise ValueError("Vectors must have equal dimension to be added")
        v = []
        for i in range(len(self)):
            v.append(self[i] - other[i])
        return Vector(v)
    
    def __mul__(self, other: Decimal) -> Vector:
        k = Decimal(other)
        v = []
        for x in self:
            v.append(k * x)
        return Vector(v)

    def magnitude(self) -> Decimal:
        sum = Decimal(0)
        for x in self:
            sum += x**2
        return sum.sqrt()
    
    def unit_vector(self) -> Vector:
        dv = self.magnitude()
        if dv == 0:
            return Vector([1, 0])
        return Vector(self * (dv.inv()))
    
    def slope(self) -> Decimal:
        if self[0] == Decimal(0):
            print("inf")
            return math.inf
        return self[1] / self[0]
    
    def angle(self) -> Angle:
        """
        Returns angle of vector
        """
        return Angle(math.acos(self.unit_vector()[0].to_float()) * (1 if self[1] < Decimal(0) else -1))
    
    def angle_relative_to(self, other: Vector) -> Angle:
        return self.angle() - other.angle()
    
    def side_relative_to(self, other: Vector) -> Side:
        return Side(self.angle_relative_to(other))
    
    def to_float_list(self) -> list[float]:
        return [x.to_float() for x in self]
    
    # let pos self and v2 be at tip of v1. is self on same side of v1 and v2 as the given side? side.dir = -1 or 1
    def side_of_angle(self, v1: Vector, v2: Vector, side: Side) -> bool:
        side = side.dir
        if side == 1:
            pass
        elif side == -1:
            pass
        else:
            raise ValueError("Side must be 1 or -1")
        self_relative_angle = self.angle() - v1.angle()
        v2_relative_angle = v2.angle() - v1.angle()
        if v2_relative_angle < self_relative_angle < Angle(math.pi):
            return -1 == side
        else:
            return 1 == side


class LinearFunc:
    def __init__(self, a: Decimal, b: Decimal, c: Decimal) -> None:
        self.a = a
        self.b = b - a * c

    def __eq__(self, other: LinearFunc) -> bool:
        if not isinstance(other, LinearFunc):
            return False
        return self.a == other.a and self.b == other.b

    def f(self, x: Decimal) -> Decimal:
        return self.a * x + self.b
    
    def inversef(self, y: Decimal) -> Decimal:
        return (y - self.b) / self.a
    
    def intersects(self, other: LinearFunc) -> bool:
        if (self.a == other.a):
            if not self.b == other.b:
                return False
        return True

    @staticmethod
    def intersection_point(line1: LinearFunc, line2: LinearFunc) -> Vector | None:
        if not line1.intersects(line2):
            return None
        if line1 == line2:
            return Vector([0, line1.f(0)])
        # a1 * x + b1 = a2 * x + b2
        # b1 - b2 = a2 * x - a1 * x
        # (b1 - b2) / (a2 - a1) = x
        intersect_x = (line1.b - line2.b) / (line2.a - line1.a)
        intersect_y = line1.f(intersect_x)
        return Vector([intersect_x, intersect_y])

def between(c, range) -> bool:
    a = range[0]
    b = range[1]
    if a > b:
        a, b = b, a
    return a <= c and c <= b

class XyRange:
    def __init__(self, xrange, yrange):
        self.xrange = xrange
        self.yrange = yrange
    
    def contains_point(self, point: Vector) -> bool:
        return between(point[0], self.xrange) and between(point[1], self.yrange)


def ranges_intersect(r1: list, r2: list) -> bool:
    if r1[0] > r1[1]:
        r1 = [r1[1], r1[0]]
    if r2[0] > r2[1]:
        r2 = [r2[1], r2[0]]
    # return true if there is point c such that r1[0] <= c <= r1[1] and r2[0] <= c <= r2[1]
    if r1[0] <= r2[1] and r2[0] <= r1[1]:
        return True
    else:
        return False


def inline_vectors_intersect(pos1: Vector, v1: Vector, pos2: Vector, v2: Vector):
    v1_relative_magnitude = v1.magnitude()
    if v1.unit_vector() != v2.unit_vector(): # if unit vectors are inequal, then they point opposite directions, so one of them is negative
        v1_relative_magnitude *= -1
    v2_relative_pos = pos2 - pos1
    if pos1.unit_vector() != pos2.unit_vector():  # if position vectors aren't in same direction, they are in opposite quadrants, one is negative
        v2_relative_pos *= -1
    return ranges_intersect([0, v1_relative_magnitude], [v2_relative_pos.magnitude(), v2_relative_pos.magnitude() + v2.magnitude()])


# Function f of form f(x) = a(x - c) + b
class VectorLinearFunc:
    def __init__(self, pos: Vector, vec: Vector) -> None:
        if vec == Vector([0, 0]):
            self.type = "Point"
            self.pos = pos
            self.range = XyRange([pos[0], pos[0]], [pos[1], pos[1]])  # [rangex, rangey]
        elif vec[0] == Decimal(0):
            self.type = "Vertical"
            self.posx = pos[0]
            self.range = XyRange([pos[0], pos[0]], [pos[1], pos[1] + vec[1]])  # y range is not well-formed
        else:
            self.type = "Line"
            self.pos = pos
            self.vec = vec
            self.line = LinearFunc(vec.slope(), pos[1], pos[0])
            self.range = XyRange([pos[0], pos[0] + vec[0]], [pos[1], pos[1] + vec[1]])
    
    def __eq__(self, other: VectorLinearFunc) -> bool:
        if self.type != other.type:
            return False
        if self.type == "Point":
            return self.pos == other.pos
        if self.type == "Vertical":
            return self.posx == other.posx
        if self.type == "Line":
            return self.line == self.line

    def f(self, x: Decimal) -> Decimal:
        if self.type != "Line":
            raise ValueError("f method cn only be called when type == line")
        return self.line.f(x)
    
    @staticmethod
    def intersect(v1: VectorLinearFunc, v2: VectorLinearFunc) -> Vector | None:
        types = (v1.type, v2.type)

        # Line, point
        if "Line" in types and "Point" in types:
            if v1.type != "Line":
                v2, v1 = v1, v2
            return v2.pos == Vector([v2.pos[0], v1.f(v2.pos[0])]) and v1.range.contains_point(v2.pos)
        
        # Line, line
        if types == ("Line", "Line"):
            intersection_point = LinearFunc.intersection_point(v1.line, v2.line)
            if intersection_point == None:
                return False
            if v1.line == v2.line:
                return inline_vectors_intersect(v1.pos, v1.vec, v2.pos, v2.vec)
            return v1.range.contains_point(intersection_point) and v2.range.contains_point(intersection_point)
        
        # Line, Vertical
        if "Line" in types and "Vertical" in types:
            if v1.type != "Line":
                v2, v1 = v1, v2
            intersection_point = Vector([v2.posx, v1.f(v2.posx)])
            return v1.range.contains_point(intersection_point) and v2.range.contains_point(intersection_point)
        
        # Point, point
        if types == ("Point", "Point"):
            return v1.pos == v2.pos
        
        # Point, vertical
        if "Point" in types and "Vertical" in types:
            if v1.type != "Point":
                v2, v1 = v1, v2
            return v2.range.contains_point(v1.pos)
        
        # Vertical, vertical
        if types == ("Vertical", "Vertical"):
            return v1.posx == v2.posx and ranges_intersect(v1.range.yrange, v2.range.yrange)

"""
def vect_full_angle(v):  # 0 rad at [1, 0], increase counterclockwise until 2pi where returns to 0 at [1, 0].
    vec = v.unit_vector()
    angle = math.acos(vec[0])
    if vec[1] < 0:

        angle = 2 * math.pi - angle
        # angle *= -1
    return 2*math.pi - angle


def v2_angle_relative_to_v1(v1, v2):
    a1 = vect_full_angle(v1)
    a2 = vect_full_angle(v2)
    a2 -= a1
    if a2 < 0:
        a2 += 2 * math.pi
    return a2


def vects_side(v1, v2):  # which side of v1 is v2 on
    angle_between = v2_angle_relative_to_v1(v1, v2)
    if 0 < angle_between < math.pi:
        return -1
    elif 0 < angle_between < 2 * math.pi:
        return 1
    else:
        return 0


def angle_between_vectors(vector1, vector2):
    # Returns the angle in radians between given vectors
    v1_u = unit_vector(vector1)
    v2_u = unit_vector(vector2)
    minor = np.linalg.det(
        np.stack((v1_u[-2:], v2_u[-2:]))
    )
    if minor == 0:
        raise NotImplementedError('Too odd vectors =(')
    return np.sign(minor) * np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


def angle_mag_to_vec(angle, magnitude):
    return [math.cos(angle)*magnitude, math.sin(angle)*magnitude]

"""


if __name__ == "__main__":
    # print(Vector([0.0000001, 0.00000000000001]) == Vector([0.0000001, 0.000000001]))
    # print(Vector([0.0000001, 0.9999999999999999]) == Vector([0.0000001, 1]))
    # print(between(10, [9,11]))
    print("vmath")
    print(Vector([1, 1]).side_relative_to(Vector([2, 1])))
    print(Vector([1, 1]) in [Vector([1, 3]), Vector([1, 2])])