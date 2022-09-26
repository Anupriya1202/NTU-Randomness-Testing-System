from math import fabs as fabs
from math import floor as floor
from math import sqrt as sqrt
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc
from scipy import zeros as zeros

class RunTest:

    @staticmethod
    def run_test(binary_data:str, verbose=False):

        one_count = 0
        vObs = 0
        length_of_binary_data = len(binary_data)

        tau = 2 / sqrt(length_of_binary_data)
        one_count = binary_data.count('1')

        pi = one_count / length_of_binary_data
        if abs(pi - 0.5) >= tau:

            return (0.0000, False)
        else:

            for item in range(1, length_of_binary_data):
                if binary_data[item] != binary_data[item - 1]:
                    vObs += 1
            vObs += 1

            # Step 4 - Compute p_value = erfc((|vObs − 2nπ * (1−π)|)/(2 * sqrt(2n) * π * (1−π)))
            p_value = erfc(abs(vObs - (2 * (length_of_binary_data) * pi * (1 - pi))) / (2 * sqrt(2 * length_of_binary_data) * pi * (1 - pi)))

        if verbose:
            print('Run Test DEBUG BEGIN:')
            print("\tLength of input:\t\t\t\t", length_of_binary_data)
            print("\tTau (2/sqrt(length of input)):\t", tau)
            print('\t# of \'1\':\t\t\t\t\t\t', one_count)
            print('\t# of \'0\':\t\t\t\t\t\t', binary_data.count('0'))
            print('\tPI (1 count / length of input):\t', pi)
            print('\tvObs:\t\t\t\t\t\t\t', vObs)
            print('\tP-Value:\t\t\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value > 0.01))

    @staticmethod
    def longest_one_block_test(binary_data:str, verbose=False):
        length_of_binary_data = len(binary_data)

        if length_of_binary_data < 128:

            return (0.00000, False, 'Error: Not enough data to run this test')
        elif length_of_binary_data < 6272:
            k = 3
            m = 8
            v_values = [1, 2, 3, 4]
            pi_values = [0.2148, 0.3672, 0.2305, 0.1875]
        elif length_of_binary_data < 750000:
            k = 5
            m = 128
            v_values = [4, 5, 6, 7, 8, 9]
            pi_values = [0.1174, 0.2430, 0.2493, 0.1752, 0.1027, 0.1124]
        else:
            k = 6
            m = 10000
            v_values = [10, 11, 12, 13, 14, 15, 16]
            pi_values = [0.0882, 0.2092, 0.2483, 0.1933, 0.1208, 0.0675, 0.0727]

        number_of_blocks = floor(length_of_binary_data / m)
        block_start = 0
        block_end = m
        xObs = 0

        frequencies = zeros(k + 1)

        for count in range(number_of_blocks):
            block_data = binary_data[block_start:block_end]
            max_run_count = 0
            run_count = 0

            for bit in block_data:
                if bit == '1':
                    run_count += 1
                    max_run_count = max(max_run_count, run_count)
                else:
                    max_run_count = max(max_run_count, run_count)
                    run_count = 0

            max(max_run_count, run_count)

            if max_run_count < v_values[0]:
                frequencies[0] += 1
            for j in range(k):
                if max_run_count == v_values[j]:
                    frequencies[j] += 1
            if max_run_count > v_values[k - 1]:
                frequencies[k] += 1

            block_start += m
            block_end += m

        for count in range(len(frequencies)):
            xObs += pow((frequencies[count] - (number_of_blocks * pi_values[count])), 2.0) / (
                    number_of_blocks * pi_values[count])

        p_value = gammaincc(float(k / 2), float(xObs / 2))

        if verbose:
            print('Run Test (Longest Run of Ones in a Block) DEBUG BEGIN:')
            print("\tLength of input:\t\t\t\t", length_of_binary_data)
            print("\tSize of each Block:\t\t\t\t", m)
            print('\tNumber of Block:\t\t\t\t', number_of_blocks)
            print("\tValue of K:\t\t\t\t\t\t", k)
            print('\tValue of PIs:\t\t\t\t\t', pi_values)
            print('\tFrequencies:\t\t\t\t\t', frequencies)
            print('\txObs:\t\t\t\t\t\t\t', xObs)
            print('\tP-Value:\t\t\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value > 0.01))