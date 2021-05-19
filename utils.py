import math


def get_coords(i, delta, dist=20):
    x = dist * math.cos(i * delta)
    y = dist * math.sin(i * delta)
    return x, y
