import numpy as np

from enum import Enum, auto
from typing import Dict, List

# region Delimiters


class Delimiter(Enum):
    Resolution = auto(),


DELIMITER: Dict[Delimiter, str] =\
    {
        Delimiter.Resolution: r"\s*(x|,)\s*"
    }

# endregion

# region Regular Expressions


class RegularExpression(Enum):
    Universal_ExitLoop = auto()
    LAB1_FirstAssignmentCommand = auto()
    LAB1_SecondAssignmentCommand = auto(),

    LAB1_FirstAssignment_Task7_Delimiter = auto(),
    LAB1_FirstAssignment_Task8_Delimiter = auto(),

    LAB1_SecondAssignment_Resolution = auto(),


REGEX: Dict[RegularExpression, str] =\
    {
        RegularExpression.Universal_ExitLoop: r"((?i)(izađi|izlaz|kraj|ugasi|exit|end|shutdown))",

        RegularExpression.LAB1_FirstAssignmentCommand: r"((?i)(1|jedan|prva|one|first))",
        RegularExpression.LAB1_SecondAssignmentCommand: r"((?i)(2|dva|druga|two|second))",

        RegularExpression.LAB1_FirstAssignment_Task7_Delimiter: r",",
        RegularExpression.LAB1_FirstAssignment_Task8_Delimiter: r",",

        RegularExpression.LAB1_SecondAssignment_Resolution: r"\d+" + DELIMITER[Delimiter.Resolution] + r"\d+"
    }

# endregion

# region Strings


class Phrase(Enum):
    Universal_VectorOutput = auto(),
    Universal_VectorOutputShort = auto(),
    Universal_ZeroDimensionalVector = auto(),

    LAB1_EnterTaskNumber = auto(),
    LAB1_InvalidTaskNumber = auto(),

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

    LAB1_SecondAssignment_EnterResolution = auto(),
    LAB1_SecondAssignment_InvalidResolution = auto(),


STRING: Dict[Phrase, str] =\
    {
        Phrase.Universal_VectorOutput: "({}) = ({})",
        Phrase.Universal_VectorOutputShort: "({})",
        Phrase.Universal_ZeroDimensionalVector: "Vektor dimenzije 0",

        Phrase.LAB1_EnterTaskNumber: "Unesite broj vježbe koju želite pokrenuti",
        Phrase.LAB1_InvalidTaskNumber: "Pogrešan unos. Pokušajte unos oblika \"1\" ili \"2\". "
                                       "Za izlaz upišite \"izlaz\".",
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

        Phrase.LAB1_SecondAssignment_EnterResolution: "Unesite rezoluciju odvojenu s \"x\" ili \",\"",
        Phrase.LAB1_SecondAssignment_InvalidResolution: "Neispravan unos rezolucije. Unesite 2 cijela broja odvojena "
                                                        "s \"x\" ili \",\"."
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

# endregion
