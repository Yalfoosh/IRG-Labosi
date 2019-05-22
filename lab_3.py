import pyglet
import re

from pyglet.gl import *
from pyglet.window import key

from pyglet.graphics import GL_LINES

from globals import STRING, REGEX,\
                    Phrase, RegularExpression, Model,\
                    get_object, get_resolution, get_eye_point, get_viewpoint, get_bezier


# region First Assignment
def first():
    object_string = get_object()

    if object_string is None:
        return

    model = Model(object_string)
    model.set_eye_and_view(get_eye_point(), get_viewpoint())
    resolution = get_resolution()

    graphics_batch = pyglet.graphics.Batch()
    window = pyglet.window.Window(width=resolution[0], height=resolution[1])

    draw_list = model.get_viewpoint_draw_list()
    drawn_vertices = list()

    for triangle in draw_list:
        drawn_vertices.append(graphics_batch.add_indexed(3,
                                                         GL_LINES,
                                                         None,
                                                         [0, 1, 1, 2, 2, 0],
                                                         ("v2f", triangle)))

    @window.event
    def on_key_press(symbol, _):
        eye_point = list(model.eye_point)
        viewpoint = list(model.viewpoint)

        print(eye_point, viewpoint)

        # region Eye Point Change
        if symbol == key.W:
            eye_point[2] += 1

        if symbol == key.A:
            eye_point[0] -= 1

        if symbol == key.S:
            eye_point[2] -= 1

        if symbol == key.D:
            eye_point[0] += 1

        if symbol == key.LCTRL:
            eye_point[1] -= 1

        if symbol == key.SPACE:
            eye_point[1] += 1
        # endregion

        # region Viewpoint Change
        if symbol == key.UP:
            viewpoint[2] += 1

        if symbol == key.LEFT:
            viewpoint[0] -= 1

        if symbol == key.DOWN:
            viewpoint[2] -= 1

        if symbol == key.RIGHT:
            viewpoint[0] += 1

        if symbol == key.RCTRL:
            viewpoint[1] -= 1

        if symbol == key.NUM_0:
            viewpoint[1] += 1
        # endregion

        model.set_eye_and_view(eye_point, viewpoint)

        for thing in drawn_vertices:
            thing.delete()

        drawn_vertices.clear()

        for tri in model.get_viewpoint_draw_list():
            drawn_vertices.append(graphics_batch.add_indexed(3,
                                                             GL_LINES,
                                                             None,
                                                             [0, 1, 1, 2, 2, 0],
                                                             ("v2f", tri)))

    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        graphics_batch.draw()

    pyglet.app.run()

    print("\n")
# endregion


# region Second Assignment
def second():
    vertices = list()

    with open("z2.tocke") as f:
        for line in f.readlines():
            vertices.append(list(map(lambda x: float(x), line.split())))

    print(vertices)

    poly_batch = pyglet.graphics.Batch()
    curve_batch = pyglet.graphics.Batch()

    window = pyglet.window.Window(*get_resolution())

    for i in range(0, len(vertices) - 1):
        poly_batch.add(2, pyglet.gl.GL_LINES, None, ("v2f",
                                                     (vertices[i][0], vertices[i][1],
                                                      vertices[i+1][0], vertices[i+1][1])))

    bezier_dots = get_bezier(vertices)

    for vertex in bezier_dots:
        curve_batch.add(1, pyglet.gl.GL_POINTS, None, ("v2f", (vertex[0], vertex[1])), ("c3B", (255, 0, 0)))

    @window.event
    def on_draw():
        window.clear()
        poly_batch.draw()
        curve_batch.draw()

    pyglet.app.run()
# endregion


def main():
    user_input = None

    while user_input is None:
        user_input = input("{}: ".format(STRING[Phrase.Universal_EnterTaskNumber]))

        if re.match(REGEX[RegularExpression.LAB3_FirstAssignmentCommand], user_input):
            first()
        elif re.match(REGEX[RegularExpression.LAB3_SecondAssignmentCommand], user_input):
            second()
        elif re.match(REGEX[RegularExpression.Universal_ExitLoop], user_input):
            exit()
        else:
            print("{}\n".format(STRING[Phrase.Universal_InvalidTaskNumber]))

        user_input = None


main()
