import random
from typing import List, Tuple
import pygame

from body import GravitationalBody

pygame.init()
font = pygame.font.SysFont("Arial", 32, bold=True)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (5, 255, 255), 
    (0, 0, 255), 
    (0, 255, 0), 
    (255, 0, 0), 
    # (255, 100, 10), 
    # (255, 255, 0), 
    # (0, 255, 170), 
    # (115, 0, 0), 
    # (180, 255, 100), 
    # (255, 100, 180), 
    # (240, 0, 255), 
    # (127, 127, 127), 
    # (255, 0, 230), 
    # (100, 40, 0), 
    # (0, 50, 0), 
    # (0, 0, 100), 
    # (210, 150, 75), 
    # (255, 200, 0), 
    # (255, 255, 100), 
    # (0, 255, 255), 
    # (200, 200, 200), 
    # (50, 50, 50), 
    # (230, 220, 170), 
    # (200, 190, 140), 
    # (235, 245, 255)
]

class GravitySimulator:
    G = 100.0
    FPS = 30
    dt = 1.0
    TRAJECTORY_LEN = 100

    def __init__(self, width: int = 640, height: int = 480):
        self.width = width
        self.height = height
        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Gravity')

        self.clock = pygame.time.Clock()

        self.running = False

        self.time = 0

        self.bodies: List[GravitationalBody] = []

    def add_body(self, mass: float, radius: float, 
        px: float, py: float, pz: float, 
        vx: float = 0, vy: float = 0, vz: float = 0):

        color = random.choice(COLORS)
        self.bodies.append(GravitationalBody(mass, radius, px, py, pz, vx, vy, vz, color, self.TRAJECTORY_LEN))

    def simulation_step(self):
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = not self.running 

        # 2. update bodies
        if self.running:
            self._apply_gravity()
            self.time += self.dt

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.FPS)

    def _apply_gravity(self):
        for body in self.bodies:
            body.gravitational_foce(self.bodies, self.dt, self.G)

        for body in self.bodies:
            body.update()

    def _project(self, x: float, y: float, z: float) -> Tuple[float, float]:
        return self.width / 2 + x/z, self.width / 2 + y/z

    def _update_ui(self):
        self.display.fill(BLACK)

        for body in self.bodies:
            x, y, z = body.coordinates
            pygame.draw.circle(self.display, body.color, self._project(x, y, z), body.radius/z)
            trajectory = [self._project(x, y, z) for x, y, z in body.trajectory]
            pygame.draw.aalines(self.display, body.color, False, trajectory)

        text = font.render("Time: " + str(self.time), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()        


if __name__ == '__main__':
    sim = GravitySimulator()

    sim.add_body(mass=10.0, radius=1000.0, px=1000.0, py=1000.0, pz=10.0)
    sim.add_body(mass=10.0, radius=1000.0, px=-1000.0, py=-1000.0, pz=10.0)

    # game loop
    while True:
        sim.simulation_step()