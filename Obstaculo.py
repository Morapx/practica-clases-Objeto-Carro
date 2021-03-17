from glew_wish import *
import glfw
from math import *

class Obstaculo:
    posicionX = 0.0
    posicionY = 0.0
    vivo = True

    def __init__(self, x, y):
        self.posicionX = x
        self.posicionY = y

    def dibujar(self):
        if self.vivo:
            glPushMatrix()
            glTranslate(self.posicionX, self.posicionY, 0.0)
            glBegin(GL_QUADS)
            glColor3f(0.0, 0.0, 1.0)
            glVertex(-0.15, 0.15, 0.0)
            glVertex(0.15, 0.15, 0.0)
            glVertex(0.15, -0.15, 0.0)
            glVertex(-0.15, -0.15, 0.0)
            glEnd()
            glPopMatrix()