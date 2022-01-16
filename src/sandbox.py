from typing import List, Optional, Tuple
import numpy as np

from projection import Camera, rotation_matrix

import pygame

WHITE = (255, 255, 255)

class SandBox:
    FPS: int = 60
    def __init__(
        self,
        background_color: Tuple[int, int, int] = (150, 150, 150),
        camera_init_pos: Tuple[float, float, float] = (500, 500, 10000),
        camera_init_rot: Tuple[float, float, float] = (0.5, 0.5, 0),
        screen_dim: Optional[Tuple[int, int]] = None,
    ):
        pygame.init()
        if screen_dim is not None:
            self.display = pygame.display.set_mode(screen_dim)
        else:
            self.display = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption("SANDBOX")
        self.clock = pygame.time.Clock()
        width = self.display.get_width()
        height = self.display.get_height()

        self.background = background_color
        self.cam_vel = 50
        self.cam_rot = 0.01

        self.camera = Camera(
            camera_init_pos, camera_init_rot, (width // 2, height // 2), focal=1000
        )

        self.cube = np.array([
            [0, 0, 0],
            [0, 0, 1],
            [1, 0, 1],
            [1, 0, 0],
            [0, 1, 0],
            [0, 1, 1],
            [1, 1, 1],
            [1, 1, 0],
        ])
        self.colors = (
            (  0,   0,   0),
            (  0,   0, 255),
            (255,   0, 255),
            (255,   0,   0),
            (  0, 255,   0),
            (  0, 255, 255),
            (255, 255, 255),
            (255, 255,   0),
        )
        self.connections = (
            (0, 1), (1, 2), (2, 3), (3, 0), 
            (4, 5), (5, 6), (6, 7), (7, 4),
            (0, 4), (1, 5), (2, 6), (3, 7)
        )
        self.cube *= 1000

    def simulation_step(self) -> bool:
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r:
                    self.camera.reset()

        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_w]:
            self.camera.move(1, self.cam_vel)
        if key_pressed[pygame.K_s]:
            self.camera.move(1, -self.cam_vel)
        if key_pressed[pygame.K_a]:
            self.camera.move(0, self.cam_vel)
        if key_pressed[pygame.K_d]:
            self.camera.move(0, -self.cam_vel)
        if key_pressed[pygame.K_q]:
            self.camera.move(2, self.cam_vel)
        if key_pressed[pygame.K_e]:
            self.camera.move(2, -self.cam_vel)

        if key_pressed[pygame.K_i]:
            self.camera.rotate(1, -self.cam_rot)
        if key_pressed[pygame.K_k]:
            self.camera.rotate(1, self.cam_rot)
        if key_pressed[pygame.K_j]:
            self.camera.rotate(0, self.cam_rot)
        if key_pressed[pygame.K_l]:
            self.camera.rotate(0, -self.cam_rot)
        if key_pressed[pygame.K_u]:
            self.camera.rotate(2, self.cam_rot)
        if key_pressed[pygame.K_o]:
            self.camera.rotate(2, -self.cam_rot)

        self.camera.apply_movement()

        self._update_ui()
        self.clock.tick(self.FPS)

        return True
    
    def _draw_cube(self):
        projected = self.camera.project_all(self.cube)
        distances = [self.camera.distance(p) for p in self.cube]
        for (i, j) in self.connections:
            color = tuple(int((c1 + c2) / 2) for c1, c2 in zip(self.colors[i], self.colors[j]))
            pygame.draw.line(self.display, color, projected[i], projected[j])
        for idx in reversed(np.argsort(distances)):
            radius = 100 * self.camera.focal / distances[idx]
            pygame.draw.circle(self.display, self.colors[idx], projected[idx], radius)        

    def _update_ui(self):
        self.display.fill(self.background)
        self._draw_cube()
        pygame.display.flip()

    def main_loop(self):
        while self.simulation_step():
            continue
        pygame.quit()

if __name__ == '__main__':
    SandBox().main_loop()