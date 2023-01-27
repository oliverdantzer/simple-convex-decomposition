from __future__ import annotations # Allows hinting the return of a method with the type of the enclosing class. This call must happen before all the other imports.
import pygame
import pygamedraw
import vmath
import numpy as np
import polygon
import polygontransform

# initialize pygame, pygame display, and global variables
pygame.init()
clock = pygame.time.Clock()
window_size = (800, 600)  # pygame display window size
bg_color = (230, 230, 230)  # display background color
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('simple-convex-decomposition')
ft_surface = pygamedraw.FadingTextSurface(screen)  # fading text surface to attach temporary messages to


# allows user to draw points on polygon, displays points as they are drawing
# return:
#   polygon.Polygon - polygon containing the point the user has drawn
#   pygame.QUIT - if the user presses exit on the window
def making_polygon() -> polygon.Polygon | pygame.QUIT:
    point_array: list[vmath.Vector] = []  # list to store point of polygon in
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return pygame.QUIT
            
            # if mouse button down, append point at position of mouse to point_array
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                # if last point in point_array is equal to the current mouse position, don't current mouse position to point_array. Otherwise, add it
                if len(point_array) > 0:
                    if point_array[len(point_array) - 1] != vmath.Vector(mouse_pos):
                        point_array.append(vmath.Vector(mouse_pos))
                else:
                    point_array.append(vmath.Vector(mouse_pos))
            
            # if return key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    p = polygon.Polygon(point_array)
                    # if not 3 points or more drawn, don't continue
                    if len(point_array) < 3:
                        ft_surface.add_fading_text("A polygon must have at least 3 sides", (window_size[0] / 2 - 200, window_size[1] - 40), pygame.time.get_ticks())
                    
                    # if user drawn polygon is not a simple polygon, restart polygon drawing
                    elif not p.is_simple():
                        ft_surface.add_fading_text("The polygon drawn was not a simple polygon", (window_size[0] / 2 - 220, window_size[1] - 70), pygame.time.get_ticks())
                        # for v in point_array:
                        #     print(v)
                        point_array = []
                    
                    # continue by returning drawn polygon
                    else:
                        return p
        
        screen.fill(bg_color)

        # pygamedraw.draw_text(screen, str(int(clock.get_fps())), (0, 0))  # Display fps (avg of s^-1 between last 10 ticks)
        ft_surface.update(pygame.time.get_ticks())  # update fading text so it can fade over time

        # display informative text
        pygamedraw.draw_text(screen, "Please draw a simple polygon", (window_size[0] / 2, 10))
        pygamedraw.draw_text(screen, "(A polygon where its sides do not intersect each other)", (window_size[0] / 3.9, 40))
        pygamedraw.draw_text(screen, "Left-click to add vertex, return key to finalize", (window_size[0] / 2.6, 70), fontcolor=(0, 200, 0))

        # display user-drawn polygon
        pygamedraw.draw_points_polygon(screen, point_array)
 
        pygame.display.flip()  # update contents of entire display
        clock.tick()  # tick clock


def displaying_polygon(original: polygon.Polygon, cpg: polygon.ConvexPolygonsGroup) -> pygame.QUIT | None:
    o = polygontransform.Polygon(original)
    p = polygontransform.ConvexPolygonGroup(cpg)
    o.scale(0.4)
    o.set_top_left(vmath.Vector([window_size[0] * 0.05, window_size[1] * 0.3]))
    p.scale(0.4)
    p.set_top_left(vmath.Vector([window_size[0] * 0.55, window_size[1] * 0.3]))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return pygame.QUIT

            # if space key pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
        screen.fill(bg_color)

        # pygamedraw.draw_text(screen, str(int(clock.get_fps())), (0, 0))  # Display fps (avg of s^-1 between last 10 ticks)
        ft_surface.update(pygame.time.get_ticks())  # update fading text so it can fade over time

        # display informative text
        pygamedraw.draw_text(screen, "Press space to draw again.", (10, 10))
        pygamedraw.draw_text(screen, "The polygon:", (window_size[0] * 0.05, window_size[1] * 0.2))
        pygamedraw.draw_text(screen, "Decomposed to convex polygons:", (window_size[0] * 0.52, window_size[1] * 0.2))

        # line down the middle of the screen
        pygamedraw.draw_vect(screen, vmath.Vector([window_size[0] * 0.5, 0]), vmath.Vector([0, window_size[1]]))

        # display user-drawn polygon
        o.draw(screen)
        p.draw(screen)

        pygame.display.flip()  # update contents of entire display
        clock.tick()  # tick clock

    
def main():
    while True:
        res = making_polygon()
        if res == pygame.QUIT:
            return
        cpg = polygon.ConvexPolygonsGroup(polygon.SimplePolygon(res))
        if displaying_polygon(res, cpg) == pygame.QUIT:
            return
        

main()
pygame.quit()
