__author__ = 'willy=='

# TODO

a = 12
p = 23


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

x1 = int(input('x1: '))
y1 = int(input('y1: '))
x2 = int(input('x2: '))
y2 = int(input('y2: '))
input_p1 = Point(x1, y1)
input_p2 = Point(x2, y2)


def get_lambda(point1, point2, a):
    if point1 == point2:
        num1 = 3 * (point1.x ** 2) + a
        num2 = 2 * point1.y
    else:
        num1 = point2.y - point1.y
        num2 = point2.x - point1.x

    lambda_value = 0
    if (num1 % num2) == 0:
        lambda_value = (num1 // num2) % p
    else:
        k = 0
        while True:
            if (num1 + num2 * k) % p == 0:
                lambda_value = (-k) % p
                break
            k += 1

    return lambda_value

getLambda = get_lambda(input_p1, input_p2, a)
print(getLambda)

x3 = ((getLambda ** 2) - input_p1.x - input_p2.x) % p
y3 = (getLambda * (input_p1.x - x3) - input_p1.y) % p
print(x3, y3)
