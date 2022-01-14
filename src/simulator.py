from typing import List, Optional, Tuple
import numpy as np

from projection import Camera, rotation_matrix
from body import GravitationalBody

import pygame

pygame.init()
font = pygame.font.SysFont("Arial", 22, bold=True)

BLACK = (0, 0, 0)
NAVY_BLUE = ((0, 0, 10))
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
DANDILION_YELLOW = (255,200,0)
COLORS = [
    (5, 255, 255),
    (255, 100, 10), 
    (255, 255, 0), 
    (0, 255, 170), 
    (115, 0, 0), 
    (180, 255, 100), 
    (255, 100, 180), 
    (240, 0, 255), 
    (127, 127, 127), 
    (255, 0, 230), 
    (100, 40, 0), 
    # (0, 50, 0), 
    # (0, 0, 100), 
    (210, 150, 75), 
    (255, 200, 0), 
    (255, 255, 100), 
    # (0, 255, 255), 
    # (200, 200, 200), 
    # (50, 50, 50), 
    (230, 220, 170), 
    (200, 190, 140), 
]

def random_star():
    l = 8000
    d = np.random.randint(l, 2 * l)
    r = np.random.random(size=3) * np.pi * 4
    p = rotation_matrix(*r)
    return np.matmul(p, [d, 0, 0])

class GravitySimulator:
    def __init__(self, G: float = 100, fps: int = 60, dt: float = 0.05, screen_dim: Optional[Tuple[int, int]] = None):
        self.G = G
        self.FPS = fps
        self.dt = dt

        # init display
        if screen_dim is not None:
            self.display = pygame.display.set_mode(screen_dim)
        else:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Gravity')

        width = self.display.get_width()
        height = self.display.get_height()

        self.cam_vel = 10
        self.cam_rot = 0.01
        self.r = 0.5 * (0.5 - np.random.random(size=3))
        self.stars = [random_star() for _ in range(200)]

        self.clock = pygame.time.Clock()
        self.camera = Camera((-500, -500, -10000), (0.5, 0.5, 0), (width // 2, height // 2), focal=1000)

        self.running = False
        self.time = 0

        self.bodies: List[GravitationalBody] = []

    def add_body(self, body: GravitationalBody) -> None:
        self.bodies.append(body)

    def add_bodies(self, bodies: List[GravitationalBody]) -> None:
        self.bodies.extend(bodies)

    def simulation_step(self) -> bool:
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.running = not self.running 
                elif event.key == pygame.K_p:
                    self.camera.reset()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.camera.move(1, self.cam_vel)
        if key_pressed[pygame.K_s]:
            self.camera.move(1, -self.cam_vel)
        if key_pressed[pygame.K_a]:
            self.camera.move(0, -self.cam_vel)
        if key_pressed[pygame.K_d]:
            self.camera.move(0, self.cam_vel)
        if key_pressed[pygame.K_q]:
            self.camera.move(2, -self.cam_vel)
        if key_pressed[pygame.K_e]:
            self.camera.move(2, self.cam_vel)

        if key_pressed[pygame.K_UP]:
            self.camera.rotate(1, self.cam_rot)
        if key_pressed[pygame.K_DOWN]:
            self.camera.rotate(1, -self.cam_rot)
        if key_pressed[pygame.K_LEFT]:
            self.camera.rotate(0, -self.cam_rot)
        if key_pressed[pygame.K_RIGHT]:
            self.camera.rotate(0, self.cam_rot)
        if key_pressed[pygame.K_r]:
            self.camera.rotate(2, -self.cam_rot)
        if key_pressed[pygame.K_f]:
            self.camera.rotate(2, self.cam_rot)

        self.r += 0.01 * (0.5 - np.random.random(size=3))
        if np.linalg.norm(self.r) > 0.5:
            self.r = 0.5 * (0.5 - np.random.random(size=3))

        self.camera.rotate(1, self.r[0] * self.cam_rot)
        self.camera.rotate(0, self.r[1] * self.cam_rot)
        self.camera.rotate(2, self.r[2] * self.cam_rot)


        # 2. update bodies
        if self.running:
            self._apply_gravity()
            self.time += self.dt

        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(self.FPS)

        return True

    def _apply_gravity(self):
        for body in self.bodies:
            body.gravitational_foce(self.bodies, self.dt, self.G)

        for body in self.bodies:
            body.update()    

    def _scale_radius(self, body: GravitationalBody) -> float:
        r = body.radius
        distance = float(np.linalg.norm(self.camera.position - body.position))
        return r * self.camera.focal / distance

    def _update_ui(self):
        self.display.fill(NAVY_BLUE)

        for star in self.camera.project_all(self.stars):
            pygame.draw.circle(self.display, WHITE, star, 1)        

        for body in self.bodies:
            m = self.camera.project(body.position)
            r = self._scale_radius(body)
            pygame.draw.circle(self.display, body.color, m, r)
            trajectory = self.camera.project_all(body.trajectory)
            pygame.draw.aalines(self.display, body.color, False, trajectory)

        # text = font.render(f"Time: {self.time:.2f}", True, WHITE)
        # self.display.blit(text, [0, 0])

        pygame.display.flip()        


if __name__ == '__main__':
    sim = GravitySimulator()
    sim.add_bodies([
        GravitationalBody(10, 30, (0, 1000, 0), (70, 0, 30), color=RED, trajectory_len=100),
        GravitationalBody(10, 60, (0, 2000, 0), (50, 0, 0), color=GREEN, trajectory_len=220),
        GravitationalBody(10, 50, (0, 3000, 0), (0, 0, 30), color=BLUE, trajectory_len=230),
        GravitationalBody(1e6, 100, (0, 0, 0), (0, 0, 0), color=DANDILION_YELLOW)
    ])

    # game loop
    while sim.simulation_step():
        pass

    pygame.quit()

