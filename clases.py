from OpenGL.GL import *
from glew_wish import *
import glfw
from math import *
from Carrito import *
from Obstaculo import *
from Bala import *

tiempo_anterior = 0

carrito = Carrito()

obstaculos = []

def iniciaizarObstaculos():
    global obstaculos
    obstaculos.append(Obstaculo(0.4, 0.6))
    obstaculos.append(Obstaculo(-0.5, 0.3))
    obstaculos.append(Obstaculo(0.5, -0.1))
 
def actualizar(window):
    global tiempo_anterior
    global carrito

    tiempo_actual = glfw.get_time()
    tiempo_delta = tiempo_actual - tiempo_anterior

    carrito.actualizar(window, tiempo_delta)
    
    for obstaculo in obstaculos:
        if obstaculo.vivo:
            carrito.checar_colisiones(obstaculo)
            if carrito.colisionando:
                break

    tiempo_anterior = tiempo_actual

def dibujar():
    global carrito
    global obstaculos
    # rutinas de dibujo
    for obstaculo in obstaculos:
        obstaculo.dibujar()
    carrito.dibujar()


def key_callback(window, key, scancode, action, mods):
    global carrito
    if not carrito.disparando and key == glfw.KEY_SPACE and action == glfw.PRESS:
        carrito.disparar()


def main():
    # inicia glfw
    if not glfw.init():
        return

    # crea la ventana,
    # independientemente del SO que usemos
    window = glfw.create_window(800, 800, "Mi ventana", None, None)
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

    iniciaizarObstaculos()

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