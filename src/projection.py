import numpy as np


def translation_matrix(dx: float, dy: float, dz: float):
    return np.array([[dx], [dy], [dz]]).astype(float)


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

    return np.matmul(np.matmul(z, y), x).astype(float)


def roto_translation_matrix(rotation_matrix: np.ndarray, translation_matrix: np.ndarray) -> np.ndarray:
    return np.hstack((rotation_matrix, translation_matrix)).astype(float)


class Camera:
    NEAR_CLIP: float = 1.0

    def __init__(
        self,
        position: tuple[float, float, float],
        rotation: tuple[float, float, float],
        center: tuple[float, float],
        focal: float = 1,
        ku_kv: tuple[float, float] = (1, 1),
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
        self.T = translation_matrix(*self.position)
        self.R = rotation_matrix(*self.rotation)
        self.G = roto_translation_matrix(self.R, self.T)

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

    def _project_M(self, position: np.ndarray) -> np.ndarray:
        """Punto nello spazio camera, prima della divisione prospettica.

        M[2] è la profondità rispetto alla camera: M[2] > NEAR_CLIP significa
        "punto (abbastanza) davanti alla camera".
        """
        W = np.hstack([position, 1])
        return np.matmul(self.G, W)

    def project(self, position: np.ndarray) -> tuple[float, float]:
        M = self._project_M(position)
        return (M[0] / M[2], M[1] / M[2]) if M[2] != 0 else (M[0], M[1])

    def project_with_depth(self, position: np.ndarray) -> tuple[tuple[float, float], float]:
        """Come project(), ma restituisce anche la profondità M[2].

        Chi disegna una linea tra più punti (es. una traiettoria) deve
        spezzarla dove questo valore scende sotto NEAR_CLIP, invece di unire
        sempre tutti i punti in un'unica linea continua.
        """
        M = self._project_M(position)
        screen = (M[0] / M[2], M[1] / M[2]) if M[2] != 0 else (M[0], M[1])
        return screen, float(M[2])

    def project_all(self, points) -> list[tuple[float, float]]:
        W = np.hstack([points, np.ones((len(points), 1))])
        M = np.matmul(self.G, W.T)
        m_all = np.matmul(self.A, M)
        return [(m[0] / m[2], m[1] / m[2]) if m[2] != 0 else (m[0], m[1]) for m in m_all.T]

    def project_distance(self, position: np.ndarray) -> tuple[tuple[float, float], float, float]:
        M = self._project_M(position)
        screen = (M[0] / M[2], M[1] / M[2]) if M[2] != 0 else (M[0], M[1])
        distance = float(np.linalg.norm(M))
        return screen, distance, float(M[2])
