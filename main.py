import pygame

import numpy as np
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

_CHUNK_SIZE = 8
_NUM_MACRO_CHUNKS = 3
_TARGET_FPS = 30
_CHUNK_SIZE_SQUARED = _CHUNK_SIZE * _CHUNK_SIZE
_CHUNK_SIZE_CUBED = _CHUNK_SIZE_SQUARED * _CHUNK_SIZE
_DEFAULT_SCALE_FACTOR = _CHUNK_SIZE**_NUM_MACRO_CHUNKS

CAMERA_DEFAULT_SPEED = 0.05 * _DEFAULT_SCALE_FACTOR
CAMERA_SWIFT_SPEED = 10 * CAMERA_DEFAULT_SPEED
CAMERA_SLOW_SPEED = 0.05 * CAMERA_DEFAULT_SPEED
CAMERA_MICRO_SPEED = 0.05 * CAMERA_SLOW_SPEED
CAMERA_NANO_SPEED = 0.05 * CAMERA_MICRO_SPEED


def _pos2idx(pos):
    return pos[0] * _CHUNK_SIZE_SQUARED + pos[1] * _CHUNK_SIZE + pos[2]


def _idx2pos(idx):
    return (
        (idx % _CHUNK_SIZE_SQUARED) // _CHUNK_SIZE,
        idx % _CHUNK_SIZE,
        idx // _CHUNK_SIZE_SQUARED,
    )


class Chunk:
    def __init__(self, pos, parent=None, id=0):
        self.pos = pos
        self.subchunks = np.empty(_CHUNK_SIZE_CUBED, dtype=object)
        self.parent = parent
        self.id = np.int8(id)

    def depth(self):
        pass

    def _realpos(self, depth):
        if self.parent == None:
            return [self.pos[n] * _CHUNK_SIZE_SQUARED for n in range(3)]
        else:
            parent_real = self.parent._realpos(depth - 1)
            return [
                parent_real[n]
                + self.pos[n] / np.float_power(_CHUNK_SIZE, depth - _NUM_MACRO_CHUNKS)
                for n in range(3)
            ]

    def add_child(self, chunk):
        self.subchunks[_pos2idx(chunk.pos)] = chunk
        chunk.parent = self

    def draw(self, depth=0):
        if self != None:
            for i in self.subchunks:
                if i != None:
                    i.draw(depth + 1)
            if self.id != 0:
                Cube(self._realpos(depth), self.id, depth)


def init_gl(display):
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    # Set up the projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55, (display[0] / display[1]), 0.00001, 3000.0)

    # Switch back to model view matrix
    glMatrixMode(GL_MODELVIEW)


#  (_CHUNK_SIZE** _NUM_MACRO_CHUNKS)


class Camera:
    def __init__(self, position=[0.5 * 1, 1.5 * 1, -0.5 * 1], yaw=0, pitch=0):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.speed = CAMERA_DEFAULT_SPEED
        self.mouse_sensitivity = 0.1
        self.velocity = np.zeros(3, dtype=float)

    def move_camera(self):
        norm = np.linalg.norm(self.velocity)
        if norm == 0:
            return
        self.velocity = self.velocity / norm

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


def handle_input(dt, camera):
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 2:
                camera.speed = CAMERA_DEFAULT_SPEED
            if event.button == 3:
                camera.speed = CAMERA_DEFAULT_SPEED
            if event.button == 1:
                camera.speed = CAMERA_DEFAULT_SPEED
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 2:
                camera.speed = CAMERA_NANO_SPEED
            if event.button == 3:
                camera.speed = CAMERA_SLOW_SPEED
            if event.button == 1:
                camera.speed = CAMERA_MICRO_SPEED

    camera.velocity = np.array([0, 0, 0], dtype=float)
    rad_yaw = np.radians(camera.yaw)
    forward = np.array([np.sin(rad_yaw), 0, np.cos(rad_yaw)])
    right = np.array([np.cos(rad_yaw), 0, -np.sin(rad_yaw)])

    if keys[pygame.K_w]:
        camera.velocity += forward
    if keys[pygame.K_s]:
        camera.velocity -= forward
    if keys[pygame.K_a]:
        camera.velocity += right
    if keys[pygame.K_d]:
        camera.velocity -= right
    if keys[pygame.K_SPACE]:
        camera.velocity[1] += 1
    if keys[pygame.K_LSHIFT]:
        camera.velocity[1] -= 1

    norm = np.linalg.norm(camera.velocity)
    if norm == 0:
        return
    else:
        camera.velocity = camera.velocity / norm
        camera.position += camera.velocity * camera.speed * dt


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
    (0.5, 0.0, 0.5),  # Purple
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


def init_font(font_path, size):
    try:
        font = pygame.font.Font(font_path, size)
        print("Font loaded successfully.")
        return font
    except IOError:
        print("Font file not found.")
        return pygame.font.Font(None, size)  # Fallback to the default font


def create_text_texture(text, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)
    glTexImage2D(
        GL_TEXTURE_2D,
        0,
        GL_RGBA,
        text_surface.get_width(),
        text_surface.get_height(),
        0,
        GL_RGBA,
        GL_UNSIGNED_BYTE,
        text_data,
    )
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    return texture_id, text_surface.get_width(), text_surface.get_height()


def draw_text(texture_id, width, height, window_width, window_height):
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, window_width, 0, window_height)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glBindTexture(GL_TEXTURE_2D, texture_id)
    glEnable(GL_TEXTURE_2D)
    glColor3f(1.0, 1.0, 1.0)  # Ensure the text color is white
    glBegin(GL_QUADS)
    x, y = (
        window_width - width - 10,
        window_height - height - 10,
    )  # 10px offset from top right corner
    glTexCoord2f(0, 1)
    glVertex2f(x, y + height)
    glTexCoord2f(1, 1)
    glVertex2f(x + width, y + height)
    glTexCoord2f(1, 0)
    glVertex2f(x + width, y)
    glTexCoord2f(0, 0)
    glVertex2f(x, y)
    glEnd()
    glDisable(GL_TEXTURE_2D)

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


# chunkGod = Chunk((0, 0, 0), None, 1)
# for idx, subchunk1 in enumerate(chunkGod.subchunks):
#     subchunk1 = Chunk(_idx2pos(idx), chunkGod, 2)
#     # chunkGod.add_child(subchunk1)


chunkGod = Chunk((0, 0, 0), None, 1)
chunkA = Chunk((0, 1, 0), chunkGod, 2)
chunkGod.add_child(chunkA)
chunkA = Chunk((0, 0, 0), chunkGod, 2)
chunkGod.add_child(chunkA)

chunkB = Chunk((0, 1, 0), chunkA, 3)
chunkA.add_child(chunkB)
chunkB = Chunk((0, 0, 0), chunkA, 3)
chunkA.add_child(chunkB)
chunkC = Chunk((0, 0, 0), chunkB, 4)
chunkB.add_child(chunkC)
chunkC = Chunk((0, 1, 0), chunkB, 4)
chunkB.add_child(chunkC)

chunkD = Chunk((0, 0, 0), chunkC, 5)
chunkC.add_child(chunkD)
chunkE = Chunk((0, 0, 0), chunkD, 6)
chunkD.add_child(chunkE)
chunkF = Chunk((0, 0, 0), chunkE, 7)
chunkE.add_child(chunkF)
chunkG = Chunk((0, 0, 0), chunkF, 6)
chunkF.add_child(chunkG)
chunkH = Chunk((0, 0, 0), chunkG, 5)
chunkG.add_child(chunkH)
chunkI = Chunk((0, 0, 0), chunkH, 5)
chunkH.add_child(chunkI)

chunkZ = Chunk((6, 6, 6), chunkB, 1)
chunkC.add_child(chunkZ)
chunkZ = Chunk((7, 6, 6), chunkB, 1)
chunkC.add_child(chunkZ)


##Define main function to draw a window for the openGL
def main():
    pygame.init()
    display = (1800, 1200)
    init_gl(display)
    camera = Camera()
    camera.update_camera()
    clock = pygame.time.Clock()
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

    font = init_font("Micro5Charted-Regular.ttf", 24)
    text, width, height = create_text_texture("Hello, OpenGL!", font)

    while True:
        dt = clock.tick(_TARGET_FPS) / 1000
        fps = clock.get_fps()

        handle_input(dt, camera)

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
        draw_text(text, width, height, display[0], display[1])

        fps_text = font.render(f"FPS: {int(fps)}", True, pygame.Color("white"))
        pygame.display.get_surface().blit(fps_text, (10, 10))

        pygame.display.flip()
        # pygame.time.wait(10)


main()
