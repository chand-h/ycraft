import pygame
import math
import sys

pygame.init()
# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60

# Set up the display
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Block:
    def __init__(self, x, y, z, block_type):
        self.x = x
        self.y = y
        self.z = z
        self.block_type = block_type  # Additional properties like block type can be added here

    def draw(self, surface, camera, points):
        # Here you would translate these points based on block's position
        draw_block(surface, translate_points(points, camera, self.x, self.y, self.z))

class Chunk:
    def __init__(self, pos_x, pos_y, pos_z, width, height, depth):
        self.blocks = [[[Block(x, y, z, 'air') for z in range(depth)] for y in range(height)] for x in range(width)]
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.pos_z = pos_z

    def draw(self, surface, camera, points):
        for x in range(len(self.blocks)):
            for y in range(len(self.blocks[0])):
                for z in range(len(self.blocks[0][0])):
                    self.blocks[x][y][z].draw(surface, camera, points)

def translate_points(base_points, camera, x, y, z):
    translated = []
    for point in base_points:
        translated.append([point[0] + x, point[1] + y, point[2] + z])
    return translated

class Camera:
    def __init__(self, x, y, z):
        self.position = [x, y, z]
        self.yaw = 0
        self.pitch = 0
        self.speed = 0.1
        self.mouse_sensitivity = 0.2

    def move(self, direction, amount):
        if direction == "forward":
            self.position[0] += math.sin(math.radians(self.yaw)) * amount
            self.position[2] += math.cos(math.radians(self.yaw)) * amount
        elif direction == "backward":
            self.position[0] -= math.sin(math.radians(self.yaw)) * amount
            self.position[2] -= math.cos(math.radians(self.yaw)) * amount
        elif direction == "left":
            self.position[0] -= math.cos(math.radians(self.yaw)) * amount
            self.position[2] += math.sin(math.radians(self.yaw)) * amount
        elif direction == "right":
            self.position[0] += math.cos(math.radians(self.yaw)) * amount
            self.position[2] -= math.sin(math.radians(self.yaw)) * amount

    def rotate(self, mouse_dx, mouse_dy):
        self.yaw += mouse_dx * self.mouse_sensitivity
        self.pitch -= mouse_dy * self.mouse_sensitivity
        self.pitch = max(-90, min(90, self.pitch))  # Limit pitch to [-90, 90] degrees


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

def draw_block(surface, points):
    connects = [(0, 1), (1, 2), (2, 3), (3, 0), (4, 5), (5, 6), (6, 7), (7, 4), (0, 4), (1, 5), (2, 6), (3, 7)]
    for connect in connects:
        p1 = perspective_projection(points[connect[0]])
        p2 = perspective_projection(points[connect[1]])
        pygame.draw.line(surface, WHITE, (p1[0] * 100 + WIDTH // 2, p1[1] * 100 + HEIGHT // 2), (p2[0] * 100 + WIDTH // 2, p2[1] * 100 + HEIGHT // 2), 1)

def perspective_projection(point, d=3):
    x, y, z = point
    factor = d / (d + z)
    x = x * factor
    y = y * factor
    return [x, y]

def main():
    pygame.mouse.set_visible(False)  # Hide the cursor
    pygame.event.set_grab(True)  # Confine the cursor to the window

    camera = Camera(0, 0, 0)
    chunk = Chunk(0, 0, 0, 4, 4, 4)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # Handle continuous key presses
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            camera.move("forward", camera.speed)
        if keys[pygame.K_s]:
            camera.move("backward", camera.speed)
        if keys[pygame.K_a]:
            camera.move("left", camera.speed)
        if keys[pygame.K_d]:
            camera.move("right", camera.speed)

        # Handle mouse movement
        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        camera.rotate(mouse_dx, mouse_dy)

        window.fill(BLACK)
        # Here you should modify the chunk drawing method to account for camera position and orientation
        chunk.draw(window, camera, points)  # You need to update this method
 
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
