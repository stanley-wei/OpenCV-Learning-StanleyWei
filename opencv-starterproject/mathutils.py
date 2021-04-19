import math

def quadratic_formula(a, b, c):
    root_expression = math.sqrt((b**2) - (4 * a * c))
    numerator_plus = -b + root_expression
    numerator_minus = -b - root_expression
    denominator = 2 * a

    answer_plus = numerator_plus / denominator
    answer_minus = numerator_minus / denominator

    return answer_plus, answer_minus

def center_in_circle(center1, center2, radius1):
    if center1[0] + radius1 > center2[0] and center1[0] - radius1 < center2[0] and center1[1] + radius1 > center2[1] and center1[1] - radius1 < center2[1]:
        return True
    else:
        return False
