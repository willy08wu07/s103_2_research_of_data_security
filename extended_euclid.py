__author__ = 'willy'

# TODO

matrix = \
    [[1, 0, 0, 0, 1, 1, 1, 1],
     [1, 1, 0, 0, 0, 1, 1, 1],
     [1, 1, 1, 0, 0, 0, 1, 1],
     [1, 1, 1, 1, 0, 0, 0, 1],
     [1, 1, 1, 1, 1, 0, 0, 0]
     [0, 1, 1, 1, 1, 1, 0, 0],
     [0, 0, 1, 1, 1, 1, 1, 0],
     [0, 0, 0, 1, 1, 1, 1, 1]]


class Polynomial:
    def __init__(self, value=0b0):
        self.value = value

    def __add__(self, other):
        return Polynomial(self.value ^ other.value)

    def __sub__(self, other):
        return self + other

    def __repr__(self):
        return "Polynomial(0x{0:x})".format(self.value)

    def __mul__(self, other):
        ans = 0
        for i in range(0, self.max_bit() + 1):
            if ((self.value >> i) % 2) == 1:
                ans ^= other.value << i
        return Polynomial(ans)

    def __truediv__(self, other):
        ans = [Polynomial(0b0), Polynomial(0b0)]
        if self.max_bit() >= other.max_bit():
            ans[0] = Polynomial(2 ** (self.max_bit() - other.max_bit()))
            ans[1] = other * ans[0] + self
            ans_r = ans[1] / other
            ans[0] += ans_r[0]
            ans[1] = ans_r[1]
        else:
            ans[0] = Polynomial(0b0)
            ans[1] = self
        return ans

    def __floordiv__(self, other):
        return (self / other)[0]

    def __mod__(self, other):
        return (self / other)[1]

    def __eq__(self, other):
        if type(other) is int:
            return self.value == other
        elif type(other) is Polynomial:
            return self.value == other.value

    def max_bit(self):
        i = 0
        number = 1
        while True:
            if number >= self.value:
                return i
            number <<= 1
            number += 1
            i += 1


def byte_sub(number):
    total = 0
    for i in range(7, -1, -1):
        total <<= 1
        element = 0
        for j in range(0, 8):
            number1 = matrix[i][j]
            number2 = (number >> j) % 2
            element += number1 * number2
        total += element % 2
    return total


def extended_euclid(m, b):
    if type(m) is Polynomial:
        return extended_euclid_r([Polynomial(1), Polynomial(0), m],
                                 [Polynomial(0), Polynomial(1), b])
    else:
        return extended_euclid_r([1, 0, m], [0, 1, b])


def extended_euclid_r(a, b):
    if b[2] == 0:
        return None
    if b[2] == 1:
        return b[1]

    q = a[2] // b[2]
    t = [a[0] - q * b[0], a[1] - q * b[1], a[2] - q * b[2]]
    a = b
    b = t
    return extended_euclid_r(a, b)
while True:
    if input('Type: ') == '0':
        input_m = int(input('input m: '))
        input_b = int(input('input b: '))
        print(extended_euclid(input_m, input_b))
    else:
        input_m = Polynomial(int(input('input m: '), 16))
        input_b = Polynomial(int(input('input b: '), 16))
        output = extended_euclid(input_m, input_b)
        print(output)
        print('byte sub: 0x{0:x}'.format(byte_sub(output.value) ^ 0x63))
