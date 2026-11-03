import math
from geometry import Vector
import pygame as pg

class Particle:
  def __init__(self, *, mass: float, pos: Vector = None, velo: Vector = None, acc: Vector = None):
    self.mass = mass

    self.radius = (mass/math.pi)**0.5

    self.pos = pos if pos is not None else Vector(0, 0)
    self.velo = velo if velo is not None else Vector(0, 0)
    self.acc = acc if acc is not None else Vector(0, 0)

  def draw(self, surface, color):
    pg.draw.circle(
      surface,
      color,
      (int(self.pos.x), int(self.pos.y)),
      int(self.radius)
    )

  def __repr__(self):
    return f"Particle(mass={self.mass}, pos={self.pos}, velo={self.velo}, acc={self.acc})"



if __name__ == "__main__":
  p = Particle(
    mass=5.0, 
    pos=Vector(x=0, y=10), 
    velo=Vector(x=2, y=0)
  )
  print(p)

  p.pos = p.pos + p.velo
  print(p)