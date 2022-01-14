from __future__ import annotations
from collections import deque
from typing import List, Tuple
import numpy as np

class GravitationalBody:
    def __init__(self, 
    mass: float, radius: float, 
    position: Tuple[float, float, float], 
    velocity: Tuple[float, float, float] = (0, 0, 0),
    color: Tuple[float, float, float] = (255, 255, 255), trajectory_len: int = 2) -> None:
        self.mass = mass
        self.radius = radius
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)

        self.color = color
        self.trajectory = deque(maxlen=trajectory_len)

        for _ in range(2):
            self.trajectory.append(self.position.copy())
    
    def gravitational_foce(self, bodies: List[GravitationalBody], dt: float, G: float) -> None:
        dV = np.zeros(3, dtype=float)
        for body in bodies:
            dV += self._acceleration(body)
        self.velocity += G * dV * dt
    
    def update(self):
        self.trajectory.append(self.position.copy())
        self.position += self.velocity

    def _acceleration(self, other: GravitationalBody) -> np.ndarray:
        if self is other:
            return np.zeros(3, dtype=float)

        distance = np.array(other.position - self.position)
        norm_distance = np.linalg.norm(distance)
        if norm_distance < 2 * (self.radius + other.radius):
            distance *= -0.1 
        return (other.mass / norm_distance ** 3) * distance

        