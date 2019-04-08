import pyglet
import re

from typing import List, Tuple
from pyglet.gl import *
from pyglet.window import mouse, key

from globals import REGEX, STRING,\
    RegularExpression, Phrase, ConvexPoly, Model, SpatialRelation, ColorTriple,\
    get_resolution, get_object, get_vertex_3d

# region First Assignment


def first():
    width, height = get_resolution()

    drawn_polygons: List[ConvexPoly] = list()
    drawn_objects: List[pyglet.graphics.vertexdomain.VertexList] = list()
    filled_lines: List[pyglet.graphics.vertexdomain.VertexList] = list()

    assigned_vertices: List[Tuple[int, int]] = list()
    assigned_vertices_vertex_list: List[pyglet.graphics.vertexdomain.VertexList] = list()

    graphics_batch = pyglet.graphics.Batch()
    window = pyglet.window.Window(width=width, height=height)

    @window.event
    def on_mouse_press(mouse_x, mouse_y, button, _):
        # Adds a polygon vertex.
        if button == mouse.LEFT:
            if len(drawn_polygons) is 0:
                assigned_vertices.append((mouse_x, mouse_y))
                assigned_vertices_vertex_list.append(graphics_batch.add(1,
                                                                        GL_POINTS,
                                                                        None,
                                                                        ("v2i", assigned_vertices[-1]),
                                                                        ("c3B", ColorTriple.Green)))

        # Adds a mock point.
        if button == mouse.RIGHT:
            coordinates = (mouse_x, mouse_y)
            drawn_objects.append(graphics_batch.add(1,
                                                    GL_POINTS,
                                                    None,
                                                    ("v2i", coordinates),
                                                    ("c3B", ColorTriple.Magenta)))
            if len(drawn_polygons) is not 0:
                point_relation = drawn_polygons[0].get_relation(coordinates)

                if point_relation == SpatialRelation.Touching:
                    print(STRING[Phrase.LAB2_FirstAssignment_PointTouchingPolygon].format(coordinates))
                else:
                    print(STRING[Phrase.LAB2_FirstAssignment_PointNotTouchingPolygon]
                          .format(coordinates, point_relation.str_croatian()))

                if len(filled_lines) is 0:
                    for line_to_fill in drawn_polygons[0].fill_lines:
                        filled_lines.append(graphics_batch.add(2,
                                                               GL_LINES,
                                                               None,
                                                               ("v2i", line_to_fill),
                                                               ("c3B", (*ColorTriple.White, *ColorTriple.White))))

    @window.event
    def on_key_press(symbol, _):
        # Draws a poly with assigned vertices.
        if symbol == key.RETURN:
            if len(assigned_vertices) < 3:
                print(STRING[Phrase.LAB2_FirstAssignment_CantCreatePolyWithout3Verts].format(len(assigned_vertices)))
            else:
                for point in assigned_vertices_vertex_list:
                    point.delete()

                assigned_vertices_vertex_list.clear()

                convex_polygon = ConvexPoly(assigned_vertices)

                for vertex_pair in convex_polygon.edge_lines:
                    drawn_objects.append(graphics_batch.add(2,
                                                            GL_LINES,
                                                            None,
                                                            ("v2i", vertex_pair),
                                                            ("c3B", (*ColorTriple.Red, *ColorTriple.Red))))

                assigned_vertices.clear()
                drawn_polygons.append(convex_polygon)

        # Deletes the last drawn object.
        if symbol == key.DELETE:
            if len(filled_lines) is not 0:
                for filled_line in filled_lines:
                    filled_line.delete()

                filled_lines.clear()
            elif len(drawn_objects) is not 0:
                drawn_objects[-1].delete()
                drawn_objects.pop()

                if len(drawn_objects) is 0:
                    drawn_polygons.clear()
            else:
                print(STRING[Phrase.LAB2_FirstAssignment_CantDeleteNothing])

    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)
        graphics_batch.draw()

    pyglet.app.run()

    print("\n")


# endregion

# region Second Assignment


def second():
    object_string = get_object()

    if object_string is None:
        print()
        return

    model = Model(object_string)
    width, height = get_resolution()
    vertex = get_vertex_3d()

    graphics_batch = pyglet.graphics.Batch()
    window = pyglet.window.Window(width=width, height=height)

    draw_list = model.get_draw_list(*(model.get_translation_and_scaling((width, height))))

    for triangle in draw_list:
        graphics_batch.add_indexed(3,
                                   GL_LINES,
                                   None,
                                   [0, 1, 1, 2, 2, 0],
                                   ("v2f", triangle))

    print(STRING[Phrase.LAB2_SecondAssignment_PointNotTouchingModel].format(vertex,
                                                                            model.get_relation(vertex).str_croatian()))

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
