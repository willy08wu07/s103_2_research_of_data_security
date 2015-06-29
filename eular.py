#!/usr/bin/python3

# TODO

def factorization(num):
    import prime
    i = 3
    while num >= i ** 2:
        if num % i == 0:
            num1 = i - 1
            num2 = (num // i) - 1
            if prime.is_prime(num1) and prime.is_prime(num2):
                print(num1)
                print(num2)
                return
        i += 1
    print('None')


def main():
    while True:
        input_num = int(input('Input a positive integer: '))
        factorization(input_num)

if __name__ == '__main__':
    main()
