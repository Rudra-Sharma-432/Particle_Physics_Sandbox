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



if __name__ == "__main__":
  # They will run ONLY if you run vector.py directly, 
  # but they will be ignored when you import it into main.py!
  

  # Create vectors using cartesian coordinates
  v1 = Vector(x=3, y=4)
  v2 = Vector(x=1, y=2)

  print(v1 + v2)      # Output: Vector(x=4.00, y=6.00, mag=7.21, theta=0.98)
  print(v1 * 2)       # Output: Vector(x=6.00, y=8.00, mag=10.00, theta=0.93)
  print(2 * v1)       # Output: Vector(x=6.00, y=8.00, mag=10.00, theta=0.93)
  print(v1 * v2)      # Output: 11.0 (Dot product: 3*1 + 4*2)

  # Create a vector using polar coordinates (Magnitude = 5, Theta = 0.927 radians)
  v3 = Vector(magnitude=5, theta=0.927295)
  print(v3)           # Output: Vector(x=3.00, y=4.00, mag=5.00, theta=0.93)
