import ctypes
import sys

import numpy as np
import pygame

from body import GravitationalBody
from projection import Camera, rotation_matrix

if sys.platform == "win32":
    try:
        # Per-monitor DPI awareness (Windows 8.1+) - la scelta più corretta
        ctypes.windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
    except (AttributeError, OSError):
        try:
            # Fallback per versioni più vecchie di Windows
            ctypes.windll.user32.SetProcessDPIAware()
        except (AttributeError, OSError):
            pass


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
        background_color: tuple[int, int, int] = (0, 0, 10),
        star_color: tuple[int, int, int] = (255, 255, 255),
        camera_init_pos: tuple[float, float, float] = (-500, -500, -10000),
        camera_init_rot: tuple[float, float, float] = (0.5, 0.5, 0),
        screen_dim: tuple[int, int] | None = None,
        start_time: bool = True,
        start_movement: bool = True,
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

        self.cam_auto_z = 0
        self.cam_auto_rotation = 0.5 * (0.5 - np.random.random(size=3))

        self.camera = Camera(camera_init_pos, camera_init_rot, (width // 2, height // 2), focal=1000)

        self.bodies: list[GravitationalBody] = []
        self.stars = [random_star(100000) for _ in range(num_star)]

        self.is_alive = True

    def add_body(self, body: GravitationalBody) -> None:
        self.bodies.append(body)

    def add_bodies(self, bodies: list[GravitationalBody]) -> None:
        self.bodies.extend(bodies)

    def _handle_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_alive = False
            elif event.type == pygame.VIDEORESIZE:
                self.screen_size = event.size
                self.screen = pygame.display.set_mode(event.size, pygame.RESIZABLE)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                self._on_mouse_motion(event.pos)
            elif event.type == pygame.MOUSEWHEEL:
                self._on_scroll(event.y)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self._on_left_click(event.pos)
            elif event.type == pygame.KEYDOWN:
                self._on_key(event.key)

    def _on_mouse_motion(self, pos: tuple[int, int]) -> None:
        pass

    def _on_scroll(self, dy: int) -> None:
        pass

    def _on_left_click(self, pos: tuple[int, int]) -> None:
        pass

    def _on_key(self, key: int) -> None:
        if key == pygame.K_ESCAPE:
            self.is_alive = False
        elif key == pygame.K_SPACE:
            self.running = not self.running
        elif key == pygame.K_r:
            self.camera.reset()
        elif key == pygame.K_t:
            self.move_camera = not self.move_camera

    def _handle_key_pressed(self) -> None:
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

    def _update_camera(self) -> None:
        if self.move_camera:
            self.cam_auto_rotation += 0.01 * (0.5 - np.random.random(size=3))
            if np.linalg.norm(self.cam_auto_rotation) > 0.5:
                self.cam_auto_rotation = 0.5 * (0.5 - np.random.random(size=3))

            self.camera.rotate(1, self.cam_auto_rotation[0] * self.cam_rot)
            self.camera.rotate(0, self.cam_auto_rotation[1] * self.cam_rot)
            self.camera.rotate(2, self.cam_auto_rotation[2] * self.cam_rot)

            self.cam_auto_z = (self.cam_auto_z + 0.005) % (2 * np.pi)
            self.camera.move(2, 0.1 * np.sin(self.cam_auto_z) * self.cam_vel)

        self.camera.apply_movement()

    def _update_simulation(self) -> None:
        if not self.running:
            return

        for body in self.bodies:
            body.gravitational_foce(self.bodies, self.dt, self.G)

        for body in self.bodies:
            body.update()

    def _draw_trajectory(self, body: GravitationalBody) -> None:
        """Disegna la traiettoria spezzandola ogni volta che un punto
        attraversa il piano della camera, per evitare la linea fantasma
        che altrimenti la collegherebbe alla sua proiezione "specchiata"
        dall'altra parte dello schermo.
        """
        run: list[tuple[float, float]] = []
        for point in body.trajectory:
            screen, z = self.camera.project_with_depth(point)
            if z > self.camera.NEAR_CLIP:
                run.append(screen)
            else:
                if len(run) > 1:
                    pygame.draw.aalines(self.display, body.color, False, run)
                run = []
        if len(run) > 1:
            pygame.draw.aalines(self.display, body.color, False, run)

    def _draw(self):
        self.display.fill(self.background)

        for star in self.stars:
            screen, z = self.camera.project_with_depth(star)
            if z <= self.camera.NEAR_CLIP:
                continue  # Stella dietro la camera: si scarta invece di proiettarla "specchiata".
            pygame.draw.circle(self.display, self.star_color, screen, 1)

        distance_body = {}
        for body in self.bodies:
            self._draw_trajectory(body)

            center, distance, z = self.camera.project_distance(body.position)
            if z <= self.camera.NEAR_CLIP:
                continue  # Corpo dietro la camera: non disegnarlo questo frame.
            radius = body.radius * self.camera.focal / distance
            distance_body[distance] = (body.color, center, radius)

        for distance in sorted(distance_body.keys(), reverse=True):
            color, center, radius = distance_body[distance]
            pygame.draw.circle(self.display, color, center, radius)

        pygame.display.flip()

    def main_loop(self) -> None:
        while self.is_alive:
            self._update_camera()
            self._update_simulation()
            self._draw()
            self.clock.tick(self.FPS)

        pygame.quit()
