import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF|OPENGL)

# Set up the perspective for the scene
gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

# Move the camera back a bit
glTranslatef(0.0, 0.0, -5)


def Cube():
    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1),
    )

    edges = (
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (4, 5),
        (4, 6),
        (6, 7),
        (7, 5),
        (0, 4),
        (1, 5),
        (3, 6),
        (2, 7)
    )

    colors = (
        (1, 0, 0),  # Red
        (0, 1, 0),  # Green
        (0, 0, 1),  # Blue
        (1, 1, 0),  # Yellow
        (1, 0, 1),  # Magenta
        (0, 1, 1),  # Cyan
        (0.5, 0.5, 0.5),  # Grey
        (1, 0.5, 0),  # Orange
        (0.5, 0, 1),  # Purple
        (1, 1, 1),  # White
        (0, 0.5, 0.5),  # Teal
        (0.5, 0.25, 0.75)  # Pinkish
    )

    glBegin(GL_LINES)
    for i, edge in enumerate(edges):
        glColor3fv(colors[i % len(colors)])
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

rotf = 0.06
def main():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1 * rotf, 3 * rotf, 1 * rotf, 1 * rotf)  # Rotate the cube
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Cube()
        pygame.display.flip()
        pygame.time.wait(10)

if __name__ == "__main__":
    main()
