from __future__ import annotations
from collections import deque
from typing import List, Tuple
import numpy as np

class GravitationalBody:
    def __init__(self, 
    mass: float, radius: float, 
    px: float, py: float, pz: float, 
    vx: float = 0.0, vy: float = 0.0, vz: float = 0.0,
    color: Tuple[int, int, int] = (255, 255, 255), trajectory_len: int = 100) -> None:
        self.mass = mass
        self.radius = radius
        self.position = np.array([px, py, pz], dtype=float)
        self.velocity = np.array([vx, vy, vz], dtype=float)
        self.color = color
        self.trajectory = deque(maxlen=trajectory_len)

        for _ in range(10):
            self.trajectory.append(self.coordinates)

    @property
    def coordinates(self) -> Tuple[float, float, float]:
        return self.position[0], self.position[1], self.position[2]
    
    def gravitational_foce(self, bodies: List[GravitationalBody], dt: float, G: float) -> None:
        dV = np.zeros(3, dtype=float)
        for body in bodies:
            dV += G * self._acceleration(body)
        
        self.velocity += dV * dt
    
    def update(self):
        self.trajectory.append(self.coordinates)
        self.position += self.velocity

    def _acceleration(self, other: GravitationalBody) -> np.ndarray:
        if self is other:
            return np.zeros(3, dtype=float)

        distance = other.position - self.position 
        norm_distance = np.linalg.norm(distance)
        return (other.mass / norm_distance ** 3) * distance

        