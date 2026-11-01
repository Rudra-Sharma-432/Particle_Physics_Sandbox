import math

class Vector:
  def __init__(self, x: float = None, y: float = None, magnitude: float = None, theta: float = None):

    self.x = x if x is not None else magnitude * math.cos(theta)
    self.y = y if y is not None else magnitude * math.sin(theta)
    
    self.magnitude = magnitude if magnitude is not None else math.hypot(x, y)
    self.theta = theta if theta is not None else math.atan2(y, x)


  def __add__(self, other):
    if isinstance(other, Vector):
      return Vector(x=self.x + other.x, y=self.y + other.y)
    return NotImplemented

  def __sub__(self, other):
    if isinstance(other, Vector):
      return Vector(x=self.x - other.x, y=self.y - other.y)
    return NotImplemented

  def __mul__(self, other):
    # Scalar multiplication (Vector * number) -> returns a new Vector
    if isinstance(other, (int, float)):
        return Vector(x=self.x * other, y=self.y * other, magnitude=None, theta=None)
    
    # Dot product (Vector * Vector) -> returns a float scalar
    if isinstance(other, Vector):
        return self.x * other.x + self.y * other.y

    return NotImplemented

  def __rmul__(self, other):
    return self.__mul__(other)

  def __repr__(self):
    return f"Vector(x={self.x:.2f}, y={self.y:.2f}, mag={self.magnitude:.2f}, theta={self.theta:.2f})"
