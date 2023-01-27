import pygame
import pygame.gfxdraw
import numpy as np
import vmath
import math


def draw_line_segment(surface, start_pos: vmath.Vector, end_pos: vmath.Vector, color=(0, 0, 0), width=1):
    """ Draws wide transparent anti-aliased lines. """
    # ref https://stackoverflow.com/a/30599392/355230

    x0, y0 = start_pos.to_float_list()
    x1, y1 = end_pos.to_float_list()
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
    x, y = pos.to_float_list()
    pygame.gfxdraw.aacircle(screen, int(x), int(y), int(r), color)


def draw_line(screen, pos, vec, color=(255, 0, 0)):
    line = vmath.LinearFunc(vec.slope(), pos[1], pos[0])
    draw_line_segment(screen,
                      (0,  line.f(0)),
                      (1150,  line.f(1150)),
                      color,
                      10)


def draw_vect(screen, pos: vmath.Vector, vec: vmath.Vector, color=pygame.Color(0, 0, 0), size=2):
    draw_line_segment(screen, pos, pos + vec, color, size)


def draw_points_polygon(screen, point_array):
    n = len(point_array)
    if n == 0:
        pass
    elif n == 1:
        draw_circle(screen, point_array[0], 1)
    else:
        for i in range(0, n - 1):
            draw_line_segment(screen, point_array[i], point_array[i + 1])
        draw_line_segment(screen, point_array[n - 1], point_array[0])


def draw_text(screen, text_to_show, pos, size=30, fontcolor=(0, 0, 0), aa=True):
    screen.blit(pygame.font.SysFont("Arial", size).render(str(text_to_show), aa, fontcolor), pos)

class FadingText:
    def __init__(self, text, pos, current_time, decay_time=1000):
        self.text = text
        self.pos = pos
        self.beginning_time = current_time
        self.decay_time = decay_time



class FadingTextSurface:
    def __init__(self, screen):
        self.screen = screen
        self.fading_text_array = []
    

    def add_fading_text(self, text, pos, current_time, decay_time=3000):
        self.fading_text_array.append(FadingText(text, pos, current_time, decay_time))
    

    def update(self, current_time):
        for fading_text in self.fading_text_array:
            # draw_text(self.screen, fading_text.text, fading_text.pos, fontcolor=(255, 0, 0, 255 - 255 * ((current_time - fading_text.beginning_time) / fading_text.decay_time) ))
            draw_text(self.screen, fading_text.text, fading_text.pos, fontcolor=(255, 0, 0))
        for fading_text in self.fading_text_array:
            if fading_text.beginning_time + fading_text.decay_time <= current_time:
                self.fading_text_array.remove(fading_text)

                
    


def draw_pointed_vect(screen, pos, vec, color=(0, 0, 0), width=1):
    width *= 0.03
    p1 = pos + vec

    pbetween = p1 + (-0.2 * vec)
    draw_line_segment(screen, pos, pbetween, color, vec.magnitude() * width * (2/3))
    p2 = pbetween + (width * vmath.Vector([-vec[1], vec[0]]))

    p3 = pbetween + (width * vmath.Vector([vec[1], -vec[0]]))
    for l in [p1, p2, p3]:
        for i in [0, 1]:
            l[i] = int(l[i])
    pygame.gfxdraw.filled_trigon(screen, p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], color)


def draw_square(screen, pos, width, height, color=(0, 0, 0)):
    pygame.gfxdraw.aapolygon(screen, [pos, [pos[0] + width, pos[1]], [pos[0] + width, pos[1] + height], [pos[0], pos[1] + height]], color)