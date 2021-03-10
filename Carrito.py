from OpenGL.GL import *
from glew_wish import *
import glfw
from math import *


class Carrito:
    posicionX = 0.0
    posicionY = -0.8
    angulo = 0
    desfase= 90
    velocidad = 1
    velocidad_angular = 180
    disparando = False 
    colisionando = False

    def dibujar(self):
        
        glPushMatrix()
        glTranslate(self.posicionX, self.posicionY, 0.0)
        glRotate(self.angulo, 0.0, 0.0, 1.0)
        glBegin(GL_TRIANGLES)
        if self.colisionando == True:
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(1.0, 0.0, 0.0)
        glVertex3f(0.0, 0.05, 0.0)
        glVertex3f(-0.05, -0.05, 0.0)
        glVertex3f(0.05, -0.05, 0.0)
        glEnd()
        glPopMatrix()

    def actualizar(self, window, tiempo_delta):
        

        estadoIzquierda = glfw.get_key(window, glfw.KEY_LEFT)
        estadoDerecha = glfw.get_key(window, glfw.KEY_RIGHT)
        estadoAbajo = glfw.get_key(window, glfw.KEY_DOWN)
        estadoArriba = glfw.get_key(window, glfw.KEY_UP)

        if estadoIzquierda == glfw.PRESS:
            self.angulo = self.angulo + (self.velocidad_angular * tiempo_delta)
            if self.angulo > 360:
                self.angulo = 0

        if estadoDerecha == glfw.PRESS:
            self.angulo = self.angulo - (self.velocidad_angular * tiempo_delta)
            if self.angulo < 0:
                self.angulo = 360

        if estadoArriba == glfw.PRESS:
            self.posicionY = self.posicionY + \
                (sin((self.angulo + self.desfase) * 3.14159 / 180) * self.velocidad * tiempo_delta)
            self.posicionX = self.posicionX + \
                (cos((self.angulo + self.desfase) * 3.14159 / 180) * self.velocidad * tiempo_delta)