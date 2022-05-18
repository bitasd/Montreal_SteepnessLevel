import math
"""
code to calculate accessibility decay based on detour from the shortest path
"""
def decay_func( L_lts4:float, Lijk: float) -> float:
    """
    :param L_lts4: shortest path in miles from the origin to the current point no restriction on LTS or Steepness Level
    :param Lijk: shortest path in miles with restriction on LTS and LS
    :return: decay/ propensity of accessibility
    """
    l1 = min(4, 1.2 * L_lts4)  # d1
    l2 = 1.33 * L_lts4   # d2
    l3 = 2 * L_lts4  # d34,3
    if Lijk <= l1:
        return 1

    elif Lijk <= l2:
        return math.exp(-0.231*(Lijk - l1))

    elif Lijk <= l3:
        return math.exp(-0.231*(Lijk - l1))*(l3 - Lijk)/(l3 - l2)
    else:
        return 0
