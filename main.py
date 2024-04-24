# Minecraft clone
# each block is a chunk and chunk is a block
# like antman and minecraft had a baby
# all about switching scales

# certain mob encounters can deny switching scales, mainly by wizards
# who can also navigate through scale
# but also by quantum creatures, who if any are observing you, your
# equipment won't operate correctly

## Infinitium Bird Feather Staff
# Allows users to glide down from the top of the chunk when switching scales
# position and velocity into realm upon change will be dependent of the position and velocity
# of the staff in the larger dimension. So you can sling yourself into existence.


## Infinitium Rings
# Rare rings held by wizards. Can power tools or be melted down into Infinitium
## Infinitium
# Extremely rare, extremely heavy metal which can be used to alter the fabric of space.

## Elytra
# Item similar to elytra will allow for gliding. The catch however is that elytra will not work
# in the macro layers. It will also not be very good in the classic layer. However speed and control
# will greatly compound throughout the lower layers, allowing smaller players to fly around like bugs
# around larger players. 

## Attacking and tool usage
# Attacking and tool usage in this game will be probably the only physics-based parts of this game.
# Swings on tools, swords, and staffs will use data of the position and velocity of the tool to calculate
# power, damage, what have you. To larger players, it will seem like their tools swing slow, and to
# smaller players, their tools will swing fast.


import pygame
import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

_CHUNK_SIZE = 8
_CHUNK_SIZE_SQUARED = _CHUNK_SIZE * _CHUNK_SIZE
_CHUNK_SIZE_CUBED = _CHUNK_SIZE_SQUARED * _CHUNK_SIZE
_NUM_MACRO_CHUNKS = 2
_DEFAULT_SCALE_FACTOR = (_CHUNK_SIZE** _NUM_MACRO_CHUNKS)


def _pos2idx(pos):
    return pos[0] * _CHUNK_SIZE_SQUARED + pos[1] * _CHUNK_SIZE + pos[2]


class Chunk:
    def __init__(self, pos, parent=None, id=0):
        self.pos = pos
        self.items = np.empty(_CHUNK_SIZE_CUBED, dtype=object)
        self.parent = parent
        self.id = np.int8(id)

    def depth(self):
        pass

    def _realpos(self, depth):
        if self.parent == None:
            return self.pos
        else:
            parent_real = self.parent._realpos(depth - 1)
            return (
                parent_real[0] + self.pos[0] / np.float_power(_CHUNK_SIZE, depth - _NUM_MACRO_CHUNKS),
                parent_real[1] + self.pos[1] / np.float_power(_CHUNK_SIZE, depth - _NUM_MACRO_CHUNKS),
                parent_real[2] + self.pos[2] / np.float_power(_CHUNK_SIZE, depth - _NUM_MACRO_CHUNKS),
            )

    def add_child(self, chunk):
        self.items[_pos2idx(chunk.pos)] = chunk
        chunk.parent = self

    def draw(self, depth=0):
        if self != None:
            for i in self.items:
                if i != None:
                    i.draw(depth + 1)
            if self.id != 0:
                Cube(self._realpos(depth), self.id, depth)


def init_gl(display):
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Set up the projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55, (display[0] / display[1]), 0.001, 300.0)

    # Switch back to model view matrix
    glMatrixMode(GL_MODELVIEW)

#  (_CHUNK_SIZE** _NUM_MACRO_CHUNKS)

class Camera:
    def __init__(self, position=[0.5 * 1, 1.5 * 1, -0.5 * 1], yaw=0, pitch=0):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.speed = 0.2 * _DEFAULT_SCALE_FACTOR
        self.mouse_sensitivity = 0.1

    def update_camera(self):
        glLoadIdentity()
        gluLookAt(
            self.position[0],
            self.position[1],
            self.position[2],
            self.position[0]
            + np.cos(np.radians(self.pitch)) * np.sin(np.radians(self.yaw)),
            self.position[1] + np.sin(np.radians(self.pitch)),
            self.position[2]
            + np.cos(np.radians(self.pitch)) * np.cos(np.radians(self.yaw)),
            0,
            1,
            0,
        )
        # print(self.position[0:3])

    def move_forward(self, dt):
        self.position[0] += np.sin(np.radians(self.yaw)) * self.speed * dt
        self.position[2] += np.cos(np.radians(self.yaw)) * self.speed * dt

    def move_backward(self, dt):
        self.position[0] -= np.sin(np.radians(self.yaw)) * self.speed * dt
        self.position[2] -= np.cos(np.radians(self.yaw)) * self.speed * dt

    def move_right(self, dt):
        self.position[0] -= np.cos(np.radians(self.yaw)) * self.speed * dt
        self.position[2] += np.sin(np.radians(self.yaw)) * self.speed * dt

    def move_left(self, dt):
        self.position[0] += np.cos(np.radians(self.yaw)) * self.speed * dt
        self.position[2] -= np.sin(np.radians(self.yaw)) * self.speed * dt

    def move_up(self, dt):
        self.position[1] += self.speed * dt

    def move_down(self, dt):
        self.position[1] -= self.speed * dt


##Define the vertices. usually a cube contains 8 vertices
vertices = (
    (1, 0, 0),
    (1, 1, 0),
    (0, 1, 0),
    (0, 0, 0),
    (1, 0, 1),
    (1, 1, 1),
    (0, 0, 1),
    (0, 1, 1),
)
##define 12 edges for the body
edges = (
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 3),
    (6, 4),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
)


def create_cube_vbo():
    vertices = [...]  # Define your cube vertices and normals
    vbo_id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
    glBufferData(GL_ARRAY_BUFFER, np.array(vertices, dtype="float32"), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo_id

color_list = [
    (1.0, 0.0, 0.0),  # Red
    (0.0, 1.0, 0.0),  # Green
    (0.0, 0.0, 1.0),  # Blue
    (1.0, 1.0, 0.0),  # Yellow
    (1.0, 0.5, 0.0),  # Orange
    (0.0, 1.0, 1.0),  # Cyan
    (1.0, 0.0, 1.0),  # Magenta
    (0.5, 0.0, 0.5)   # Purple
]


##define function to draw the cube
def Cube(pos, id, depth):
    # print(pos)
    glBegin(GL_LINES)
    glColor3fv(color_list[id])
    for edge in edges:
        for index in edge:
            glVertex3f(
                *tuple(
                    a / np.float_power(_CHUNK_SIZE, depth - _NUM_MACRO_CHUNKS) + b
                    for a, b in zip(vertices[index], pos)
                )
            )
    glEnd()


chunkGod = Chunk((0, 0, 0), None, 1)
chunkA = Chunk((0, 0, 0), chunkGod, 2)
chunkGod.add_child(chunkA)
chunkA = Chunk((0, 1, 0), chunkGod, 2)
chunkGod.add_child(chunkA)

chunkB = Chunk((0, 0, 0), chunkA, 3)
chunkA.add_child(chunkB)
chunkB = Chunk((0, 1, 0), chunkA, 3)
chunkA.add_child(chunkB)
chunkC = Chunk((0, 0, 0), chunkB, 4)
chunkB.add_child(chunkC)
chunkD = Chunk((0, 0, 0), chunkB, 5)
chunkC.add_child(chunkD)


##Define main function to draw a window for the openGL
def main():
    pygame.init()
    display = (1200, 700)
    init_gl(display)
    camera = Camera()
    camera.update_camera()
    clock = pygame.time.Clock()
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)  # Hide the mouse cursor

    while True:
        dt = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            keys = pygame.key.get_pressed()

            if keys[pygame.K_w]:
                camera.move_forward(dt)
            if keys[pygame.K_s]:
                camera.move_backward(dt)
            if keys[pygame.K_a]:
                camera.move_left(dt)
            if keys[pygame.K_d]:
                camera.move_right(dt)
            if keys[pygame.K_SPACE]:
                camera.move_up(dt)
            if keys[pygame.K_LSHIFT]:
                camera.move_down(dt)

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        camera.yaw -= mouse_dx * camera.mouse_sensitivity
        camera.pitch -= mouse_dy * camera.mouse_sensitivity
        camera.pitch = max(
            -89, min(89, camera.pitch)
        )  # Limit pitch to prevent flipping

        camera.update_camera()
        # glRotatef(1, 3, 1, 1)

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        chunkGod.draw()
        # Cube((0,0,0),1)
        # Cube((1,1,0),1)

        pygame.display.flip()
        pygame.time.wait(10)


main()
