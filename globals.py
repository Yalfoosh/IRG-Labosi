import numpy as np
import re
import os
import pyglet

from enum import Enum, auto
from math import *
from typing import Any, Dict, List, Tuple

# region Delimiters


class Delimiter(Enum):
    Resolution = auto(),
    Vertex3D = auto(),


DELIMITER: Dict[Delimiter, str] =\
    {
        Delimiter.Resolution: r"\s*(x|,)\s*",
        Delimiter.Vertex3D: r"(\s*,\s*|\s+)",
    }

# endregion

# region Regular Expressions


class RegularExpression(Enum):
    Universal_ExitLoop = auto(),
    Universal_Resolution = auto(),
    Universal_Vertex3D = auto(),

    LAB1_FirstAssignmentCommand = auto(),
    LAB1_SecondAssignmentCommand = auto(),

    LAB1_FirstAssignment_Task7_Delimiter = auto(),
    LAB1_FirstAssignment_Task8_Delimiter = auto(),

    LAB1_SecondAssignment_Resolution = auto(),

    LAB2_FirstAssignmentCommand = auto(),
    LAB2_SecondAssignmentCommand = auto(),

    LAB2_FirstAssignment_Resolution = auto(),

    LAB3_FirstAssignmentCommand = auto(),
    LAB3_SecondAssignmentCommand = auto(),


REGEX: Dict[RegularExpression, str] =\
    {
        RegularExpression.Universal_ExitLoop: r"((?i)(izađi|izlaz|kraj|ugasi|exit|end|shutdown))",
        RegularExpression.Universal_Resolution: r"\d+" + DELIMITER[Delimiter.Resolution] + r"\d+",
        RegularExpression.Universal_Vertex3D: r"(-){0,1}\d+(.*\d*){0,1}" + DELIMITER[Delimiter.Vertex3D]
                                              + r"(-){0,1}\d+(.*\d*){0,1}" + DELIMITER[Delimiter.Vertex3D]
                                              + r"(-){0,1}\d+(.*\d*){0,1}",

        RegularExpression.LAB1_FirstAssignmentCommand: r"((?i)(1|jedan|prva|prvi|one|first))",
        RegularExpression.LAB1_SecondAssignmentCommand: r"((?i)(2|dva|druga|drugi|two|second))",

        RegularExpression.LAB1_FirstAssignment_Task7_Delimiter: r",",
        RegularExpression.LAB1_FirstAssignment_Task8_Delimiter: r",",

        RegularExpression.LAB2_FirstAssignmentCommand: r"((?i)(1|jedan|prva|prvi|one|first))",
        RegularExpression.LAB2_SecondAssignmentCommand: r"((?i)(2|dva|druga|drugi|two|second))",

        RegularExpression.LAB3_FirstAssignmentCommand: r"((?i)(1|jedan|prva|prvi|one|first))",
        RegularExpression.LAB3_SecondAssignmentCommand: r"((?i)(2|dva|druga|drugi|two|second))",
    }

# endregion

# region Strings


class Phrase(Enum):
    Universal_EnterTaskNumber = auto(),
    Universal_InvalidTaskNumber = auto(),

    Universal_EnterResolution = auto(),
    Universal_InvalidResolution = auto(),

    Universal_EnterObjectNameOrNumber = auto(),
    Universal_InvalidObjectNameOrNumber = auto(),
    Universal_ObjectIndexOutOfRange = auto(),
    Universal_NoObjectFilesAtDefaultLocation = auto(),

    Universal_EnterVertex3D = auto(),
    Universal_InvalidVertex3D = auto(),

    Universal_VectorOutput = auto(),
    Universal_VectorOutputShort = auto(),
    Universal_ZeroDimensionalVector = auto(),

    LAB1_FirstAssignment_Task1 = auto(),
    LAB1_FirstAssignment_Task2 = auto(),
    LAB1_FirstAssignment_Task3 = auto(),
    LAB1_FirstAssignment_Task4 = auto(),
    LAB1_FirstAssignment_Task5 = auto(),
    LAB1_FirstAssignment_Task6 = auto(),
    LAB1_FirstAssignment_Task6_1 = auto(),
    LAB1_FirstAssignment_Task6_2 = auto(),
    LAB1_FirstAssignment_Task6_3 = auto(),

    LAB1_FirstAssignment_Task7_EnterEquation = auto(),
    LAB1_FirstAssignment_Task7_EnterFurtherCoefficients = auto(),
    LAB1_FirstAssignment_Task7_Result = auto(),

    LAB1_FirstAssignment_Task8_EnterTriangleCoordinates = auto(),
    LAB1_FirstAssignment_Task8_InvalidTriangleCoordinates = auto(),
    LAB1_FirstAssignment_Task8_EnterPoint = auto(),
    LAB1_FirstAssignment_Task8_InvalidPointCoordinates = auto(),
    LAB1_FirstAssignment_Task8_Result = auto(),
    LAB1_FirstAssignment_Task8_IsInTriangle = auto(),
    LAB1_FirstAssignment_Task8_IsNotInTriangle = auto(),

    LAB2_FirstAssignment_PointTouchingPolygon = auto(),
    LAB2_FirstAssignment_PointNotTouchingPolygon = auto(),

    LAB2_FirstAssignment_CantCreatePolyWithout3Verts = auto(),
    LAB2_FirstAssignment_CantDeleteNothing = auto(),

    LAB2_SecondAssignment_PointTouchingModel = auto(),
    LAB2_SecondAssignment_PointNotTouchingModel = auto(),


class Path(Enum):
    LAB2_ObjectPath = auto(),


STRING: Dict[Phrase, str] =\
    {
        Phrase.Universal_EnterTaskNumber: "Unesite broj vježbe koju želite pokrenuti",
        Phrase.Universal_InvalidTaskNumber: "Pogrešan unos. Pokušajte unos oblika \"1\" ili \"2\". "
                                            "Za izlaz upišite \"izlaz\".",

        Phrase.Universal_EnterResolution: "Unesite rezoluciju odvojenu s \"x\" ili \",\"",
        Phrase.Universal_InvalidResolution: "Neispravan unos rezolucije. Unesite 2 cijela broja odvojena "
                                            "s \"x\" ili \",\".",

        Phrase.Universal_EnterObjectNameOrNumber: "Unesite puno ime .obj datoteke ili pripadajući joj indeks",
        Phrase.Universal_InvalidObjectNameOrNumber: "Krivi unos, pokušajte ponovo.",
        Phrase.Universal_ObjectIndexOutOfRange: "Uneseni indeks bi trebao biti manji ili jednak {} (uneseno {}). "
                                                "Pokupašajte ponovo.",
        Phrase.Universal_NoObjectFilesAtDefaultLocation: "Datoteke koje završavaju na .obj nisu pronađene na "
                                                         "uobičajenoj lokaciji",

        Phrase.Universal_EnterVertex3D: "Unesite trodimenzionalnu točku odvojenu s \",\" ili \" \"",
        Phrase.Universal_InvalidVertex3D: "Neispravan unos trodimenzionalne točke. Unesite 3 realna broja odvojena "
                                            "s \",\" ili \" \".",

        Phrase.Universal_VectorOutput: "({}) = ({})",
        Phrase.Universal_VectorOutputShort: "({})",
        Phrase.Universal_ZeroDimensionalVector: "Vektor dimenzije 0",

        Phrase.LAB1_FirstAssignment_Task1: "v₁ = {} - {} = {}",
        Phrase.LAB1_FirstAssignment_Task2: "s = v₁ · {} = {}",
        Phrase.LAB1_FirstAssignment_Task3: "v₂  = v₁ × {} = {}",
        Phrase.LAB1_FirstAssignment_Task4: "v₃ = |v₂| = {}",
        Phrase.LAB1_FirstAssignment_Task5: "v₄ = -v₂  = {}",
        Phrase.LAB1_FirstAssignment_Task6: "m₁ =\n{}\n\nm₂ =\n{}",
        Phrase.LAB1_FirstAssignment_Task6_1: "M₁ = m₁ + m₂ =\n{}",
        Phrase.LAB1_FirstAssignment_Task6_2: "M₂ = m₁ + m₂ᵀ =\n{}",
        Phrase.LAB1_FirstAssignment_Task6_3: "M₃ = m₁ + m₂⁻¹ =\n{}",

        Phrase.LAB1_FirstAssignment_Task7_EnterEquation: "Unesite koeficijente triju jednadžbi "
                                                         "(u redoslijedu x, y, z, rezultat)",
        Phrase.LAB1_FirstAssignment_Task7_EnterFurtherCoefficients: "Unesite još {} koeficijenata",
        Phrase.LAB1_FirstAssignment_Task7_Result: "[x y z] = {}",

        Phrase.LAB1_FirstAssignment_Task8_EnterTriangleCoordinates: "Unesite točku trokuta {} koordinate",
        Phrase.LAB1_FirstAssignment_Task8_InvalidTriangleCoordinates: "Neispravan unos točke trokuta. "
                                                                      "Unos treba biti oblika \"x, y, z\".",
        Phrase.LAB1_FirstAssignment_Task8_EnterPoint: "Unesite točku za koju želite provjeriti je li u prije navedenom "
                                                      "trokutu",
        Phrase.LAB1_FirstAssignment_Task8_InvalidPointCoordinates: "Neispravan unos točke. Unos treba biti oblika "
                                                                   "\"x, y, z\".",
        Phrase.LAB1_FirstAssignment_Task8_Result: "Baricentrične koordinate zadane točke su {}.",
        Phrase.LAB1_FirstAssignment_Task8_IsInTriangle: "Točka {} nalazi se u trokutu.",
        Phrase.LAB1_FirstAssignment_Task8_IsNotInTriangle: "Točka {} ne nalazi se u trokutu.",

        Phrase.LAB2_FirstAssignment_PointTouchingPolygon: "Točka {} dira mnogokut.",
        Phrase.LAB2_FirstAssignment_PointNotTouchingPolygon: "Točka {} je {} mnogokuta.",
        Phrase.LAB2_FirstAssignment_CantCreatePolyWithout3Verts: "Nemoguće iscrtati mnogokut sa samo {} točke "
                                                                 "(potrebno minimalno 3)!",
        Phrase.LAB2_FirstAssignment_CantDeleteNothing: "Ne postoji ništa za obrisati!",

        Phrase.LAB2_SecondAssignment_PointTouchingModel: "Točka {} dira model.",
        Phrase.LAB2_SecondAssignment_PointNotTouchingModel: "Točka {} je {} modela."
    }

PATH: Dict[Path, str] =\
    {
        Path.LAB2_ObjectPath: "objects",
    }

# endregion

# region Numbers


class Number(Enum):
    Universal_SinglePrecisionThreshold = auto(),
    Universal_DoublePrecisionThreshold = auto(),

    LAB1_FirstAssignment_Task7_EquationDimensionality = auto(),
    LAB1_FirstAssignment_Task7_EquationCount = auto(),

    LAB1_SecondAssignment_LineOffsetY = auto(),


NUMBER: Dict[Number, int or float] =\
    {
        Number.Universal_SinglePrecisionThreshold: 0.000001,
        Number.Universal_DoublePrecisionThreshold: 0.000000000001,

        Number.LAB1_FirstAssignment_Task7_EquationDimensionality: 3,
        Number.LAB1_FirstAssignment_Task7_EquationCount: 3,

        Number.LAB1_SecondAssignment_LineOffsetY: 10,
    }

# endregion

# region Classes

# region LAB2


class ConvexPoly:
    def __init__(self, coordinates: List[Tuple[int, int]]):
        self.vertices: List[Tuple[int, int]] = coordinates

        self.x_bounds, self.y_bounds = ((None, None), (None, None))
        self.coefficients: Dict[str, Dict[int, float]] = dict()

        self.edge_lines = list()
        self.fill_lines: List[Tuple[int, int, int, int]] = list()

        self._init()

    def _init(self):
        # region Find x and y bounds.

        x_entries, y_entries = (set(map(lambda x: x[0], self.vertices)), set(map(lambda x: x[1], self.vertices)))

        self.x_bounds = (min(x_entries), max(x_entries))
        self.y_bounds = (min(y_entries), max(y_entries))

        # endregion

        # region Calculate edge coefficients.
        for coefficient in ["a", "b", "c"]:
            self.coefficients[coefficient] = dict()

        vertex_count = len(self.vertices)

        for i in range(0, vertex_count):
            self.coefficients["a"][i] = self.vertices[i][1] - self.vertices[(i + 1) % vertex_count][1]
            self.coefficients["b"][i] = -self.vertices[i][0] + self.vertices[(i + 1) % vertex_count][0]
            self.coefficients["c"][i] = self.vertices[i][0] * self.vertices[(i + 1) % vertex_count][1] \
                                        - self.vertices[(i + 1) % vertex_count][0] * self.vertices[i][1]

        # endregion

        # region Calculate vertex pairs for polygon edges.

        self.edge_lines = [(*self.vertices[i], *self.vertices[(i + 1) % vertex_count]) for i in range(0, vertex_count)]

        # endregion

        # region Calculate points to fill poly.

        for y_0 in range(self.y_bounds[0], self.y_bounds[1] + 1):
            left_bound, right_bound = (self.x_bounds[0], self.x_bounds[1])

            for i in range(0, vertex_count):
                if self.coefficients["a"][i] is 0:
                    continue

                x_l = float(-self.coefficients["b"][i] * y_0 - self.coefficients["c"][i]) / self.coefficients["a"][i]

                if self.vertices[i][1] < self.vertices[(i + 1) % vertex_count][1]:
                    if x_l > left_bound:
                        left_bound = int(x_l)
                elif x_l < right_bound:
                    right_bound = int(x_l)

            if left_bound < right_bound:
                self.fill_lines.append((left_bound, y_0, right_bound, y_0))

        # endregion

    def get_relation(self, vertex: Tuple[int, int] or List[int]) -> "SpatialRelation":
        has_larger = False

        for i in range(0, len(self.coefficients["a"])):
            result = vertex[0] * self.coefficients["a"][i] \
                     + vertex[1] * self.coefficients["b"][i] \
                     + self.coefficients["c"][i]

            if result is 0:
                return SpatialRelation.Touching
            elif not has_larger and result > 0:
                has_larger = True

        if has_larger:
            return SpatialRelation.Outside

        return SpatialRelation.Inside


class Model:
    def __init__(self, obj_string: str):
        self.group: str = None
        self.vertices: List[Tuple[float, float, float]] = list()
        self.faces: List[Tuple[int, int, int]] = list()
        self._coordinate_bounds: Tuple[float, float, float, float] = None

        self.coefficients: Dict[str, List[float]] = dict()

        self.eye_point = [0, 0, 0]
        self.viewpoint = [0, 0, 0]

        self.t_matrix = [[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]

        self.p_matrix = [[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]

        self.light_source = [0, 0, 0]

        self.intensity_a, self.intensity_i = (255, 255)
        self.coefficient_a, self.coefficient_d = (0.5, 0.2)

        # region Parse string.

        for line in obj_string.splitlines():
            line = line.strip()

            if line.startswith("#"):
                continue
            elif line.startswith("g"):
                if self.group is None:
                    self.group = re.split(r"\s+", line)[1]
            elif line.startswith("v"):
                self.vertices.append(tuple(map(lambda x: float(x), re.split(r"\s+", line)[1:]))[0:3])
            elif line.startswith("f"):
                self.faces.append(tuple(map(lambda x: int(x), re.split(r"\s+", line)[1:]))[0:3])

        # endregion

        # region Determine object bounds.

        x_map = set(map(lambda x: x[0], self.vertices))
        y_map = set(map(lambda x: x[1], self.vertices))

        self._coordinate_bounds = (min(x_map), max(x_map), min(y_map), max(y_map))

        # endregion

        # region Calculate coefficients.

        for coefficient in ["A", "B", "C", "D"]:
            self.coefficients[coefficient] = list()

        for face in self.faces:
            vertices = (self.vertices[face[0] - 1], self.vertices[face[1] - 1], self.vertices[face[2] - 1])

            a = (vertices[1][1] - vertices[0][1]) * (vertices[2][2] - vertices[0][2])\
                - (vertices[1][2] - vertices[0][2]) * (vertices[2][1] - vertices[0][1])
            b = (vertices[1][2] - vertices[0][2]) * (vertices[2][0] - vertices[0][0])\
                - (vertices[1][0] - vertices[0][0]) * (vertices[2][2] - vertices[0][2])
            c = (vertices[1][0] - vertices[0][0]) * (vertices[2][1] - vertices[0][1])\
                - (vertices[1][1] - vertices[0][1]) * (vertices[2][0] - vertices[0][0])

            self.coefficients["A"].append(a)
            self.coefficients["B"].append(b)
            self.coefficients["C"].append(c)
            self.coefficients["D"].append(-vertices[0][0] * a - vertices[0][1] * b - vertices[0][2] * c)

        # endregion

    def normalize_in_space(self):
        max_x, max_y, max_z = self.vertices[0]
        min_x, min_y, min_z = self.vertices[0]

        for vertex in self.vertices:
            max_x, max_y, max_z = (max(vertex[0], max_x), max(vertex[1], max_y), max(vertex[2], max_z))
            min_x, min_y, min_z = (min(vertex[0], min_x), min(vertex[1], min_y), min(vertex[2], min_z))

        center = (float(min_x + max_x)/2., float(min_y + max_y)/2., float(min_z + max_z) /2.)
        biggest_offset = float(max(max_x - min_x, max_y - min_y, max_z - min_z))

        new_vertices = list()

        for vertex in self.vertices:
            new_vertices.append(((vertex[0] - center[0]) * 2 / biggest_offset,
                                 (vertex[1] - center[1]) * 2 / biggest_offset,
                                 (vertex[2] - center[2]) * 2 / biggest_offset))

        self.vertices = new_vertices

    def get_minimized_vertex_list(self):
        vertex_list = list()
        new_vertices = list()

        for vertex in self.vertices:
            new_vertex = np.matmul(np.matmul([*vertex, 1], self.t_matrix), self.p_matrix)
            new_vertex = tuple(np.multiply(new_vertex, 1 / new_vertex[3]))
            new_vertices.append(new_vertex)

        for face in self.faces:
            verts = (new_vertices[face[0] - 1], new_vertices[face[1] - 1], new_vertices[face[2] - 1])

            a = (verts[1][1] - verts[0][1]) * (verts[2][2] - verts[0][2]) - (verts[1][2] - verts[0][2]) *\
                (verts[2][1] - verts[0][1])
            b = (verts[1][2] - verts[0][1]) * (verts[2][0] - verts[0][0]) - (verts[1][0] - verts[0][0]) *\
                (verts[2][2] - verts[0][2])
            c = (verts[1][0] - verts[0][0]) * (verts[2][1] - verts[0][1]) - (verts[1][1] - verts[0][1]) *\
                (verts[2][0] - verts[0][0])

            xc = (verts[0][0] + verts[1][0] + verts[2][0]) / 3
            yc = (verts[0][1] + verts[1][1] + verts[2][1]) / 3
            zc = (verts[0][2] + verts[1][2] + verts[2][2]) / 3

            d = (self.eye_point[0] - xc, self.eye_point[1] - yc, self.eye_point[2] - zc)

            cos_a = (a * d[0] + b * d[1] + c * d[2]) /\
                    ((a ** 2 + b ** 2 + c ** 2) ** 0.5 * (d[0] ** 2 + d[1] ** 2 + d[2] ** 2) ** 0.5)

            if degrees(acos(cos_a)) < 90:
                vertex_list.append(verts)

        return vertex_list

    def get_minimized_face_list(self):
        face_list = list()
        new_vertices = list()

        for vertex in self.vertices:
            new_vertex = np.matmul(np.matmul([*vertex, 1], self.t_matrix), self.p_matrix)
            new_vertex = tuple(np.multiply(new_vertex, 1 / new_vertex[3]))
            new_vertices.append(new_vertex)

        for face in self.faces:
            verts = (new_vertices[face[0] - 1], new_vertices[face[1] - 1], new_vertices[face[2] - 1])

            a = (verts[1][1] - verts[0][1]) * (verts[2][2] - verts[0][2]) - (verts[1][2] - verts[0][2]) *\
                (verts[2][1] - verts[0][1])
            b = (verts[1][2] - verts[0][1]) * (verts[2][0] - verts[0][0]) - (verts[1][0] - verts[0][0]) *\
                (verts[2][2] - verts[0][2])
            c = (verts[1][0] - verts[0][0]) * (verts[2][1] - verts[0][1]) - (verts[1][1] - verts[0][1]) *\
                (verts[2][0] - verts[0][0])

            xc = (verts[0][0] + verts[1][0] + verts[2][0]) / 3
            yc = (verts[0][1] + verts[1][1] + verts[2][1]) / 3
            zc = (verts[0][2] + verts[1][2] + verts[2][2]) / 3

            d = (self.eye_point[0] - xc, self.eye_point[1] - yc, self.eye_point[2] - zc)

            cos_a = (a * d[0] + b * d[1] + c * d[2]) /\
                    ((a ** 2 + b ** 2 + c ** 2) ** 0.5 * (d[0] ** 2 + d[1] ** 2 + d[2] ** 2) ** 0.5)

            if degrees(acos(cos_a)) < 90:
                face_list.append(face)

        return face_list

    def get_constant_shaded_lists(self):
        triangles = list()
        colors = list()

        for face in self.get_minimized_vertex_list():
            vertex_c = ((face[0][0] + face[1][0] + face[2][0]) / 3,
                        (face[0][1] + face[1][1] + face[2][1]) / 3,
                        (face[0][2] + face[1][2] + face[2][2]) / 3)

            n = ((face[1][1] - face[0][1]) * (face[2][2] - face[0][2]) - (face[1][2] - face[0][2]) *
                 (face[2][1] - face[0][1]),
                 (face[1][2] - face[0][1]) * (face[2][0] - face[0][0]) - (face[1][0] - face[0][0]) *
                 (face[2][2] - face[0][2]),
                 (face[1][0] - face[0][0]) * (face[2][1] - face[0][1]) - (face[1][1] - face[0][1]) *
                 (face[2][0] - face[0][0]))

            n_length = (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5
            n = (n[0] / n_length, n[1] / n_length, n[2] / n_length)

            l = (self.light_source[0] - vertex_c[0],
                 self.light_source[1] - vertex_c[1],
                 self.light_source[2] - vertex_c[2])

            l_length = (l[0] ** 2 + l[1] ** 2 + l[2] ** 2) ** 0.5
            l = (l[0] / l_length, l[1] / l_length, l[2] / l_length)

            ln = l[0] * n[0] + l[1] * n[1] + l[2] * n[2]

            intensity = max(0, self.intensity_i * self.coefficient_d * ln)
            intensity += self.intensity_a * self.coefficient_a
            intensity = min(255, int(intensity))

            triangles.append((face[0][0], face[0][1], face[1][0], face[1][1], face[2][0], face[2][1]))
            colors.append((0, intensity, 0, 0, intensity, 0, 0, intensity, 0))

        return triangles, colors

    def get_variable_shaded_lists(self):
        vertex_to_faces = dict()
        vertex_normal = dict()
        triangles = list()
        colors = list()

        new_vertices = list()

        for vertex in self.vertices:
            new_vertex = np.matmul(np.matmul([*vertex, 1], self.t_matrix), self.p_matrix)
            new_vertex = tuple(np.multiply(new_vertex, 1 / new_vertex[3]))
            new_vertices.append(new_vertex)

        for face in self.faces:
            for vertex_index in face:
                vertex_index -= 1
                if vertex_index not in vertex_to_faces:
                    vertex_to_faces[vertex_index] = list()

                vertex_to_faces[vertex_index].append(face)

        for i in range(0, len(self.vertices)):
            n = (0, 0, 0)

            for face in vertex_to_faces[i]:
                current_vertex = (new_vertices[face[0] - 1], new_vertices[face[1] - 1], new_vertices[face[2] - 1])

                a = (current_vertex[1][1] - current_vertex[0][1]) *\
                    (current_vertex[2][2] - current_vertex[0][2]) - (current_vertex[1][2] - current_vertex[0][2]) *\
                    (current_vertex[2][1] - current_vertex[0][1])
                b = (current_vertex[1][2] - current_vertex[0][1]) *\
                    (current_vertex[2][0] - current_vertex[0][0]) - (current_vertex[1][0] - current_vertex[0][0]) *\
                    (current_vertex[2][2] - current_vertex[0][2])
                c = (current_vertex[1][0] - current_vertex[0][0]) *\
                    (current_vertex[2][1] - current_vertex[0][1]) - (current_vertex[1][1] - current_vertex[0][1]) *\
                    (current_vertex[2][0] - current_vertex[0][0])
                d = (a ** 2 + b ** 2 + c ** 2) ** 0.5

                if d:
                    n = (n[0] + a/d, n[1] + b/d, n[2] + c/d)

            n_length = (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5

            if n_length:
                vertex_normal[i] = (n[0] / n_length, n[1] / n_length, n[2] / n_length)
            else:
                vertex_normal[i] = n

        for face in self.get_minimized_face_list():
            intensity = [0, 0, 0]

            for i, vertex_index in enumerate(face):
                vertex_index -= 1
                l = (self.light_source[0] - self.vertices[vertex_index][0],
                     self.light_source[1] - self.vertices[vertex_index][1],
                     self.light_source[2] - self.vertices[vertex_index][2])

                l_length = (l[0] ** 2 + l[1] ** 2 + l[2] ** 2) ** 0.5

                if l_length:
                    l = (l[0] / l_length, l[1] / l_length, l[2] / l_length)

                n = vertex_normal[vertex_index]
                ln = l[0] * n[0] + l[1] * n[1] + l[2] * n[2]

                intensity[i] = max(0, self.intensity_i * self.coefficient_d * ln)
                intensity[i] += self.intensity_a * self.coefficient_a
                intensity[i] = min(255, int(intensity[i]))

            triangles.append((new_vertices[face[0] - 1][0], new_vertices[face[0] - 1][1],
                              new_vertices[face[1] - 1][0], new_vertices[face[1] - 1][1],
                              new_vertices[face[2] - 1][0], new_vertices[face[2] - 1][1]))
            colors.append((0, intensity[0], 0, 0, intensity[1], 0, 0, intensity[2], 0))

        return triangles, colors

    def calculate_perspective_matrices(self):
        t_1 = [[1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [-self.eye_point[0], -self.eye_point[1], -self.eye_point[2], 1]]

        g_1 = np.matmul([*self.viewpoint, 1], t_1)

        alpha_denominator = (g_1[0] ** 2 + g_1[1] ** 2) ** 0.5

        alpha = (g_1[1] / alpha_denominator,
                 g_1[0] / alpha_denominator)

        t_2 = [[alpha[1], -alpha[0], 0, 0],
               [alpha[0], alpha[1], 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]

        g_2 = np.matmul(g_1, t_2)

        beta_denominator = (g_2[0] ** 2 + g_2[2] ** 2) ** 0.5

        beta = (g_2[0] / beta_denominator,
                g_2[2] / beta_denominator)

        t_3 = [[beta[1], 0, beta[0], 0],
               [0, 1, 0, 0],
               [-beta[0], 0, beta[1], 0],
               [0, 0, 0, 1]]

        t_4 = [[0, -1, 0, 0],
               [1, 0, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]

        t_5 = [[-1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [0, 0, 0, 1]]

        self.t_matrix = np.matmul(t_1, t_2)
        self.t_matrix = np.matmul(self.t_matrix, t_3)
        self.t_matrix = np.matmul(self.t_matrix, t_4)
        self.t_matrix = np.matmul(self.t_matrix, t_5)

        h = ((self.eye_point[0] - self.viewpoint[0]) ** 2 +
             (self.eye_point[1] - self.viewpoint[1]) ** 2 +
             (self.eye_point[2] - self.viewpoint[2]) ** 2) ** 0.5

        self.p_matrix = [[1, 0, 0, 0],
                         [0, 1, 0, 0],
                         [0, 0, 0, 1 / h],
                         [0, 0, 0, 0]]

    def set_eye_and_view(self, eye_point: Tuple[float, float, float], viewpoint: Tuple[float, float, float]):
        self.eye_point = eye_point
        self.viewpoint = viewpoint

        self.calculate_perspective_matrices()

    def get_translation_and_scaling(self, resolution: Tuple[int, int])\
            -> Tuple[Tuple[float, float], float, Tuple[float, float]]:
        middle_values = ((self._coordinate_bounds[0] + self._coordinate_bounds[1]),
                         (self._coordinate_bounds[2] + self._coordinate_bounds[3]))

        translation = (float(-middle_values[0])/2, float(-middle_values[1])/2)

        value_ranges = (self._coordinate_bounds[1] - self._coordinate_bounds[0],
                        self._coordinate_bounds[3] - self._coordinate_bounds[2])

        scaling = min(float(resolution[0])/(value_ranges[0]),
                      float(resolution[1])/(value_ranges[1])) * 0.95

        second_translation = (float(resolution[0]) / 2, float(resolution[1]) / 2)

        return translation, scaling, second_translation

    def get_draw_list(self, translation: Tuple[int, int], scaling: float, second_translation: Tuple[int, int])\
            -> List[Tuple[float, float, float, float, float, float]]:
        draw_list: List[Tuple[float, float, float, float, float, float]] = list()

        for face in self.faces:
            vertices = (self.vertices[face[0] - 1], self.vertices[face[1] - 1], self.vertices[face[2] - 1])

            draw_list.append(((vertices[0][0] + translation[0]) * scaling + second_translation[0],
                              (vertices[0][1] + translation[1]) * scaling + second_translation[1],
                              (vertices[1][0] + translation[0]) * scaling + second_translation[0],
                              (vertices[1][1] + translation[1]) * scaling + second_translation[1],
                              (vertices[2][0] + translation[0]) * scaling + second_translation[0],
                              (vertices[2][1] + translation[1]) * scaling + second_translation[1]))

        return draw_list

    def get_viewpoint_draw_list(self)\
            -> List[Tuple[float, float, float, float, float, float]]:
        viewpoint_draw_list = list()
        new_vertices = list()

        for vertex in self.vertices:
            new_vertex = np.matmul(np.matmul([*vertex, 1], self.t_matrix), self.p_matrix)
            new_vertex = tuple(np.multiply(new_vertex, 1/new_vertex[3]))
            new_vertices.append(new_vertex)

        for face in self.faces:
            vertices = (new_vertices[face[0] - 1], new_vertices[face[1] - 1], new_vertices[face[2] - 1])

            viewpoint_draw_list.append((vertices[0][0], vertices[0][1],
                                        vertices[1][0], vertices[1][1],
                                        vertices[2][0], vertices[2][1]))

        return viewpoint_draw_list

    def get_relation(self, vertex: Tuple[float, float, float]) -> "SpatialRelation":
        for i in range(0, len(self.coefficients["A"])):
            result = self.coefficients["A"][i] * vertex[0] + self.coefficients["B"][i] * vertex[1]\
                    + self.coefficients["C"][i] * vertex[2] + self.coefficients["D"][i]

            if result > 0:
                return SpatialRelation.Outside

        return SpatialRelation.Inside

    def __str__(self):
        return "Group: {}\nVertices: {}\nFaces: {}".format(self.group, self.vertices, self.faces)

# endregion

# endregion

# region Enumerators


class SpatialRelation(Enum):
    Touching = auto(),
    Inside = auto(),
    Outside = auto(),

    def __str__(self):
        return self.name.lower()

    def str_croatian(self):
        if self is SpatialRelation.Touching:
            return "dira"
        elif self is SpatialRelation.Inside:
            return "unutar"
        elif self is SpatialRelation.Outside:
            return "izvan"

# endregion

# region Mappings


class ColorTriple:
    Red = (255, 0, 0)
    Green = (0, 255, 0)
    Blue = (0, 0, 255)

    Yellow = (255, 255, 0)
    Magenta = (255, 0, 255)
    Cyan = (0, 255, 255)

    Black = (0, 0, 0)
    White = (255, 255, 255)

# endregion

# region Global Methods


def solve_equation_set(coefficients: List[int or float], equation_count: int):
    coefficient_matrix = list()
    result_matrix = list()
    entries_per_equation = int(len(coefficients) / equation_count)

    for i in range(0, equation_count):
        coefficient_matrix.append(list())

        for j in range(0, entries_per_equation - 1):
            coefficient_matrix[i].append(coefficients[i * entries_per_equation + j])

        result_matrix.append(coefficients[(i + 1) * entries_per_equation - 1])

    coefficient_matrix = np.linalg.inv(np.array(coefficient_matrix))
    result_matrix = np.transpose(np.array(result_matrix))

    return np.matmul(coefficient_matrix, result_matrix)


def get_resolution() -> Tuple[int, int]:
    user_input, width, height = None, None, None

    while user_input is None:
        user_input = input("{}: ".format(STRING[Phrase.Universal_EnterResolution]))

        if re.match(REGEX[RegularExpression.Universal_Resolution], user_input):
            results = re.split(DELIMITER[Delimiter.Resolution], user_input)[0::2]

            if len(results) is 2:
                try:
                    width, height = int(results[0]), int(results[1])
                except ValueError:
                    print("{}\n".format(STRING[Phrase.Universal_InvalidResolution]))
                    user_input = None
            else:
                print("{}\n".format(STRING[Phrase.Universal_InvalidResolution]))
                user_input = None
        else:
            print("{}\n".format(STRING[Phrase.Universal_InvalidResolution]))
            user_input = None

    return width, height


def get_object() -> str or None:
    user_input = None

    while user_input is None:
        path_to_look = os.path.join(os.curdir, PATH[Path.LAB2_ObjectPath])

        file_names = list(filter(lambda x: x.endswith(".obj"), os.listdir(path_to_look)))

        if len(file_names) is 0:
            print("{} ({})".format(STRING[Phrase.Universal_NoObjectFilesAtDefaultLocation],
                                   os.path.abspath(path_to_look)))
            return None
        else:
            for i, file_name in enumerate(file_names):
                print("{} - {}".format(i, file_name))

            print()

            user_input = None

            while user_input is None:
                user_input = input("{}: ".format(STRING[Phrase.Universal_EnterObjectNameOrNumber]))

                if re.match(r"\d+", user_input):
                    user_input = int(user_input)
                    if user_input < len(file_names):
                        return open(os.path.join(path_to_look, file_names[user_input])).read()
                    else:
                        print(STRING[Phrase.Universal_ObjectIndexOutOfRange].format(str(len(file_names) - 1),
                                                                                    str(user_input)))
                        print()
                        user_input = None
                elif user_input in file_names:
                    return open(os.path.join(path_to_look, user_input)).read()
                else:
                    print("{}\n".format(STRING[Phrase.Universal_InvalidObjectNameOrNumber]))
                    user_input = None


def get_vertex_3d() -> Tuple[float, float, float]:
    user_input, vertex = None, (None, None, None)

    while user_input is None:
        user_input = input("{}: ".format(STRING[Phrase.Universal_EnterVertex3D]))

        if re.match(REGEX[RegularExpression.Universal_Vertex3D], user_input):
            results = re.split(DELIMITER[Delimiter.Vertex3D], user_input)[0::2]

            if len(results) is 3:
                try:
                    vertex = (float(results[0]), float(results[1]), float(results[2]))
                except ValueError:
                    print("{}\n".format(STRING[Phrase.Universal_InvalidVertex3D]))
                    user_input = None
            else:
                print("{}\n".format(STRING[Phrase.Universal_InvalidVertex3D]))
                user_input = None
        else:
            print("{}\n".format(STRING[Phrase.Universal_InvalidVertex3D]))
            user_input = None

    return vertex


def get_eye_point() -> Tuple[float, float, float]:
    print("Očište:")
    return get_vertex_3d()


def get_viewpoint() -> Tuple[float, float, float]:
    print("Gledište:")
    return get_vertex_3d()


def get_bezier(vertices: List):
    points = list()

    l = len(vertices)
    c = list()

    for i in range(l):
        c.append(factorial(l - 1) / (factorial(i) * factorial(l - i - 1)))

    t = 0.0

    l -= 1

    while t <= 1.:
        i = 0
        p = [0, 0, 0]

        for vertex in vertices:
            r = [*vertex]
            b = c[i] * t ** i * (1 - t) ** (l - i)
            p = np.add(p, np.multiply(r, b))
            i += 1

        points.append((p[0], p[1]))

        t += 0.01

    return points


def get_light_source() -> Tuple[float, float, float]:
    print("Izvor svjetlosti:")
    return get_vertex_3d()


def get_fractal_mode():
    user_input = None

    while user_input is None:
        user_input = input("{}: ".format("Unesite mandelbrot ili julia"))

        if re.match(r"(?i)(mandelbrot|m)", user_input):
            return 0
        elif re.match(r"(?i)(julia|j)", user_input):
            return 1
        else:
            print("Pogrešan unos.")
            user_input = None


def get_mandelbrot(x_y_max: Tuple[int, int], u_range: Tuple[float, float], v_range: Tuple[float, float],
                   epsilon, iterations):
    points = list()
    colors = list()

    for x in range(0, x_y_max[0] + 1):
        for y in range(0, x_y_max[1] + 1):
            u, v = ((u_range[1] - u_range[0]) / x_y_max[0] * x + u_range[0],
                    (v_range[1] - v_range[0]) / x_y_max[1] * y + v_range[0])

            k, z, r = - 1, 0, 0
            c = complex(u, v)

            for k in range(0, iterations + 1):
                if r >= epsilon:
                    break

                z = z * z + c
                r = (z.real ** 2 + z.imag ** 2) ** 0.5

                points.append((x, y))

                if k is iterations:
                    colors.append((0, 0, 0))
                else:
                    colors.append((int(hash("ljac") * k) % 256,
                                   int(hash("i") * k) % 256,
                                   int(hash("aral") * k) % 256))

    return points, colors


def get_julia(x_y_max: Tuple[int, int], u_range: Tuple[float, float], v_range: Tuple[float, float],
              epsilon, iterations, c):
    points = list()
    colors = list()

    for x in range(0, x_y_max[0] + 1):
        for y in range(0, x_y_max[1] + 1):
            u, v = ((u_range[1] - u_range[0]) / x_y_max[0] * x + u_range[0],
                    (v_range[1] - v_range[0]) / x_y_max[1] * y + v_range[0])

            k, r = - 1, 0
            z = complex(u, v)

            for k in range(0, iterations + 1):
                if r >= epsilon:
                    break

                z = z * z + c
                r = (z.real ** 2 + z.imag ** 2) ** 0.5

                points.append((x, y))

                if k is iterations:
                    colors.append((0, 0, 0))
                else:
                    colors.append((int(hash("ljac") * k) % 256,
                                   int(hash("i") * k) % 256,
                                   int(hash("aral") * k) % 256))

    return points, colors

# endregion
