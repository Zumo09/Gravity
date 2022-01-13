from typing import Tuple
import numpy as np

def translation_matrix(dx: float, dy: float, dz: float):   
    return np.array([[dx],
                     [dy],
                     [dz]])

def rotation_matrix(rx: float, ry: float, rz: float) -> np.ndarray:   
    c = np.cos(rx)
    s = np.sin(rx)
    x = np.array([
        [1, 0, 0],
        [0, c,-s],
        [0, s, c]])
    
    c = np.cos(ry)
    s = np.sin(ry)
    y = np.array([
        [ c, 0, s],
        [ 0, 1, 0],
        [-s, 0, c]])
    
    c = np.cos(rz)
    s = np.sin(rz)
    z = np.array([
        [c,-s, 0],
        [s, c, 0],
        [0, 0, 1]])

    return x @ y @ z

def roto_translation_matrix(dx: float, dy: float, dz: float, rx: float, ry: float, rz: float):   
    return np.hstack((rotation_matrix(rx, ry, rz), translation_matrix(dx, dy, dz)))

def transform(vector, matrix):
    """ Apply a transformation defined by a given matrix. """
    return np.dot(matrix, vector)

class Camera:
    def __init__(self, position: Tuple[float, float, float], rotation: Tuple[float, float, float], 
    center: Tuple[float, float], focal: float = 1, ku_kv: Tuple[float, float] = (1, 1)) -> None:
        self.focal = focal
        self.ku_kv = ku_kv
        self.center = center
        
        self.position = list(position)
        self.rotation = list(rotation)
        
        self.A = self.generate_A()
        self.G = self.generate_G()

    def generate_A(self):
        return np.array([
            [self.focal * self.ku_kv[0], 0, self.center[0] / 2],
            [0, self.focal * self.ku_kv[1], self.center[1] / 2],
            [             0,             0,                  1]
        ])

    def generate_G(self) -> np.ndarray:
        return roto_translation_matrix(
            self.position[0], 
            self.position[1],
            self.position[2],
            self.rotation[0],
            self.rotation[1],
            self.rotation[2])

    def move(self, axes: int, movement: float) -> None:
        self.position[axes] += movement
        self.G = self.generate_G()

    def rotate(self, axes: int, movement: float) -> None:
        self.rotation[axes] += movement
        self.G = self.generate_G()

    def project(self, position: Tuple[float, float, float]) -> Tuple[float, float]:
        W = np.array([*position, 1])
        M = transform(W, self.G)
        m = transform(M, self.A)
        if m[2] == 0:
            return m[0], m[1]
        else:
            return m[0] / m[2], m[1] / m[2]