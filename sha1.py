#!/usr/bin/python3

# TODO

import time


def read_padded_file_block(filename):
    file_len = 0
    length_per_read = 64
    with open(filename, "rb") as file:
        block = file.read(length_per_read)
        while block:
            block_len = block.__len__()
            file_len += block_len
            if block_len >= length_per_read:
                yield block
                block = file.read(length_per_read)
            else:
                break

    length = file_len
    length_in_bits = length * 8
    length_with_padded1_and_size = length + 1 + 8
    needed_padding_byte = (64 - length_with_padded1_and_size) % 64
    extra_padded_data = bytearray(block)

    extra_padded_data.append(0b10000000)
    for i in range(needed_padding_byte):
        extra_padded_data.append(0x0)

    for i in range(56, -1, -8):
        extra_padded_data.append((length_in_bits >> i) % 0x100)

    for i in range(0, extra_padded_data.__len__(), 64):
        yield bytes(extra_padded_data[i:i + 64])


def f_stage1(b, c, d):
    ans = (b & c) | (~b & d)
    return ans % 0x100000000


def f_stage2(b, c, d):
    ans = b ^ c ^ d
    return ans


def f_stage3(b, c, d):
    ans = (b & c) | (b & d) | (c & d)
    return ans


def f_stage4(b, c, d):
    return f_stage2(b, c, d)


def f(t, b, c, d):
    if t >= 60:
        return f_stage4(b, c, d)
    elif t >= 40:
        return f_stage3(b, c, d)
    elif t >= 20:
        return f_stage2(b, c, d)
    else:
        return f_stage1(b, c, d)


def k(t):
    if t >= 60:
        return 0xca62c1d6
    elif t >= 40:
        return 0x8f1bbcdc
    elif t >= 20:
        return 0x6ed9eba1
    else:
        return 0x5a827999


def sha(data, hash_value=None):
    def w(position):
        ans = w_value[position]

        if ans is None:
            if position < 16:
                data_position = position * 4
                ans = (data[data_position + 0] << 24) + \
                      (data[data_position + 1] << 16) + \
                      (data[data_position + 2] << 8) + \
                      (data[data_position + 3] << 0)
            else:
                ans = w(position - 16) ^ \
                    w(position - 14) ^ \
                    w(position - 8) ^ \
                    w(position - 3)
                ans = (ans << 1) % 0x100000000 + (ans >> 31)

        w_value[position] = ans
        return ans

    if hash_value is None:
        # Initial constants
        hash_value = [0x67452301,
                      0xefcdab89,
                      0x98badcfe,
                      0x10325476,
                      0xc3d2e1f0]

    w_value = [None] * 80

    a = hash_value[0]
    b = hash_value[1]
    c = hash_value[2]
    d = hash_value[3]
    e = hash_value[4]

    for i in range(80):
        a_shift = (a << 5) % 0x100000000 + (a >> 27)
        w_t = w(i)
        k_t = k(i)
        new_a = (f(i, b, c, d) + e + a_shift + w_t + k_t) % 0x100000000
        new_b = a
        new_c = (b << 30) % 0x100000000 + (b >> 2)
        new_d = c
        new_e = d
        a = new_a
        b = new_b
        c = new_c
        d = new_d
        e = new_e

        # print('t = %d :' % i, end=' ')
        # print('{0:08x}'.format(a), end=' ')
        # print('{0:08x}'.format(b), end=' ')
        # print('{0:08x}'.format(c), end=' ')
        # print('{0:08x}'.format(d), end=' ')
        # print('{0:08x}'.format(e), end='\n')

    hash_value[0] += a
    hash_value[1] += b
    hash_value[2] += c
    hash_value[3] += d
    hash_value[4] += e

    for i in range(5):
        hash_value[i] %= 0x100000000

    # print('{0:08x}'.format(a), end=' ')
    # print('{0:08x}'.format(b), end=' ')
    # print('{0:08x}'.format(c), end=' ')
    # print('{0:08x}'.format(d), end=' ')
    # print('{0:08x}'.format(e), end='\n')

    return hash_value


def main():
    hash_value = None
    progress = 0
    start = time.time()
    for block in read_padded_file_block('filename_here'):
        hash_value = sha(block, hash_value)
        progress += 64
        if progress % 65536 == 0:
            print("{:,} bytes".format(progress))
    end = time.time()
    print(end - start)

    for i in hash_value:
        print('{0:08x}'.format(i), end='')
    print()

if __name__ == '__main__':
    main()
