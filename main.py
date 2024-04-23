import pygame
import math
import sys

pygame.init()


class Chunk:
    def __init__(self, pos):
        self.contents = [] * 4096
        self.contents[0:2047] = Block(pos, 0, self)
        self.contents[2048:4095] = Block(pos, 1, self)

    def set_block(self, pos, id):
        self.contents[pos[0] * 256 + pos[1] * 16 + pos[2]] = id


class Block:
    def __init__(self, chunk_pos, chunk):
        self.id = 0
        self.chunk_pos = chunk_pos
        self.chunk = chunk


# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Cube points
points = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
]


def perspective_projection(point, d=3):
    """Perspective projection transformation to give a sense of depth."""
    x, y, z = point
    factor = d / (d + z)
    x = x * factor
    y = y * factor
    return [x, y, z]


def rotate_z(theta, points):
    """Rotate points around the Z-axis"""
    new_points = []
    for point in points:
        x, y, z = point
        new_x = x * math.cos(theta) - y * math.sin(theta)
        new_y = x * math.sin(theta) + y * math.cos(theta)
        new_points.append([new_x, new_y, z])
    return new_points


def rotate_y(theta, points):
    """Rotate points around the Y-axis"""
    new_points = []
    for point in points:
        x, y, z = point
        new_x = x * math.cos(theta) + z * math.sin(theta)
        new_z = -x * math.sin(theta) + z * math.cos(theta)
        new_points.append([new_x, y, new_z])
    return new_points


def rotate_x(theta, points):
    """Rotate points around the X-axis"""
    new_points = []
    for point in points:
        x, y, z = point
        new_y = y * math.cos(theta) - z * math.sin(theta)
        new_z = y * math.sin(theta) + z * math.cos(theta)
        new_points.append([x, new_y, new_z])
    return new_points


def draw_cube(points):
    """Draw the edges of the cube"""
    connects = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (5, 6),
        (6, 7),
        (7, 4),
        (0, 4),
        (1, 5),
        (2, 6),
        (3, 7),
    ]
    for connect in connects:
        p1 = perspective_projection(points[connect[0]])
        p2 = perspective_projection(points[connect[1]])
        pygame.draw.line(
            window,
            WHITE,
            (p1[0] * 100 + WIDTH // 2, p1[1] * 100 + HEIGHT // 2),
            (p2[0] * 100 + WIDTH // 2, p2[1] * 100 + HEIGHT // 2),
            1,
        )


def main():
    angle = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        window.fill(BLACK)
        angle += 0.01
        rotated_points = rotate_x(angle, points)
        rotated_points = rotate_y(angle, rotated_points)
        rotated_points = rotate_z(angle, rotated_points)
        draw_cube(rotated_points)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
