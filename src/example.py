import pygame
import numpy as np

from projection import Camera

black, white, blue  = (20, 20, 20), (230, 230, 230), (0, 154, 255)
width, height = 800, 600

pygame.init()
pygame.display.set_caption("3D cube Projection")

font = pygame.font.SysFont("Arial", 24, bold=True)
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
fps = 60

points = [
    np.array([0, 0, 10]),
    np.array([10, 0, 10]),
    np.array([10, 10, 10]),
    np.array([0, 10, 10]),
    np.array([0, 0, 0]),
    np.array([10, 0, 0]),
    np.array([10, 10, 0]),
    np.array([0, 10, 0]),
]
camera = Camera((1, 1, -100), (0, 0, 0), (width // 2, height // 2), focal=1000)   
# camera = Camera((1, 1, -1.05), (0, 0, 0), (width // 2, height // 2), focal=0.1, ku_kv=(100, 100))   
speed = 0.01

def connect_point(i, j, k):
    a = k[i]
    b = k[j]
    pygame.draw.line(screen, white, (a[0], a[1]), (b[0], b[1]), 2)

run = True
while run:
    clock.tick(fps)
    screen.fill(black)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    key_pressed = pygame.key.get_pressed()
    if key_pressed[pygame.K_w]:
        camera.move(1, 50 * speed)
    if key_pressed[pygame.K_s]:
        camera.move(1, -50 * speed)
    if key_pressed[pygame.K_a]:
        camera.move(0, -50 * speed)
    if key_pressed[pygame.K_d]:
        camera.move(0, 50 * speed)
    if key_pressed[pygame.K_q]:
        camera.move(2, -50 * speed)
    if key_pressed[pygame.K_e]:
        camera.move(2, 50 * speed)

    if key_pressed[pygame.K_UP]:
        camera.rotate(1, speed)
    if key_pressed[pygame.K_DOWN]:
        camera.rotate(1, -speed)
    if key_pressed[pygame.K_LEFT]:
        camera.rotate(0, -speed)
    if key_pressed[pygame.K_RIGHT]:
        camera.rotate(0, speed)
    if key_pressed[pygame.K_r]:
        camera.rotate(2, -speed)
    if key_pressed[pygame.K_f]:
        camera.rotate(2, speed)

    proj_origin = camera.project(np.array([0, 0, 0]))
    # xx = camera.project(np.array([1000, 0, 0]))
    yy = camera.project(np.array([0, 1000, 0]))
    # zz = camera.project(np.array([0, 0, 1000]))
    # pygame.draw.line(screen, (255, 0, 0), proj_origin, xx, 5)
    pygame.draw.line(screen, (0, 255, 0), proj_origin, yy, 5)
    # pygame.draw.line(screen, (0, 0, 255), proj_origin, zz, 5)

    # l = 50
    # plane = (
    #     camera.project(np.array([ l, 0, l])), 
    #     camera.project(np.array([ l, 0,-l])), 
    #     camera.project(np.array([-l, 0,-l])), 
    #     camera.project(np.array([-l, 0, l]))
    #     )
    # pygame.draw.polygon(screen, (255, 0, 0, 50), plane)

    # l = 2
    # cam_pos = np.array(camera.position)
    # camera_plane = (
    #     camera.project(cam_pos + np.array([ l, 0, l])), 
    #     camera.project(cam_pos + np.array([ l, 0,-l])), 
    #     camera.project(cam_pos + np.array([-l, 0,-l])), 
    #     camera.project(cam_pos + np.array([-l, 0, l]))
    #     )
    # pygame.draw.polygon(screen, (255, 0, 0, 50), camera_plane, 2)

    projected_points = [camera.project(point) for point in points]

    #draw cube
    for point in projected_points:
        pygame.draw.circle(screen, blue, point, 5)
    for m in range(4):
        connect_point(m, (m+1)%4, projected_points)
        connect_point(m+4, (m+1)%4 + 4, projected_points)
        connect_point(m, m+4, projected_points)


    text = font.render(f'Pos: {camera.position[0]:2f}, {camera.position[1]:2f}, {camera.position[2]:2f}' +
    f' Rot: {camera.rotation[0]:2f}, {camera.rotation[1]:2f}, {camera.rotation[2]:2f}', True, white)
    screen.blit(text, [0, 0])

    # for i in range(len(points)):
    #     points[i] = points[i] + np.array([0.01, 0.01, 0])

    pygame.display.update()

pygame.quit()