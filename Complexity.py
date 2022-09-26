from copy import copy as copy
from numpy import dot as dot
from numpy import histogram as histogram
from numpy import zeros as zeros
from scipy.special import gammaincc as gammaincc

class ComplexityTest:

    @staticmethod
    def linear_complexity_test(binary_data:str, verbose=False, block_size=500):


        length_of_binary_data = len(binary_data)

        degree_of_freedom = 6
        pi = [0.01047, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833]

        t2 = (block_size / 3.0 + 2.0 / 9) / 2 ** block_size
        mean = 0.5 * block_size + (1.0 / 36) * (9 + (-1) ** (block_size + 1)) - t2

        number_of_block = int(length_of_binary_data / block_size)

        if number_of_block > 1:
            block_end = block_size
            block_start = 0
            blocks = []
            for i in range(number_of_block):
                blocks.append(binary_data[block_start:block_end])
                block_start += block_size
                block_end += block_size

            complexities = []
            for block in blocks:
                complexities.append(ComplexityTest.berlekamp_massey_algorithm(block))

            t = ([-1.0 * (((-1) ** block_size) * (chunk - mean) + 2.0 / 9) for chunk in complexities])
            vg = histogram(t, bins=[-9999999999, -2.5, -1.5, -0.5, 0.5, 1.5, 2.5, 9999999999])[0][::-1]
            im = ([((vg[ii] - number_of_block * pi[ii]) ** 2) / (number_of_block * pi[ii]) for ii in range(7)])

            xObs = 0.0
            for i in range(len(pi)):
                xObs += im[i]

            p_value = gammaincc(degree_of_freedom / 2.0, xObs / 2.0)

            if verbose:
                print('Linear Complexity Test DEBUG BEGIN:')
                print("\tLength of input:\t", length_of_binary_data)
                print('\tLength in bits of a block:\t', )
                print("\tDegree of Freedom:\t\t", degree_of_freedom)
                print('\tNumber of Blocks:\t', number_of_block)
                print('\tValue of Vs:\t\t', vg)
                print('\txObs:\t\t\t\t', xObs)
                print('\tP-Value:\t\t\t', p_value)
                print('DEBUG END.')


            return (p_value, (p_value >= 0.01))
        else:
            return (-1.0, False)

    @staticmethod
    def berlekamp_massey_algorithm(block_data):
        n = len(block_data)
        c = zeros(n)
        b = zeros(n)
        c[0], b[0] = 1, 1
        l, m, i = 0, -1, 0
        int_data = [int(el) for el in block_data]
        while i < n:
            v = int_data[(i - l):i]
            v = v[::-1]
            cc = c[1:l + 1]
            d = (int_data[i] + dot(v, cc)) % 2
            if d == 1:
                temp = copy(c)
                p = zeros(n)
                for j in range(0, l):
                    if b[j] == 1:
                        p[j + i - m] = 1
                c = (c + p) % 2
                if l <= 0.5 * i:
                    l = i + 1 - l
                    m = i
                    b = temp
            i += 1
        return l