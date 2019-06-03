import pyglet
import re

from pyglet.gl import *
from pyglet.window import key

from pyglet.graphics import GL_LINES

from globals import STRING, REGEX,\
                    Phrase, RegularExpression, Model,\
                    get_object, get_eye_point, get_viewpoint, get_light_source,\
                    get_fractal_mode, get_mandelbrot, get_julia


# region First Assignment
def first():
    object_string = get_object()

    if object_string is None:
        return

    model = Model(object_string)

    model.normalize_in_space()

    model.set_eye_and_view(get_eye_point(), get_viewpoint())
    resolution = (700, 700)
    model.light_source = get_light_source()

    graphics_batch = pyglet.graphics.Batch()
    window = pyglet.window.Window(width=resolution[0], height=resolution[1])

    drawn_stuff = list()

    half_res = (resolution[0] / 2, resolution[0] / 2)

    print("Pritisnite 1 za žičnu formu, 2 za konstantno sjenčanje, 3 za Gouradovo sjenčanje...")

    @window.event
    def on_key_press(symbol, _):
        if symbol in [key._1, key._2, key._3]:
            for thing in drawn_stuff:
                thing.delete()

            drawn_stuff.clear()

            if symbol == key._1:
                for t in model.get_minimized_vertex_list():
                    t = (t[0][0] * half_res[0] + half_res[0], t[0][1] * half_res[1] + half_res[1],
                         t[1][0] * half_res[0] + half_res[0], t[1][1] * half_res[1] + half_res[1],
                         t[2][0] * half_res[0] + half_res[0], t[2][1] * half_res[1] + half_res[1])

                    drawn_stuff.append(graphics_batch.add_indexed(3,
                                                                  GL_LINES,
                                                                  None,
                                                                  [0, 1, 1, 2, 2, 0],
                                                                  ("v2f", t)))
            elif symbol == key._2:
                draw_lists = model.get_constant_shaded_lists()

                for t, c in zip(draw_lists[0], draw_lists[1]):
                    t = (t[0] * half_res[0] + half_res[0], t[1] * half_res[1] + half_res[1],
                         t[2] * half_res[0] + half_res[0], t[3] * half_res[1] + half_res[1],
                         t[4] * half_res[0] + half_res[0], t[5] * half_res[1] + half_res[1])

                    drawn_stuff.append(graphics_batch.add(3,
                                                          pyglet.gl.GL_TRIANGLES,
                                                          None,
                                                          ("v2f", t),
                                                          ("c3B", c)))
            elif symbol == key._3:
                draw_lists = model.get_variable_shaded_lists()

                for t, c in zip(draw_lists[0], draw_lists[1]):
                    t = (t[0] * half_res[0] + half_res[0], t[1] * half_res[1] + half_res[1],
                         t[2] * half_res[0] + half_res[0], t[3] * half_res[1] + half_res[1],
                         t[4] * half_res[0] + half_res[0], t[5] * half_res[1] + half_res[1])

                    drawn_stuff.append(graphics_batch.add(3,
                                                          pyglet.gl.GL_TRIANGLES,
                                                          None,
                                                          ("v2f", t),
                                                          ("c3B", c)))

            print("Pritisnite 1 za žičnu formu, 2 za konstantno sjenčanje, 3 za Gouradovo sjenčanje...")
        else:
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

    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        graphics_batch.draw()

    pyglet.app.run()

    print("\n")
# endregion


# region Second Assignment
def second():
    resolution = (700, 700)
    fractal_mode = get_fractal_mode()
    epsilon = float(input("Unesite epsilon: "))
    iterations = int(input("Unesite broj iteracija: "))
    u_range = float(input("Unesite u minimum: ")), float(input("Unesite u maksimum: "))
    v_range = float(input("Unesite v minimum: ")), float(input("Unesite v maksimum: "))

    graphics_batch = pyglet.graphics.Batch()
    drawn_stuff = list()

    if fractal_mode is 0:
        draw_list = get_mandelbrot(resolution, u_range, v_range, epsilon, iterations)

    elif fractal_mode is 1:
        c = complex(float(input("Unesite realni dio kompleksnog broja: ")),
             float(input("Unesite imaginaran dio kompleksnog broja: ")))

        draw_list = get_julia(resolution, u_range, v_range, epsilon, iterations, c)
    else:
        return

    window = pyglet.window.Window(width=resolution[0], height=resolution[1])

    for t, c in zip(draw_list[0], draw_list[1]):
        drawn_stuff.append(graphics_batch.add(1,
                                              GL_POINTS,
                                              None,
                                              ("v2f", t),
                                              ("c3B", c)))

    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        graphics_batch.draw()

    pyglet.app.run()

    print("\n")
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
