import math
import numpy as np


def vect_magnitude(vect):
    vec = vect[:]
    sums = 0
    for v in vec:
        sums += v**2
    sums = math.sqrt(sums)
    return sums


def scalar_mult(v, mult):
    vec = list(v[:])
    for x in range(len(vec)):
        vec[x] *= mult
    return vec


def vect_add(v1, v2):
    vec1 = list(v1[:])
    for i in range(len(vec1)):
        vec1[i] += v2[i]
    return vec1


def vect_diff(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]


def unit_vector(vec):
    dv = vect_magnitude(vec)
    if dv == 0:
        return [1, 0]
    return scalar_mult(vec, 1 / dv)


def y_lin_func(a, c, b, x):
    return a * (x - c) + b


def line_to_pos_and_unit_vect(a, c, b):
    rise = a
    run = 1
    pos = [c, b]
    v = [run, rise]
    uv = unit_vector(v)
    return pos, uv


def pos_and_vect_to_line(pos, vec):
    c, b = pos
    if vec[0] != 0:
        a = vec[1]/vec[0]
    else:
        a = 10000
    return [a, c, b]


def vect_angle(vec):
    return math.acos(unit_vector(vec)[0])


def vect_full_angle(v):  # 0 rad at [1, 0], increase counterclockwise until 2pi where returns to 0 at [1, 0].
    vec = unit_vector(v)
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
    """ Returns the angle in radians between given vectors"""
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


def between(c, rangelist, include_endpoints):
    ranges = rangelist[:]
    if ranges[0] > ranges[1]:
        ranges = [rangelist[1], rangelist[0]]
    if include_endpoints:
        if ranges[0] <= c <= ranges[1]:  # Change to <='s if you want endpoints to count
            return True
    else:
        if ranges[0] < c < ranges[1]:  # Change to <='s if you want endpoints to count
            return True
    return False


def ranges_intersect(range1, range2, include_endpoints=True):
    a1, a2 = range1
    if a2 < a1: # swap if improper range
        a1, a2 = a2, a1
    b1, b2 = range2
    if b2 < b1: # swap if improper range
        b1, b2 = b2, b1
    if include_endpoints:
        if b2 < a1 or a2 < b1:
            return False
        else:
            return True
    else:
        if b2 <= a1 or a2 <= b1:
            return False
        else:
            return True
