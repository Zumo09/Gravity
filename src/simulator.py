from doctest import REPORT_UDIFF
from tkinter.messagebox import NO
from turtle import update
import projection
from typing import List, Optional, Tuple, Union
import numpy as np

import random
import pygame

from body import GravitationalBody

pygame.init()
font = pygame.font.SysFont("Arial", 32, bold=True)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
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
    (0, 50, 0), 
    (0, 0, 100), 
    (210, 150, 75), 
    (255, 200, 0), 
    (255, 255, 100), 
    (0, 255, 255), 
    (200, 200, 200), 
    (50, 50, 50), 
    (230, 220, 170), 
    (200, 190, 140), 
]

class GravitySimulator:
    def __init__(self, width: int = 640, height: int = 480, G: float = 100, fps: int = 30, dt: float = 1):
        self.G = G
        self.FPS = fps
        self.dt = dt

        self.width = width
        self.height = height

        self.cam_vel = 100
        self.cam_rot = 0.1

        # init display
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Gravity')

        self.clock = pygame.time.Clock()
        self.camera = projection.Camera((1000, 1000, 1000), (1, 1, 1), (self.width / 2, self.height / 2))

        self.running = False
        self.time = 0

        self.bodies: List[GravitationalBody] = []

    def add_body(self, body: GravitationalBody) -> None:
        body.color = random.choice(COLORS)
        self.bodies.append(body)

    def add_bodies(self, bodies: List[GravitationalBody]) -> None:
        for body in bodies:
            self.add_body(body)

    def simulation_step(self) -> bool:
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.running = not self.running 

                elif event.key == pygame.K_w:
                    self.camera.move(1, self.cam_vel)
                elif event.key == pygame.K_s:
                    self.camera.move(1, -self.cam_vel)
                elif event.key == pygame.K_a:
                    self.camera.move(0, -self.cam_vel)
                elif event.key == pygame.K_d:
                    self.camera.move(0, self.cam_vel)
                elif event.key == pygame.K_q:
                    self.camera.move(2, -self.cam_vel)
                elif event.key == pygame.K_e:
                    self.camera.move(2, self.cam_vel)

                elif event.key == pygame.K_UP:
                    self.camera.rotate(1, self.cam_rot)
                elif event.key == pygame.K_DOWN:
                    self.camera.rotate(1, -self.cam_rot)
                elif event.key == pygame.K_LEFT:
                    self.camera.rotate(0, -self.cam_rot)
                elif event.key == pygame.K_RIGHT:
                    self.camera.rotate(0, self.cam_rot)
                elif event.key == pygame.K_r:
                    self.camera.rotate(2, -self.cam_rot)
                elif event.key == pygame.K_f:
                    self.camera.rotate(2, self.cam_rot)


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

    def _update_ui(self):
        self.display.fill(BLACK)

        scale = 1000
        origin = self.camera.project((0, 0, 0))
        xx = self.camera.project((scale, 0, 0))
        yy = self.camera.project((0, scale, 0))
        zz = self.camera.project((0, 0, scale))
        pygame.draw.line(self.display, RED, origin, xx, scale)
        pygame.draw.line(self.display, GREEN, origin, yy, scale)
        pygame.draw.line(self.display, BLUE, origin, zz, scale)

        # for body in self.bodies:
        #     m = self._project(body.position)
        #     r = self._scale_radius(body)
        #     pygame.draw.circle(self.display, body.color, m, r)
        #     trajectory = [self._project(x, y, z) for x, y, z in body.trajectory]
        #     pygame.draw.aalines(self.display, body.color, False, trajectory)

        text = font.render("Time: " + str(self.time), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()        


if __name__ == '__main__':
    sim = GravitySimulator()
    TRAJECTORY_LEN = 1000

    # game loop
    while sim.simulation_step():
        pass

    pygame.quit()

