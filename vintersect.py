import vmath
# import pygamedraw


def closest_point_on_line(line_vec, line_pos, point_pos):
    if line_vec[0] == 0:
        line_vec[0] = 0.00001
    if line_vec[1] == 0:
        line_vec[1] = 0.00001
    # assume circ2 is static
    # we have line_pos, line_vec, and point_pos
    # let p be the closest point on velocity line to circle
    # turn self vel and pos into equation of y and x: slope = rise/run
    line_slope = line_vec[1] / line_vec[0]
    # draw_line(line_pos, line_vec, (0, 255, 0))
    # y = line_slope(x - line_pos[0]) + line_pos[1]
    # line perpendicular to self will have slope:
    point_slope = -1 / line_slope
    # draw_line(point_pos, [1, point_slope], (0, 255, 0))
    # line going through circ2:
    # y = point_slope(x - point_pos[0]) + point_pos[1]
    # intersection will be p
    # line_slope(p_x - line_pos[0]) + line_pos[1] = point_slope(p_x - point_pos[0]) + point_pos[1]
    # line_slope*p_x - line_slope*line_pos[0]=point_slope*p_x- point_slope*point_pos[0] + point_pos[1] - line_pos[1]
    # line_slope*p_x -point_slope*p_x=-point_slope*point_pos[0] + point_pos[1] - line_pos[1] +line_slope*line_pos[0]
    # (line_slope-point_slope)*p_x = line_slope*line_pos[0] - point_slope*point_pos[0] + point_pos[1] - line_pos[1]
    p_x = (line_slope * line_pos[0] - point_slope * point_pos[0] + point_pos[1] - line_pos[1]) / (
            line_slope - point_slope)
    p_y = point_slope * (p_x - point_pos[0]) + point_pos[1]
    p = [p_x, p_y]
    # pygame.draw.circle(screen, (255, 0, 0), p, 20)
    return p


def find_intersection_lines(line1, line2):
    a1, c1, b1 = line1
    a2, c2, b2 = line2
    # a(x - c) + b = ax - ac + b = ax + (b - ac)
    if a1 == a2:
        if (b1 - a1 * c1) == (b2 - a2 * c2):
            return True, [c1, b1], "all"
        else:
            return False, 0, "none"

    # a1 * x + (b1 - a1 * c1) = a2 * x + (b2 - a2 * c2)
    # a1 * x - a2 * x  =  (b2 - a2 * c2) - (b1 - a1 * c1)
    # (a1 - a2) * x  =  b2 - a2 * c2 - b1 + a1 * c1
    x_0 = (a1 * c1 - a2 * c2 + b2 - b1) / (a1 - a2)
    y_0 = a1 * (x_0 - c1) + b1
    return True, [x_0, y_0], "unique"


def collinear_vectors_intersect(pos1, v1, pos2, v2, include_endpoints):
    v1_mag = vmath.vect_magnitude(v1)
    v2_mag = vmath.vect_magnitude(v2)
    if vmath.unit_vector(v1) == vmath.scalar_mult(vmath.unit_vector(v2), -1): # if vectors are opposite instead of same direction, one of them is negative
        v2_mag *= -1
    v1_distance = vmath.vect_magnitude(pos1)
    v2_distance = vmath.vect_magnitude(pos2)
    if vmath.unit_vector(pos1) == vmath.scalar_mult(vmath.unit_vector(pos2), -1):  # if position vectors aren't in same direction, on of them is negative (in opposite quadrant)
        print("other side of quadrants")
        v2_distance *= -1
    v2_start = v2_distance - v1_distance
    v2_end = v2_start + v2_mag
    # print([0, v1_mag], [v2_start, v2_end])
    return vmath.ranges_intersect([0, v1_mag], [v2_start, v2_end], include_endpoints)


def collinear_point_in_vector(point_pos, v_pos, vec, include_endpoints):
    v_pos_to_point_pos = vmath.vect_diff(v_pos, point_pos)  # Vector from start of vec to position of point
    dist_from_v_pos_to_point_pos = vmath.vect_magnitude(v_pos_to_point_pos)  # Distance of point along start of vector
    vec_mag = vmath.vect_magnitude(vec)
    if dist_from_v_pos_to_point_pos == 0 or vmath.between(dist_from_v_pos_to_point_pos, [vec_mag - vec_mag*0.0001, vec_mag + vec_mag*0.0001], False):
        return include_endpoints
    if v_pos_to_point_pos[0] * vec[0] + v_pos_to_point_pos[1] * vec[1] < 0:
        return False
    if dist_from_v_pos_to_point_pos < vmath.vect_magnitude(vec):
        return True
    else:
        return False


def vectors_intersect(pos1, v1, pos2, v2, include_endpoints):

    intersect_result = find_intersection_lines(vmath.pos_and_vect_to_line(pos1, v1), vmath.pos_and_vect_to_line(pos2, v2))
    if intersect_result[0] is False:
        return False
    else:
        if intersect_result[2] == "all":
            if collinear_vectors_intersect(pos1, v1, pos2, v2, include_endpoints):
                return True
            else:
                return False
        else:
            intersection = intersect_result[1]
            intersect = [False, False]
            if collinear_point_in_vector(intersection, pos1, v1, include_endpoints):
                intersect[0] = True
            if collinear_point_in_vector(intersection, pos2, v2, include_endpoints):
                intersect[1] = True
            if intersect[0] and intersect[1]:
                return True
            return False


def line_intersects_vector(posline, vline, posvec, vvec):
    intersect_result = find_intersection_lines(vmath.pos_and_vect_to_line(posline, vline), vmath.pos_and_vect_to_line(posvec, vvec))
    if intersect_result[0] is False:
        return False
    else:
        if intersect_result[2] == "all":
            return True
        else:
            intersection = intersect_result[1]
            intersect = [False, False]
            if collinear_point_in_vector(intersection, posvec, vvec, 1):
                return True

# print(vectors_intersect([325, 472], [13, -267], [346, 205], [-21, 267], True))
# print(vectors_intersect([0, 0], [1, 1], [1, 1], [1, 1], True))
# print(vectors_intersect([508, 409], [0, 102], [508, 511], [50, -65], True))