import math
"""
code to calculate accessibility decay based on detour from the shortest path
"""
def decay_func( L_lts4:float, Lijk: float) -> float:
    """
    :param L_lts4: shortest path in meters from the origin to the current point no restriction on LTS or Steepness Level
    :param Lijk: shortest path in meters with restriction on LTS and LS
    :return: decay/ propensity of accessibility
    """
    L_lts4, Lijk = L_lts4/1609.34, Lijk/1609.34  # transform to miles
    l1 = min(4, 1.2 * L_lts4)  # d1
    l2 = 1.33 * L_lts4   # d2
    l3 = 2 * L_lts4  # d34,3
    if Lijk <= l1:
        return 1

    elif Lijk <= l2:
        return math.exp(-0.231*(Lijk - l1))

    elif Lijk <= l3:
        return math.exp(-0.231*(Lijk - l1))*(l3 - Lijk)/(l3 - l2)
    elif Lijk > l3:
        return 0
    else:
        return 0
