#!/usr/bin/python3

# TODO

def get_bit(number, position):
    ans = (number % (2 << position)) >> position
    return ans


def main():
    print(get_bit(5, 0))
    print(get_bit(5, 1))

if __name__ == '__main__':
    w_value = [2] * 80

    print(w_value[80])
