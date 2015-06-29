#!/usr/bin/python3

# TODO

def is_prime(num):
    if num == 1:
        return False
    i = 2
    while num >= i ** 2:
        if num % i == 0:
            return False
        i += 1
    return True


def main():
    while True:
        number = int(input('Input an integer: '))
        if is_prime(number):
            print('%d is a prime.' % number)
        else:
            print('%d is not a prime.' % number)

if __name__ == '__main__':
    main()
