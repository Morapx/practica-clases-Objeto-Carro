from OpenGL.GL import *
from glew_wish import *
import glfw
from math import *

xObstaculo = 0.0
yObstaculo = 0.6
obstaculoVivo = True

xCarrito = 0.0
yCarrito = -0.8

colisionando = False

angulo = 0
# el desfase es debido a que el triangulo en 0 grados voltea
# hacia arriba y no hacia la derecha
desfase = 90

velocidad = 1
velocidad_angular = 180

tiempo_anterior = 0

# Indicador si hay "bala" viva o no
disparando = False
xBala = 0
yBala = 0


def actualizar_bala(tiempo_delta):
    global disparando
    global xBala
    global yBala
    global anguloBala
    global velocidad
    global obstaculoVivo
    if disparando:
        if xBala >= 1:
            disparando = False
        elif xBala <= -1:
            disparando = False
        elif yBala >= 1:
            disparando = False
        elif yBala <= -1:
            disparando = False
        print("Disparando")
        yBala = yBala + \
            (sin((anguloBala + desfase) * 3.14159 / 180) * velocidad * tiempo_delta)
        xBala = xBala + \
            (cos((anguloBala + desfase) * 3.14159 / 180) * velocidad * tiempo_delta)
        # checar colision con obstaculo si sigue "vivo"
        if obstaculoVivo and xBala + 0.01 > xObstaculo - 0.15 and xBala - 0.01 < xObstaculo + 0.15 and yBala + 0.01 > yObstaculo - 0.15 and yBala - 0.01 < yObstaculo + 0.15:
            obstaculoVivo = False
            disparando = False


def checar_colisiones():
    global colisionando
    # Si extremaDerechaCarrito > extremaIzquierdaObstaculo
    # Y extremaIzquierdaCarrito < extremaDerechaObstaculo
    # Y extremoSuperiorCarrito > extremoInferiorObstaculo
    # Y extremoInferiorCarrito < extremoSuperiorObstaculo
    if xCarrito + 0.05 > xObstaculo - 0.15 and xCarrito - 0.05 < xObstaculo + 0.15 and yCarrito + 0.05 > yObstaculo - 0.15 and yCarrito - 0.05 < yObstaculo + 0.15:
        colisionando = True
    else:
        colisionando = False


def actualizar(window):
    global tiempo_anterior
    global angulo
    global xCarrito
    global yCarrito

    tiempo_actual = glfw.get_time()
    tiempo_delta = tiempo_actual - tiempo_anterior

    estadoIzquierda = glfw.get_key(window, glfw.KEY_LEFT)
    estadoDerecha = glfw.get_key(window, glfw.KEY_RIGHT)
    estadoAbajo = glfw.get_key(window, glfw.KEY_DOWN)
    estadoArriba = glfw.get_key(window, glfw.KEY_UP)

    if estadoIzquierda == glfw.PRESS:
        angulo = angulo + (velocidad_angular * tiempo_delta)
        if angulo > 360:
            angulo = 0
    if estadoDerecha == glfw.PRESS:
        angulo = angulo - (velocidad_angular * tiempo_delta)
        if angulo < 0:
            angulo = 360

    if estadoArriba == glfw.PRESS:
        yCarrito = yCarrito + \
            (sin((angulo + desfase) * 3.14159 / 180) * velocidad * tiempo_delta)
        xCarrito = xCarrito + \
            (cos((angulo + desfase) * 3.14159 / 180) * velocidad * tiempo_delta)

    checar_colisiones()
    actualizar_bala(tiempo_delta)
    tiempo_anterior = tiempo_actual


def dibujarObstaculo():
    global xObstaculo
    global yObstaculo

    if obstaculoVivo:
        glPushMatrix()
        glTranslate(xObstaculo, yObstaculo, 0.0)
        glBegin(GL_QUADS)
        glColor3f(0.0, 0.0, 1.0)
        glVertex(-0.15, 0.15, 0.0)
        glVertex(0.15, 0.15, 0.0)
        glVertex(0.15, -0.15, 0.0)
        glVertex(-0.15, -0.15, 0.0)
        glEnd()
        glPopMatrix()


def dibujar_bala():
    global disparando
    global xBala
    global yBala
    if disparando == True:
        glPushMatrix()
        glTranslate(xBala, yBala, 0.0)
        glRotate(anguloBala, 0.0, 0.0, 1.0)
        glBegin(GL_QUADS)
        glColor3f(1.0, 1.0, 1.0)
        glVertex3f(-0.01, 0.01, 0.0)
        glVertex3f(0.01, 0.01, 0.0)
        glVertex3f(0.01, -0.01, 0.0)
        glVertex3f(-0.01, -0.01, 0.0)
        glEnd()
        glPopMatrix()


def dibujarCarrito():
    global colisionando
    global xCarrito
    global yCarrito
    glPushMatrix()
    glTranslate(xCarrito, yCarrito, 0.0)
    glRotate(angulo, 0.0, 0.0, 1.0)
    glBegin(GL_TRIANGLES)
    if colisionando == True:
        glColor3f(1.0, 1.0, 1.0)
    else:
        glColor3f(1.0, 0.0, 0.0)
    glVertex3f(0.0, 0.05, 0.0)
    glVertex3f(-0.05, -0.05, 0.0)
    glVertex3f(0.05, -0.05, 0.0)
    glEnd()
    glPopMatrix()


def dibujar():
    # rutinas de dibujo
    dibujarObstaculo()
    dibujarCarrito()
    dibujar_bala()


def key_callback(window, key, scancode, action, mods):
    global disparando
    global anguloBala
    global xBala
    global yBala
    if not disparando and key == glfw.KEY_SPACE and action == glfw.PRESS:
        disparando = True
        xBala = xCarrito
        yBala = yCarrito
        anguloBala = angulo


def main():
    # inicia glfw
    if not glfw.init():
        return

    # crea la ventana,
    # independientemente del SO que usemos
    window = glfw.create_window(800, 800, "Mi ventana", None, None)

    # Configuramos OpenGL
    glfw.window_hint(glfw.SAMPLES, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    # Validamos que se cree la ventana
    if not window:
        glfw.terminate()
        return
    # Establecemos el contexto
    glfw.make_context_current(window)

    # Activamos la validación de
    # funciones modernas de OpenGL
    glewExperimental = True

    # Inicializar GLEW
    if glewInit() != GLEW_OK:
        print("No se pudo inicializar GLEW")
        return

    # Obtenemos versiones de OpenGL y Shaders
    version = glGetString(GL_VERSION)
    print(version)

    version_shaders = glGetString(GL_SHADING_LANGUAGE_VERSION)
    print(version_shaders)

    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        # Establece regiond e dibujo
        glViewport(0, 0, 800, 800)
        # Establece color de borrado
        glClearColor(0.4, 0.8, 0.1, 1)
        # Borra el contenido de la ventana
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Dibujar
        actualizar(window)
        dibujar()

        # Preguntar si hubo entradas de perifericos
        # (Teclado, mouse, game pad, etc.)
        glfw.poll_events()
        # Intercambia los buffers
        glfw.swap_buffers(window)

    # Se destruye la ventana para liberar memoria
    glfw.destroy_window(window)
    # Termina los procesos que inició glfw.init
    glfw.terminate()


if __name__ == "__main__":
    main()