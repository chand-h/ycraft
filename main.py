# Minecraft clone
# each block is a chunk and chunk is a block
# like antman and minecraft had a baby
# all around switching scales

# certain mob encounters can deny switching scales

## Infinitium Bird Feather Staff
# Allows users to glide down from the top of the chunk when switching scales




import pygame
import numpy as np
import keyboard
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

_CHUNK_SIZE = 4

class Block:
    def __init__(self, chunk_pos, id):
        self.chunk_pos = chunk_pos
        self.id = id


class ChunkData:
    
    items = list()
    for i in range(_CHUNK_SIZE * _CHUNK_SIZE * _CHUNK_SIZE):
        items.append(0)
    
    def get_items(self):
        return self.items

class Chunk:
    def __init__(self, pos, items):
        self.pos = pos
        self.items = items

    def draw(self):
        for idx, i in enumerate(self.items):
            Cube((self.pos[0] * _CHUNK_SIZE + (idx % _CHUNK_SIZE ** 2) // _CHUNK_SIZE, self.pos[1] * _CHUNK_SIZE + (idx // _CHUNK_SIZE // _CHUNK_SIZE), self.pos[2] * _CHUNK_SIZE + idx % _CHUNK_SIZE ^ 2), i)

def init_gl(display):
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    
    # Set up the projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(55, (display[0]/display[1]), 0.1, 300.0)
    
    # Switch back to model view matrix
    glMatrixMode(GL_MODELVIEW)



class Camera:
    def __init__(self, position=[0, 0, -5], yaw=0, pitch=0):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.speed = 5.0
        self.mouse_sensitivity = 0.1

    def update_camera(self):
        glLoadIdentity()
        gluLookAt(self.position[0], self.position[1], self.position[2],
            self.position[0] + np.cos(np.radians(self.pitch)) * np.sin(np.radians(self.yaw)),
            self.position[1] + np.sin(np.radians(self.pitch)),
            self.position[2] + np.cos(np.radians(self.pitch)) * np.cos(np.radians(self.yaw)),
            0, 1, 0)
        #print(self.position[0:3])

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
vertices=( (1, -1, -1),
    (1, 1, -1),
    (-1, 1, -1),
    (-1, -1, -1),
    (1, -1, 1),
    (1, 1, 1),
    (-1, -1, 1),
    (-1, 1, 1))
##define 12 edges for the body
edges = (
    (0,1),
    (0,3),
    (0,4),
    (2,1),
    (2,3),
    (2,7),
    (6,3),
    (6,4),
    (6,7),
    (5,1),
    (5,4),
    (5,7)
    )

def create_cube_vbo():
    vertices = [...]  # Define your cube vertices and normals
    vbo_id = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo_id)
    glBufferData(GL_ARRAY_BUFFER, np.array(vertices, dtype='float32'), GL_STATIC_DRAW)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    return vbo_id

# # Initialization
# cube_vbo = create_cube_vbo()

# # To draw
# glBindBuffer(GL_ARRAY_BUFFER, cube_vbo)
# # Set up vertex arrays or enable client states here depending on your version of OpenGL
# for i in range(_CHUNK_SIZE ^ 3):
#     glPushMatrix()
#     # Apply transformation here
#     glTranslate(x, y, z)  # Example transformation
#     glDrawArrays(GL_TRIANGLES, 0, len(vertices) // stride)  # Adjust based on your vertex format
#     glPopMatrix()
# glBindBuffer(GL_ARRAY_BUFFER, 0)



##define function to draw the cube
def Cube(pos, id):
    #print(pos)
    glBegin(GL_LINES)
    glColor3fv((1,id,1))
    for edge in edges:
        for index in edge:
            glVertex3f(*tuple(a * 0.5 + b for a, b in zip(vertices[index], pos)))
    glEnd()


cd = ChunkData()
chunk_set = list()
chunk_set.append(Chunk((0,0,0), cd.items))
chunk_set.append(Chunk((1,0,0), cd.items))
chunk_set.append(Chunk((0,1,0), cd.items))
chunk_set.append(Chunk((1,1,1), cd.items))
chunk_set.append(Chunk((3,3,3), cd.items))
chunk_set.append(Chunk((2,3,3), cd.items))
chunk_set.append(Chunk((3,2,3), cd.items))
chunk_set.append(Chunk((2,2,2), cd.items))
chunk_set.append(Chunk((3,3,0), cd.items))
chunk_set.append(Chunk((0,3,3), cd.items))
#chunk_set.append(Chunk((3,3,3), cd.items))
#chunk_set.append(Chunk((3,0,3), cd.items))



##Define main function to draw a window for the openGL
def main():
    pygame.init()
    display=(600,600)
    init_gl(display)
    camera = Camera()
    camera.update_camera()
    clock = pygame.time.Clock()
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)  # Hide the mouse cursor

    while True:
        dt = clock.tick() / 1000
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
            if keyboard.is_pressed('x'):
                camera.move_up(dt)
            if keyboard.is_pressed('z'):
                camera.move_down(dt)
            

        mouse_dx, mouse_dy = pygame.mouse.get_rel()
        camera.yaw -= mouse_dx * camera.mouse_sensitivity
        camera.pitch -= mouse_dy * camera.mouse_sensitivity
        camera.pitch = max(-89, min(89, camera.pitch))  # Limit pitch to prevent flipping

        
        camera.update_camera()
        #glRotatef(1, 3, 1, 1)
        
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        for c in chunk_set:
            c.draw()
        # Cube((0,0,0),1)
        # Cube((1,1,0),1)
        
        pygame.display.flip()
        pygame.time.wait(10)


main()