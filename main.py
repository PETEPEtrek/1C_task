import cv2
import queue
import geom
import math


class Pixels:
    """
    A class for working with pixels
    """

    def __init__(self, red, blue, green):
        self.red_ = red
        self.blue_ = blue
        self.green_ = green
        self.epsilon = 10

    def is_in_range(self, other):
        return abs(other.red_ - self.red_) + abs(other.green_ - self.green_) + abs(
            other.blue_ - self.blue_) <= self.epsilon


class Image:
    """
    A class for working with png image
    """

    def __init__(self, path: str):
        self.image_ = cv2.imread(path)

    def GetHeight(self):
        return self.image_.shape[0]

    def GetWidth(self):
        return self.image_.shape[1]

    def Colors(self, x: int, y: int):
        return self.image_[x, y]

    def initialize(self, pixels):
        for i in range(0, height):
            new = []
            for j in range(0, width):
                new.append(Pixels(0, 0, 0))
            pixels.append(new)

        for i in range(0, height):
            for j in range(0, width):
                colors_for_point = image.Colors(i, j)
                blue = colors_for_point[0]
                green = colors_for_point[1]
                red = colors_for_point[2]
                pixels[i][j] = Pixels(red, blue, green)


def is_path(x: int, y: int, pixels,
            is_used, height: int,
            width: int):
    """

    :param x: first coordinate
    :param y: second coordinate
    :param pixels: an array of pixels
    :param is_used: an array of used points
    :param height: number of pixels of picture height
    :param width: number of pixels of picture width
    :return: bool which means does we get a black unused point on the picture
    """
    if y < 0 or x < 0 or y > width or x > height:
        return False

    return pixels[x][y].is_in_range(Pixels(0, 0, 0)) and not is_used[x][y]


def is_thin_enough(first_point, second_point):
    """
    Checking distance between the points
    """
    pixels_thin = 30
    return abs(first_point.x - second_point.x) + abs(first_point.y - second_point.y) > pixels_thin


def BFS(height: int, width: int,
        pixels,
        verteses):
    """

    :param height: number of pixels of picture height
    :param width: number of pixels of picture width
    :param pixels: an array of pixels
    :param verteses: array of  points which belongs to the graph
    :return: verteses
    """
    is_used = []
    for i in range(0, height):
        new = []
        for j in range(0, width):
            new.append(False)
        is_used.append(new)
    for x in range(0, height):
        for y in range(0, width):
            if not is_path(x, y, pixels, is_used, height, width):
                continue
            good_point = geom.Point(x, y)
            verteses.append(good_point)

            next_point = geom.Point(-1, -1)
            que = queue.LifoQueue()
            que.put(good_point)
            is_used[good_point.x][good_point.y] = True

            while not que.empty():
                size = que.qsize()

                next_point = que.queue[0]

                for k in range(0, size):
                    point = que.get()

                    if not is_thin_enough(next_point, point):

                        if is_path(point.x + 1, point.y, pixels, is_used, height, width):
                            que.put(geom.Point(point.x + 1, point.y))
                            is_used[point.x + 1][point.y] = True

                        if is_path(point.x - 1, point.y, pixels, is_used, height, width):
                            que.put(geom.Point(point.x - 1, point.y))
                            is_used[point.x - 1][point.y] = True

                        if is_path(point.x, point.y + 1, pixels, is_used, height, width):
                            que.put(geom.Point(point.x, point.y + 1))
                            is_used[point.x][point.y + 1] = True

                        if is_path(point.x, point.y - 1, pixels, is_used, height, width):
                            que.put(geom.Point(point.x, point.y - 1))
                            is_used[point.x][point.y - 1] = True

            verteses.append(next_point)


def RemovingLinearRelation(num_of_verteses, verteses, not_a_line):
    """
    :param num_of_verteses: number of available points
    :param verteses: array of  points which belongs to the graph
    :param not_a_line: bool which means does three points are looking like straight line
    :return: not_a_line
    """
    for i in range(0, num_of_verteses):
        for j in range(0, num_of_verteses):
            for k in range(i + 1, num_of_verteses):

                if i == j or j == k:
                    continue

                first_point = verteses[i]
                second_point = verteses[j]
                third_point = verteses[k]

                first_side = ((first_point.x - second_point.x) ** 2.0 + (first_point.y - second_point.y) ** 2.0) ** 0.5
                second_side = ((third_point.x - second_point.x) ** 2.0 + (third_point.y - second_point.y) ** 2.0) ** 0.5
                third_side = ((first_point.x - third_point.x) ** 2.0 + (first_point.y - third_point.y) ** 2.0) ** 0.5

                if abs(first_side + second_side - third_side) < 0.001 * third_side:
                    not_a_line[j] = False


def FindAllIntersections(final_verteses):
    """
    finds all intersection between edges
    """
    answer = 0
    final_size = len(final_verteses)

    for first in range(0, final_size):
        for second in range(first + 1, final_size):
            for third in range(first + 1, final_size):
                for fourth in range(third + 1, final_size):
                    if first == third or first == fourth or second == third or second == fourth:
                        continue

                    if geom.intersection(final_verteses[first], final_verteses[second],
                                         final_verteses[third], final_verteses[fourth]):
                        answer = answer + 1
    return answer


if __name__ == '__main__':
    image = Image('example.png.png')
    height = image.GetHeight()
    width = image.GetWidth()
    pixels = []
    image.initialize(pixels)

    verteses = []
    BFS(height, width, pixels, verteses)

    fit_points = []
    num_of_verteses = len(verteses)
    for i in range(0, num_of_verteses):
        fit_points.append(True)

    RemovingLinearRelation(num_of_verteses, verteses, fit_points)

    final_verteses = []
    for i in range(0, num_of_verteses):
        if not fit_points[i]:
            continue
        final_verteses.append(verteses[i])

    answer = FindAllIntersections(final_verteses)

    print("Number of intersections is: ", math.ceil(answer / 2))
