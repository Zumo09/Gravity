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
        camera_init_pos: Tuple[float, float, float] = (0, 0, -2500),
        camera_init_rot: Tuple[float, float, float] = (0, 0, 0),
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

        self.center = (width // 2, height // 2)
        self.center_center = (width // 4, height // 4)

        self.background = background_color
        self.cam_vel = 50
        self.cam_rot = 0.01

        self.camera = Camera(
            camera_init_pos, camera_init_rot, self.center_center, focal=1000
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
        self.scale = 1000
        self.radius = 10
        self.cube *= self.scale
        self.proj_xyz = (
            self._xy_proj,
            self._xz_proj,
            self._yz_proj
        )

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
            start = np.clip(projected[i], (0, 0), self.center)
            end = np.clip(projected[j], (0, 0), self.center)
            color = tuple(int((c1 + c2) / 2) for c1, c2 in zip(self.colors[i], self.colors[j]))
            pygame.draw.line(self.display, color, start, end)
        for idx in reversed(np.argsort(distances)):
            radius = self.radius * self.camera.focal / distances[idx]
            center = projected[idx]
            if center[0] < self.center[0] and center[1] < self.center[1]:
                pygame.draw.circle(self.display, self.colors[idx], center, radius)
    
    def _check_project(self, point, ax, check):
        if check and point[ax] == 0:
            return None
        return  point * 0.1

    def _yz_proj(self, point, check=True):
        point = self._check_project(point, 0, check)
        if point is None:
            return None
        return (point[1] + self.center_center[0] + self.center[0], point[2] + self.center_center[1]) 

    def _xz_proj(self, point, check=True):
        point = self._check_project(point, 1, check)
        if point is None:
            return None
        return (point[0] + self.center_center[0], point[2] + self.center_center[1] + self.center[1]) 

    def _xy_proj(self, point, check=True):
        point = self._check_project(point, 2, check)
        if point is None:
            return None
        return (point[0] + self.center_center[0] + self.center[0], point[1] + self.center_center[1] + self.center[1]) 

    def _draw_projections(self):
        for (i, j) in self.connections:
            color = tuple(int((c1 + c2) / 2) for c1, c2 in zip(self.colors[i], self.colors[j]))
            start = self.cube[i]
            end = self.cube[j]
            for prj in self.proj_xyz:
                s = prj(start)
                e = prj(end)
                if e is not None and s is not None:
                    pygame.draw.line(self.display, color, s, e)

        for point, color in zip(self.cube, self.colors):
            for prj in self.proj_xyz:
                c = prj(point)
                if c is not None:
                    pygame.draw.circle(self.display, color, c, self.radius)
        
        for prj in self.proj_xyz:
            c = prj(np.array(self.camera.position).astype(float), check=False)
            if c is not None:
                pygame.draw.circle(self.display, (0, 0, 0), c, self.radius)

    def _update_ui(self):
        self.display.fill(self.background)
        
        self._draw_cube()
        self._draw_projections()

        pygame.draw.line(self.display, (0, 0, 0), (self.center[0], 0), (self.center[0], 2 * self.center[1]), 5)
        pygame.draw.line(self.display, (0, 0, 0), (0, self.center[1]), (2 * self.center[0], self.center[1]), 5)
        pygame.display.flip()

    def main_loop(self):
        while self.simulation_step():
            continue
        pygame.quit()

if __name__ == '__main__':
    SandBox().main_loop()