from __future__ import annotations
import vmath
import pygame
import pygamedraw

class Vector:
    def __init__(self, pos: vmath.Vector, dir: vmath.Vector) -> None:
        for v in [pos, dir]:
            if type(v) != vmath.Vector:
                raise TypeError("Vector only accepts type vmath.Vector")
        self.pos = pos
        self.dir = dir
    
    def __repr__(self) -> str:
        return "{pos:" + str(self.pos) + ", dir:" + str(self.dir) + "}"
    
    def intersects(self, other: Vector) -> bool:
        l1 = vmath.VectorLinearFunc(self.pos, self.dir)
        l2 = vmath.VectorLinearFunc(other.pos, other.dir)
        return vmath.VectorLinearFunc.intersect(l1, l2)
    
    def draw(self, screen: pygame.Surface, color: pygame.Color = pygame.Color(0, 0, 0)):
        pygamedraw.draw_vect(screen, self.pos, self.dir, color)