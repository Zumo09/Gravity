from typing import Iterable, List, Tuple
import numpy as np


def translation_matrix(dx: float, dy: float, dz: float):
    return np.array([[dx], [dy], [dz]])


def rotation_matrix(rx: float, ry: float, rz: float) -> np.ndarray:
    c = np.cos(rx)
    s = np.sin(rx)
    x = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

    c = np.cos(ry)
    s = np.sin(ry)
    y = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

    c = np.cos(rz)
    s = np.sin(rz)
    z = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    return np.matmul(np.matmul(z, y), x)


def roto_translation_matrix(
    dx: float, dy: float, dz: float, rx: float, ry: float, rz: float
):
    return np.hstack((rotation_matrix(rx, ry, rz), translation_matrix(dx, dy, dz)))


class Camera:
    def __init__(
        self,
        position: Tuple[float, float, float],
        rotation: Tuple[float, float, float],
        center: Tuple[float, float],
        focal: float = 1,
        ku_kv: Tuple[float, float] = (1, 1),
    ) -> None:
        self.focal = focal
        self.ku_kv = ku_kv
        self.center = center

        self._init_pos = position
        self._init_rot = rotation

        self.position = list(position)
        self.rotation = list(rotation)

        self._moved = False
        self.update_A()
        self.update_G()

    def update_A(self) -> None:
        self.A = np.array(
            [
                [self.focal * self.ku_kv[0], 0, self.center[0]],
                [0, self.focal * self.ku_kv[1], self.center[1]],
                [0, 0, 1],
            ],
            dtype=float,
        )

    def update_G(self) -> None:
        self.G = roto_translation_matrix(
            self.position[0],
            self.position[1],
            self.position[2],
            self.rotation[0],
            self.rotation[1],
            self.rotation[2],
        ).astype(float)

    def move(self, axes: int, movement: float) -> None:
        self.position[axes] += movement
        self._moved = True

    def rotate(self, axes: int, movement: float) -> None:
        self.rotation[axes] += movement
        self._moved = True

    def apply_movement(self) -> None:
        if self._moved:
            self._moved = False
            self.update_G()

    def reset(self):
        self.position = list(self._init_pos)
        self.rotation = list(self._init_rot)
        self.update_G()

    def project(self, position: np.ndarray) -> Tuple[float, float]:
        W = np.hstack([position, 1])
        M = np.matmul(self.G, W)
        m = np.matmul(self.A, M)
        return (m[0] / m[2], m[1] / m[2]) if m[2] != 0 else (m[0], m[1])

    def project_all(self, points) -> List[Tuple[float, float]]:
        W = np.hstack([points, np.ones((len(points), 1))])
        M = np.matmul(self.G, W.T)
        m_all = np.matmul(self.A, M)
        return [
            (m[0] / m[2], m[1] / m[2]) if m[2] != 0 else (m[0], m[1]) for m in m_all.T
        ]
