import pygame
import pygame.gfxdraw
import vmath
import math


def draw_line_segment(surface, start_pos, end_pos, color=(0, 0, 0), width=1):
    """ Draws wide transparent anti-aliased lines. """
    # ref https://stackoverflow.com/a/30599392/355230

    x0, y0 = start_pos
    x1, y1 = end_pos
    midpnt_x, midpnt_y = (x0+x1)/2, (y0+y1)/2  # Center of line segment.
    length = math.sqrt((x1-x0)**2 + (y1-y0)**2)
    angle = math.atan2(y0-y1, x0-x1)  # Slope of line.
    width2, length2 = width/2, length/2
    sin_ang, cos_ang = math.sin(angle), math.cos(angle)

    width2_sin_ang  = width2*sin_ang
    width2_cos_ang  = width2*cos_ang
    length2_sin_ang = length2*sin_ang
    length2_cos_ang = length2*cos_ang

    # Calculate box ends.
    ul = (midpnt_x + length2_cos_ang - width2_sin_ang,
          midpnt_y + width2_cos_ang  + length2_sin_ang)
    ur = (midpnt_x - length2_cos_ang - width2_sin_ang,
          midpnt_y + width2_cos_ang  - length2_sin_ang)
    bl = (midpnt_x + length2_cos_ang + width2_sin_ang,
          midpnt_y - width2_cos_ang  + length2_sin_ang)
    br = (midpnt_x - length2_cos_ang + width2_sin_ang,
          midpnt_y - width2_cos_ang  - length2_sin_ang)

    pygame.gfxdraw.aapolygon(surface, (ul, ur, br, bl), color)
    pygame.gfxdraw.filled_polygon(surface, (ul, ur, br, bl), color)


def draw_circle(screen, pos, r, color=(255, 0, 0)):
    pygame.gfxdraw.aacircle(screen, pos[0], pos[1], r, color)


def draw_line(screen, starting, vec, color=(255, 0, 0)):
    slope = vmath.unit_vector(vec)[0]
    draw_line_segment(screen,
                      (0,  vmath.y_lin_func(slope, starting[0], starting[1], 0)),
                      (1150,  vmath.y_lin_func(slope, starting[0], starting[1], 1150)),
                      color,
                      10)


def draw_vect(screen, pos, vec, color=(0, 0, 0)):
    draw_line_segment(screen, pos, vmath.vect_add(pos, vec), color, 5)


def draw_points(screen, points):
    n = len(points)
    if n == 0:
        pass
    elif n == 1:
        draw_line_segment(screen, points[0], vmath.vect_add(points[0], [1, 1]))
    else:
        for i in range(0, n - 1):
            draw_line_segment(screen, points[i], points[i + 1])
        draw_line_segment(screen, points[n - 1], points[0])


def draw_text(screen, text_to_show, pos, size=30, fontcolor=(0, 0, 0), aa=True):
    screen.blit(pygame.font.SysFont("Arial", size).render(text_to_show, aa, fontcolor), pos)


def draw_pointed_vect(screen, pos, vec, color=(0, 0, 0), width=1):
    width *= 0.03
    p1 = vmath.vect_add(pos, vec)

    pbetween = vmath.vect_add(p1, vmath.scalar_mult(vec, -0.2))
    draw_line_segment(screen, pos, pbetween, color, vmath.vect_magnitude(vec) * width * (2/3))
    p2 = vmath.vect_add(pbetween, vmath.scalar_mult([-vec[1], vec[0]], width))

    p3 = vmath.vect_add(pbetween, vmath.scalar_mult([vec[1], -vec[0]], width))
    for l in [p1, p2, p3]:
        for i in [0, 1]:
            l[i] = int(l[i])
    pygame.gfxdraw.filled_trigon(screen, p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], color)


def draw_square(screen, pos, width, height, color=(0, 0, 0)):
    pygame.gfxdraw.aapolygon(screen, [pos, [pos[0] + width, pos[1]], [pos[0] + width, pos[1] + height], [pos[0], pos[1] + height]], color)