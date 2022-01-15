from typing import List, Optional, Tuple
import numpy as np

from projection import Camera, rotation_matrix
from body import GravitationalBody

import pygame


def shades(
    light: Tuple[int, int, int], dark: Tuple[int, int, int], shades: int
) -> List[Tuple[int, int, int]]:
    gaps = [(l - d) / (shades - 1) for l, d in zip(light, dark)]
    return [
        (
            int(light[0] - s * gaps[0]),
            int(light[1] - s * gaps[1]),
            int(light[2] - s * gaps[2]),
        )
        for s in range(shades)
    ]


def random_star(min_distance: int) -> np.ndarray:
    d = np.random.randint(min_distance, 2 * min_distance)
    r = np.random.random(size=3) * np.pi * 4
    p = rotation_matrix(*r)
    return np.matmul(p, [d, 0, 0])


class GravitySimulator:
    G: float = 100
    FPS: int = 60
    dt: float = 0.05

    def __init__(
        self,
        num_star: int = 200,
        background_color: Tuple[int, int, int] = (0, 0, 10),
        star_color: Tuple[int, int, int] = (255, 255, 255),
        camera_init_pos: Tuple[float, float, float] = (-500, -500, -10000),
        camera_init_rot: Tuple[float, float, float] = (0.5, 0.5, 0),
        screen_dim: Optional[Tuple[int, int]] = None,
        start_time: bool = True,
        start_movement: bool = True
    ):
        pygame.init()
        if screen_dim is not None:
            self.display = pygame.display.set_mode(screen_dim)
        else:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("Gravity Simulator")
        self.clock = pygame.time.Clock()
        width = self.display.get_width()
        height = self.display.get_height()

        self.running = start_time
        self.move_camera = start_movement

        self.background = background_color
        self.star_color = star_color

        self.cam_vel = 50
        self.cam_rot = 0.01

        self.cam_auto_rotation = 0.5 * (0.5 - np.random.random(size=3))
        
        self.camera = Camera(
            camera_init_pos, camera_init_rot, (width // 2, height // 2), focal=1000
        )

        self.bodies: List[GravitationalBody] = []
        self.stars = [random_star(100000) for _ in range(num_star)]

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
                elif event.key == pygame.K_r:
                    self.camera.reset()
                elif event.key == pygame.K_t:
                    self.move_camera = not self.move_camera

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.camera.move(1, -self.cam_vel)
        if key_pressed[pygame.K_s]:
            self.camera.move(1, self.cam_vel)
        if key_pressed[pygame.K_a]:
            self.camera.move(0, -self.cam_vel)
        if key_pressed[pygame.K_d]:
            self.camera.move(0, self.cam_vel)
        if key_pressed[pygame.K_q]:
            self.camera.move(2, -self.cam_vel)
        if key_pressed[pygame.K_e]:
            self.camera.move(2, self.cam_vel)

        if key_pressed[pygame.K_i]:
            self.camera.rotate(1, self.cam_rot)
        if key_pressed[pygame.K_k]:
            self.camera.rotate(1, -self.cam_rot)
        if key_pressed[pygame.K_j]:
            self.camera.rotate(0, -self.cam_rot)
        if key_pressed[pygame.K_l]:
            self.camera.rotate(0, self.cam_rot)
        if key_pressed[pygame.K_u]:
            self.camera.rotate(2, -self.cam_rot)
        if key_pressed[pygame.K_o]:
            self.camera.rotate(2, self.cam_rot)

        if self.move_camera:
            self.cam_auto_rotation += 0.01 * (0.5 - np.random.random(size=3))
            if np.linalg.norm(self.cam_auto_rotation) > 0.5:
                self.cam_auto_rotation = 0.5 * (0.5 - np.random.random(size=3))

            self.camera.rotate(1, self.cam_auto_rotation[0] * self.cam_rot)
            self.camera.rotate(0, self.cam_auto_rotation[1] * self.cam_rot)
            self.camera.rotate(2, self.cam_auto_rotation[2] * self.cam_rot)

        self.camera.apply_movement()

        if self.running:
            for body in self.bodies:
                body.gravitational_foce(self.bodies, self.dt, self.G)

            for body in self.bodies:
                body.update()

        self._update_ui()
        self.clock.tick(self.FPS)

        return True

    def _scale_radius(self, body: GravitationalBody) -> float:
        r = body.radius
        distance = float(np.linalg.norm(self.camera.position - body.position))
        return r * self.camera.focal / distance

    def _update_ui(self):
        self.display.fill(self.background)

        for star in self.camera.project_all(self.stars):
            pygame.draw.circle(self.display, self.star_color, star, 1)

        for body in self.bodies:
            m = self.camera.project(body.position)
            r = self._scale_radius(body)
            pygame.draw.circle(self.display, body.color, m, r)
            trajectory = self.camera.project_all(body.trajectory)
            pygame.draw.aalines(self.display, body.color, False, trajectory)

        pygame.display.flip()

    def main_loop(self):
        while self.simulation_step():
            continue

        pygame.quit()
