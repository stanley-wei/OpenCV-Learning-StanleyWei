import math

def quadratic_formula(a, b, c):
    root_expression = math.sqrt((b**2) - (4 * a * c))
    numerator_plus = -b + root_expression
    numerator_minus = -b - root_expression
    denominator = 2 * a

    answer_plus = numerator_plus / denominator
    answer_minus = numerator_minus / denominator

    return answer_plus, answer_minus
