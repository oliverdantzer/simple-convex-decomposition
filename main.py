import pygame
import pygamedraw
import vmath
import vintersect
import math


def vector_intersects_vectors(pos, vec, point_array, vector_array):
    for i in range(len(vector_array)):
        if vintersect.vectors_intersect(pos, vec, point_array[i], vector_array[i], False):
            return True
    return False


def check_polygon(points, vectors):
    n = len(vectors)
    for i in range(0, n):
        for j in range(i + 1, n):
            # screen.fill((200, 200, 200))
            # pygamedraw.draw_points(screen, points)
            # pygamedraw.draw_vect(screen, points[i], vectors[i], (255, 0, 0))
            # pygamedraw.draw_vect(screen, points[j], vectors[j], (0, 0, 255))
            # pygame.display.flip()
            # pygame.time.delay(100 - i*n)
            if vintersect.vectors_intersect(points[i], vectors[i], points[j], vectors[j], False):
                # print(points[i], vectors[i], points[j], vectors[j])
                # print("NOT POLYGON")
                return False, (i, j)
            # else:
            #     print(points[i], vectors[i], points[j], vectors[j])
    return True, None


def polygon_vectors(polypoints):
    vecs = []
    n = len(polypoints)
    for i in range(n):
        if i == n - 1:
            vecs.append(vmath.vect_diff(polypoints[i], polypoints[0]))
        else:
            vecs.append(vmath.vect_diff(polypoints[i], polypoints[i + 1]))
    return vecs


def find_concave_points_idx(points, vecs):
    concave_points_idx = []

    n = len(points)

    min_idx = 0
    min_y = points[0][1]
    for i, val in enumerate(points):
        if val[1] < min_y:
            min_idx = i
            min_y = val[1]

    AB = vmath.vect_diff(points[min_idx], points[min_idx - 1])
    c = 0 if min_idx + 1 == n else min_idx + 1
    AC = vmath.vect_diff(points[min_idx], points[c])
    ABxAC = (AB[0] * AC[1]) - (AB[1] * AC[0])
    dir = -ABxAC / abs(ABxAC)

    for i in range(n):
        side = vmath.vects_side(vecs[i - 1], vecs[i])
        if side != dir and side != 0:
            concave_points_idx.append(i)

    return concave_points_idx


def find_first_concave_point_idx(vecs):
    dir = None
    n = len(vecs)
    for i in range(n):
        side = vmath.vects_side(vecs[i - 1], vecs[i])
        if dir == None:
            if side != 0:
                dir = side
        elif side != dir and side != 0:
            return i
    return None


def find_partition_point(point1_idx, point_array, vector_array):
    # point1 is starting point of partition
    v1 = vmath.vect_diff(point_array[point1_idx - 1], point_array[point1_idx])  # v1 is the vector from the point before point1 leading to point1
    # pygamedraw.draw_pointed_vect(screen, point_array[point1_idx - 1], v1, (127, 127, 0), 4)
    # v2 is vector from point1 leading to the next point
    if point1_idx != len(point_array) - 1:
        v2 = vmath.vect_diff(point_array[point1_idx], point_array[point1_idx + 1])
    else:
        v2 = vmath.vect_diff(point_array[point1_idx], point_array[0])
    # pygamedraw.draw_pointed_vect(screen, point_array[point1_idx], v2, (0, 127, 127), 4)
    # pygame.display.flip()
    dir12 = vmath.vects_side(v1, v2)  # dir is the side of v1 which v2 is on
    dir21 = vmath.vects_side(vmath.scalar_mult(v2, -1), vmath.scalar_mult(v1, -1))
    i = point1_idx + 2
    if i > len(point_array) - 1:
        i -= len(point_array)
    while i != point1_idx:
        # pygamedraw.draw_line_segment(screen, point_array[point1_idx], point_array[i], (255, 0, 0))
        # pygame.display.flip()
        # pygame.time.delay(10000)
        v = vmath.vect_diff(point_array[point1_idx], point_array[i])
        side1 = vmath.vects_side(v1, v)  # side of v1 which v is on
        side2 = vmath.vects_side(vmath.scalar_mult(v2, -1), v)
        if (not (side1 == dir12 and side2 == dir21)) and (side1 != 0 and side2 != 0):
            if not vector_intersects_vectors(point_array[point1_idx], v, point_array, vector_array):
                # pygamedraw.draw_line_segment(screen, point_array[point1_idx], point_array[i], (0, 255, 0))
                # pygame.display.flip()
                # pygame.time.delay(1000)
                return i
        # else:
        #     print("side1 != dir12", side1 != dir12)
        #     print("side2 != dir21", side2 != dir21)
            # pygame.time.delay(3000)
        # else:

        if i != len(point_array) - 1:
            i += 1
        else:
            i = 0
    return None


def partition_lists(lis, range):
    if range[1] < range[0]:
        # partition 1
        p1 = lis[range[0]:]
        p1.extend(lis[:range[1] + 1])

        # partition 2
        p2 = lis[range[1]:range[0] + 1]
    else:
        # partition 1
        p1 = lis[range[0]:range[1] + 1]

        # partition 2
        p2 = lis[range[1]:]
        p2.extend(lis[:range[0] + 1])

    return [p1, p2]


def init_screen_and_clock():
    global screen, display, clock, window_size
    pygame.init()
    window_size = (1150, 640)
    pygame.display.set_caption('Game')
    screen = pygame.display.set_mode(window_size, 0, 32)
    clock = pygame.time.Clock()


class Polygon:
    def __init__(self, points_array, pos, mass=1, vel=[0, 0], colour=[0, 0, 0], is_polygon=None):
        self.points_array = points_array
        self.pos = pos
        self.mass = mass
        self.vel = vel
        self.colour = colour
        self.vectors_array = polygon_vectors(points_array)
        self.is_polygon, self.bad_vecs = check_polygon(self.points_array, self.vectors_array)


    def draw(self):
        for i in range(len(self.points_array)):
            color = (0, 0, 0)
            if not self.is_polygon and i in self.bad_vecs:
                color = (0, 255, 0)
            pygamedraw.draw_vect(screen, self.points_array[i], self.vectors_array[i], color)


def decompose_to_convex(p):
    concave_points_idx = find_concave_points_idx(p.points_array, p.vectors_array)
    if not concave_points_idx:
        return None
    for point in concave_points_idx:
        point_1 = point
        point_2 = find_partition_point(point, p.points_array, p.vectors_array)
        if point_2 != None:
            break
    if point_2 == None:
        return None
    points_lists = partition_lists(p.points_array, [point_1, point_2])

    p1, p2 = Polygon(points_lists[0], p.pos, is_polygon=True), Polygon(points_lists[1], p.pos, is_polygon=True)
    # return get_convex_polygons(p1), get_convex_polygons(p2)
    return p1, p2

def get_convex_polys(p):
    poly_list = [p]
    i = 0
    while i < len(poly_list):
        # print(i)
        decomp = decompose_to_convex(poly_list[i])
        if decomp == None:
            # print("convex")
            poly_list[i].draw()
            pygame.display.flip()
            i += 1
        else:
            del poly_list[i]
            poly_list.insert(i, decomp[0])
            poly_list.insert(i + 1, decomp[1])
    return poly_list



def main_loop():
    points = []
    making = True

    first = True

    loop = True

    while loop:
        dt = clock.tick(100) / 1000

        fps = int(clock.get_fps())
        screen.fill((200, 200, 200))
        pygamedraw.draw_text(screen, str(fps), (0, 0))
        # [446, 446][101, -149][440, 280][114, 172]
        # [353, 384][334, -145][750, 321][-397, 63]
        mouse_pos = list(pygame.mouse.get_pos())
        # vecs = [353, 384], [334, -145], [750, 321], [-397, 63]
        # pygamedraw.draw_vect(screen, vecs[0], vecs[1])
        # pygamedraw.draw_vect(screen, vecs[2], vecs[3])
        # print(vintersect.vectors_intersect(vecs[0], vecs[1], vecs[2], vecs[3], False))
        # pygamedraw.draw_vect(screen, [300,300], vmath.vect_diff([300,300], [mouse_pos[0], mouse_pos[1]]))
        # print(vintersect.vectors_intersect([446, 446], [101, -149], [300,300], vmath.vect_diff([300,300], [mouse_pos[0], mouse_pos[1]]), False))

        # pygamedraw.draw_line_segment(screen, [300,300], [mouse_pos[0], mouse_pos[1]])
        # v = vmath.vect_diff([300,300], [mouse_pos[0], mouse_pos[1]])
        mouse_down = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_down = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    making = False
                    p1 = Polygon(points, [0, 0])
                    # print(p1.is_polygon)
                    # if not p1.is_polygon:
                    #     print("not polygon")
        if making:
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
            pygamedraw.draw_text(screen, "Please draw a simple polygon", (window_size[0] / 2, 10))
            pygamedraw.draw_text(screen, "(A polygon that does not intersect itself)", (window_size[0] / 2.2, 40))
            if mouse_down:
                points.append(mouse_pos)
            pygamedraw.draw_points(screen, points)
        if not making:
            if p1.is_polygon:
                if first:
                    poly_list = get_convex_polys(p1)
                    # concave_points_idx = find_concave_points_idx(p1.points_array, p1.vectors_array)
                    # print(concave_points_idx)
                    first = False

                for p in poly_list:
                    p.draw()
                if len(poly_list) == 1:
                    pygamedraw.draw_text(screen, "Try drawing a concave polygon", (window_size[0] / 2, 10))
                pygamedraw.draw_square(screen, [window_size[0] - 210, window_size[1] - 50], 200, 40)
                pygamedraw.draw_text(screen, "DRAW AGAIN", [window_size[0] - 190, window_size[1] - 50])
                if vmath.between(mouse_pos[0], [window_size[0] - 210, window_size[0] - 10], True) and vmath.between(mouse_pos[1], [window_size[1] - 50, window_size[1] - 10], True):
                    pygame.mouse.set_cursor(*pygame.cursors.diamond)
                    if mouse_down:
                        main_loop()
                        break
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)


            else:
                pygamedraw.draw_text(screen, "Not a simple polygon. Try again...", (window_size[0] / 2, 10))
                pygame.display.flip()
                pygame.time.delay(1000)
                main_loop()
                break


        pygame.display.flip()


init_screen_and_clock()

# print(partition_lists([0,1,2,3,4,5,6,7,8,9], [3,7]))
# print(partition_lists([0,1,2,3,4,5,6,7,8,9], [3,7]))
# print(partition_lists([0,1,2,3,4,5,6,7,8,9], [3,7]))
# print(partition_lists([0,1,2,3,4,5,6,7,8,9], [3,7]))
# print(partition_lists([0,1,2,3,4,5,6,7,8,9], [3,7]))

main_loop()

pygame.quit()
# print("Game over")
