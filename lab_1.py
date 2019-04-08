import numpy as np
import pyglet
import re

from typing import List
from pyglet.gl import *
from pyglet.window import mouse

from globals import REGEX, STRING, NUMBER,\
                    RegularExpression, Phrase, Number,\
                    solve_equation_set, get_resolution

# region First Assignment


def first():
    # region Task 1
    left_vector = np.array([2, 3, -4])
    right_vector = np.array([-1, 4, -1])

    v_1 = left_vector - right_vector

    print(STRING[Phrase.LAB1_FirstAssignment_Task1].format(left_vector, right_vector, v_1))
    print()
    # endregion

    # region Task 2
    right_vector = np.array([-1, 4, -1])
    s = v_1 * right_vector

    print(STRING[Phrase.LAB1_FirstAssignment_Task2].format(right_vector, s))
    print()
    # endregion

    # region Task 3
    right_vector = np.array([2, 2, 4])
    v_2 = np.cross(v_1, right_vector)

    print(STRING[Phrase.LAB1_FirstAssignment_Task3].format(right_vector, v_2))
    print()
    # endregion

    # region Task 4
    v_3 = np.linalg.norm(v_2)

    print(STRING[Phrase.LAB1_FirstAssignment_Task4].format(v_3))
    print()
    # endregion

    # region Task 5
    v_4 = -v_2

    print(STRING[Phrase.LAB1_FirstAssignment_Task5].format(v_4))
    print()
    # endregion

    # region Task 6
    left_multidimensional = np.array([[1, 2, 3], [2, 1, 3], [4, 5, 1]])
    right_multidimensional = np.array([[-1, 2, -3], [5, -2, 7], [-4, -1, 3]])

    m_1 = left_multidimensional + right_multidimensional
    m_2 = left_multidimensional + np.transpose(right_multidimensional)
    m_3 = left_multidimensional + np.linalg.inv(right_multidimensional)

    print(STRING[Phrase.LAB1_FirstAssignment_Task6].format(left_multidimensional, right_multidimensional))
    print()
    print(STRING[Phrase.LAB1_FirstAssignment_Task6_1].format(m_1))
    print()
    print(STRING[Phrase.LAB1_FirstAssignment_Task6_2].format(m_2))
    print()
    print(STRING[Phrase.LAB1_FirstAssignment_Task6_3].format(m_3))
    print()

    # endregion

    # region Task 7
    print("{}: ".format(STRING[Phrase.LAB1_FirstAssignment_Task7_EnterEquation]))

    equation_coefficients: List[int or float] = list()
    expected_arguments = ((NUMBER[Number.LAB1_FirstAssignment_Task7_EquationDimensionality] + 1)
                          * NUMBER[Number.LAB1_FirstAssignment_Task7_EquationCount])

    waiting_for = expected_arguments - len(equation_coefficients)

    while waiting_for > 0:
        equation_input = input("{}: ".format(STRING[Phrase.LAB1_FirstAssignment_Task7_EnterFurtherCoefficients]
                                             .format(waiting_for)))

        parsed_input = list(re.split(REGEX[RegularExpression.LAB1_FirstAssignment_Task7_Delimiter], equation_input))

        for entry in parsed_input:

            try:
                equation_coefficients.append(int(str(entry)))
            except ValueError:
                try:
                    equation_coefficients.append(float(str(entry)))
                except ValueError:
                    continue

        waiting_for = expected_arguments - len(equation_coefficients)

    results = solve_equation_set(equation_coefficients, 3)
    print(STRING[Phrase.LAB1_FirstAssignment_Task7_Result].format(results))
    print()
    # endregion

    # region Task 8
    # TODO ispravi baricentrične koordinate u smislu poruke gdje se točka nalazi.
    triangles = list()
    point = list()

    coordinate = ["x", "y", "z"]

    while len(triangles) < 3:
        parsed_input = re.split(REGEX[RegularExpression.LAB1_FirstAssignment_Task8_Delimiter],
                                input("{}: ".format(STRING[Phrase.LAB1_FirstAssignment_Task8_EnterTriangleCoordinates]
                                      .format(coordinate[len(triangles)]))))

        if len(parsed_input) is 3:
            for particle in parsed_input:
                try:
                    float(particle)
                except ValueError:
                    print(STRING[Phrase.LAB1_FirstAssignment_Task8_InvalidTriangleCoordinates])

            triangles.append(list(map(lambda x: float(x), parsed_input)))

    while len(point) is not 3:
        parsed_input = re.split(REGEX[RegularExpression.LAB1_FirstAssignment_Task8_Delimiter],
                                input("{}: ".format(STRING[Phrase.LAB1_FirstAssignment_Task8_EnterPoint])))

        if len(parsed_input) is 3:
            for particle in parsed_input:
                try:
                    float(particle)
                except ValueError:
                    print(STRING[Phrase.LAB1_FirstAssignment_Task8_InvalidPointCoordinates])

            point.extend(list(map(lambda x: float(x), parsed_input)))

    equation_coefficients = list()
    triangles = np.transpose(np.array(triangles))

    for i in range(0, len(triangles)):
        equation_coefficients.extend(triangles[i])
        equation_coefficients.append(point[i])

    baricentric_coordinates = solve_equation_set(equation_coefficients, 3)
    print()
    print(STRING[Phrase.LAB1_FirstAssignment_Task8_Result].format(baricentric_coordinates))

    result = 0
    for coordinate in baricentric_coordinates:
        result += coordinate

    if abs(result) < NUMBER[Number.Universal_SinglePrecisionThreshold]:
        print(STRING[Phrase.LAB1_FirstAssignment_Task8_IsInTriangle].format(point))
    else:
        print(STRING[Phrase.LAB1_FirstAssignment_Task8_IsNotInTriangle].format(point))
    # endregion

    print("\n")

# endregion

# region Second Assignment


def draw_line(batch, starting_vertex, ending_vertex, color_tuple=("c3B", (255, 0, 0, 255, 0, 0))):
    to_draw = list()
    to_draw.extend(starting_vertex)
    to_draw.extend(ending_vertex)
    to_draw = tuple(to_draw)

    batch.add(2, GL_LINES, None, ('v2i', to_draw), color_tuple)


def draw_line_pixel_by_pixel(batch, starting_vertex, ending_vertex):
    # Make sure that starting_vertex is the left-most vertex.
    if starting_vertex[0] > ending_vertex[0]:
        t = list(starting_vertex)

        starting_vertex = list(ending_vertex)
        ending_vertex = t

    # Calculate differentials.
    y_dif = ending_vertex[1] - starting_vertex[1]
    x_dif = ending_vertex[0] - starting_vertex[0]

    points_to_draw = list()

    # If the x differential is 0, we're drawing a vertical line. We will not calculate the gradient to prevent
    # division by 0.
    if x_dif is 0:
        start = min(starting_vertex[1], ending_vertex[1])
        end = max(starting_vertex[1], ending_vertex[1]) + 1

        for i in range(start, end):
            points_to_draw.extend([starting_vertex[0], i])

    # If our y differential is greater than the x differential, we'll handle it differently.
    if abs(y_dif) > abs(x_dif):
        # Firstly, since we're traversing the y-axis, we need the cotangent of the angle.
        coefficient = x_dif / y_dif

        # We'll assume that we're starting with the starting_vertex y value, and ending with the ending_vertex y value.
        start = starting_vertex[1]
        end = ending_vertex[1]
        # Current x will always be the starting_vertex x value since we've already swapped them around.
        current_x = starting_vertex[0]

        # If our start is larger than the end, we want to swap them around, as well as the current_x.
        if start > end:
            t = start
            start = end
            end = t

            current_x = ending_vertex[0]

        # Finally, since range only goes to ending - 1, we need to increment the end by 1.
        end += 1

        for i in range(start, end):
            points_to_draw.extend([int(current_x), i])

            current_x += coefficient
    else:
        # Since our y differential is smaller than our x differential, we can use the regular procedure.
        # First, we calculate the tangent of the angle.
        coefficient = y_dif / x_dif

        # We assume that our start is the starting_vertex x value and our end is the ending_vertex x value.
        # Because we've previously swapped the values around, there should be no special cases like above.
        start = starting_vertex[0]
        end = ending_vertex[0]

        # Like before, because range stops at the last value before the given last value, we need to increment end.
        end += 1
        # Our current_y will be the starting_vertex y value regardless.
        current_y = starting_vertex[1]

        for i in range(start, end):
            points_to_draw.extend([i, int(current_y)])

            current_y += coefficient

    batch.add(int(len(points_to_draw) / 2), GL_POINTS, None, ('v2i', tuple(points_to_draw)))


def second():
    user_input, width, height = None, None, None

    width, height = get_resolution()

    mouse_presses = list()
    graphics_batch = pyglet.graphics.Batch()

    window = pyglet.window.Window(width=width, height=height)

    @window.event
    def on_mouse_press(mouse_x, mouse_y, button, modifier):
        if button == mouse.LEFT:
            if len(mouse_presses) is 0:
                mouse_presses.append((mouse_x, mouse_y))
            elif len(mouse_presses) is 1:
                mouse_presses.append((mouse_x, mouse_y))

                custom_start = [mouse_presses[0][0], mouse_presses[0][1]]
                custom_end = [mouse_presses[1][0], mouse_presses[1][1]]

                starting_vertex = [mouse_presses[0][0],
                                   mouse_presses[0][1] + NUMBER[Number.LAB1_SecondAssignment_LineOffsetY]]
                ending_vertex = [mouse_presses[1][0],
                                 mouse_presses[1][1] + NUMBER[Number.LAB1_SecondAssignment_LineOffsetY]]

                draw_line_pixel_by_pixel(batch=graphics_batch,
                                         starting_vertex=custom_start,
                                         ending_vertex=custom_end)
                draw_line(batch=graphics_batch, starting_vertex=starting_vertex, ending_vertex=ending_vertex)
                mouse_presses.clear()

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

        if re.match(REGEX[RegularExpression.LAB2_FirstAssignmentCommand], user_input):
            first()
        elif re.match(REGEX[RegularExpression.LAB2_SecondAssignmentCommand], user_input):
            second()
        elif re.match(REGEX[RegularExpression.Universal_ExitLoop], user_input):
            exit()
        else:
            print("{}\n".format(STRING[Phrase.Universal_InvalidTaskNumber]))

        user_input = None


main()
