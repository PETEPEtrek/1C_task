class Point:
    """
    class for 2D points
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y


def Area(first_point, second_point, third_point):
    """
    :return: the area of three points
    """
    return (second_point.x - first_point.x) * (third_point.y - first_point.y) * \
           (second_point.y - first_point.y) * (third_point.x - first_point.x)


def is_projection_intersect(first, second, third, fourth):
    first_swp_x = first.x
    second_swp_x = second.x
    third_swp_x = third.x
    fourth_swp_x = fourth.x

    first_swp_y = first.y
    second_swp_y = second.y
    third_swp_y = third.y
    fourth_swp_y = fourth.y

    if first.x > second.x:
        first_swp_x, second_swp_x = second_swp_x, first_swp_x
    if third.x > fourth.x:
        third_swp_x, fourth_swp_x = fourth_swp_x, third_swp_x

    if first.y > second.y:
        first_swp_y, second_swp_y = second_swp_y, first_swp_y
    if third.y > fourth.y:
        third_swp_y, fourth_swp_y = fourth_swp_y, third_swp_y
    return min(second_swp_x, fourth_swp_x) >= max(first_swp_x, third_swp_x) and \
           min(second_swp_y, fourth_swp_y) >= max(first_swp_y, third_swp_y)


def intersection(first_point, second_point, third_point, fourth_point):
    return is_projection_intersect(first_point, second_point, third_point, fourth_point) and Area(
        first_point, second_point, fourth_point) * Area(
        first_point, second_point, third_point) <= 0 and Area(
        third_point, fourth_point, first_point) * Area(
        third_point, fourth_point, second_point) <= 0
