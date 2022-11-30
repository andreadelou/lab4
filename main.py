import numpy
import random
import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import *
import glm
from obj import *

pygame.init()

screen = pygame.display.set_mode(
    (800, 800),
    pygame.OPENGL | pygame.DOUBLEBUF
)
# dT = pygame.time.Clock()



vertex_shader = """
#version 460
layout (location = 0) in vec3 position;
layout (location = 1) in vec3 vertexColor;
uniform mat4 amatrix;
out vec3 ourColor;
out vec2 fragCoord;
void main()
{
    gl_Position = amatrix * vec4(position, 1.0f);
    ourColor = vertexColor;
    fragCoord = gl_Position.xy;
}
"""

fragment_shader = """
#version 460

layout (location = 0) out vec4 fragColor;

uniform vec3 color;
in vec3 ourColor;

void main()
{
    // fragColor = vec4(ourColor, 1.0f);
    fragColor = vec4(color, 1.0f);
}
"""

compiled_vertex_shader = compileShader(vertex_shader, GL_VERTEX_SHADER)
compiled_fragment_shader = compileShader(fragment_shader, GL_FRAGMENT_SHADER)


shader = compileProgram(compiled_vertex_shader, compiled_fragment_shader)
# shader2 = compileProgram(compiled_vertex_shader, compiled_fragment_shader2)


glUseProgram(shader)

glEnable(GL_DEPTH_TEST)

obj = Obj("silla.obj")


faces = []
for face in obj.faces:
    for f in face:
        faces.append(int(f[0]) - 1)

index_data = numpy.array(faces, dtype=numpy.int32)

vertex_array_object = glGenVertexArrays(1)
glBindVertexArray(vertex_array_object)

vertex_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vertex_buffer_object)


element_buffer_object = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, element_buffer_object)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

def calculateMatrix(angle, new_vec):
    i = glm.mat4(1)
    translate = glm.translate(i, glm.vec3(0, -0.5, 0))
    rotate = glm.rotate(i, glm.radians(angle), new_vec)
    scale = glm.scale(i, glm.vec3(1, 1, 1))

    model = translate * rotate * scale

    view = glm.lookAt(glm.vec3(0, 0, 2), glm.vec3(0, 0, 0), glm.vec3(0, 1, 0))

    projection = glm.perspective(glm.radians(45), 1600 / 1200, 0.1, 1000.0)

    glViewport(0, 0, 1000, 800)

    amatrix = projection * view * model

    glUniformMatrix4fv(
        glGetUniformLocation(shader, "amatrix"), 1, GL_FALSE, glm.value_ptr(amatrix)
    )


running = True

glClearColor(0, 0, 0, 1.0)

angle = 0
new_vec = glm.vec3(0, 1, 0)
prev_time = pygame.time.get_ticks()

current_shader = shader

while running:
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    glUseProgram(current_shader)

    glUniform1f(glGetUniformLocation(shader, "iTime"), angle / 1000)

    glDrawElements(GL_TRIANGLES, len(index_data), GL_UNSIGNED_INT, None)

    calculateMatrix(angle, new_vec)

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_shader = shader
            if event.key == pygame.K_2:
                current_shader = shader2
            if event.key == pygame.K_w:
                new_vec = glm.vec3(1, 0, 0)
                angle += 10
            if event.key == pygame.K_s:
                new_vec = glm.vec3(1, 0, 0)
                angle -= 10
            if event.key == pygame.K_d:
                new_vec = glm.vec3(0, 1, 0)
                angle += 10
            if event.key == pygame.K_a:
                new_vec = glm.vec3(0, 1, 0)
                angle -= 10