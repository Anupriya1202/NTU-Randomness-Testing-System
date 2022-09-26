from numpy import zeros as zeros
from scipy.special import gammaincc as gammaincc
class Serial:

    @staticmethod
    def serial_test(binary_data:str, verbose=False, pattern_length=16):
        length_of_binary_data = len(binary_data)
        binary_data += binary_data[:(pattern_length -1):]
        max_pattern = ''
        for i in range(pattern_length + 1):
            max_pattern += '1'
        vobs_01 = zeros(int(max_pattern[0:pattern_length:], 2) + 1)
        vobs_02 = zeros(int(max_pattern[0:pattern_length - 1:], 2) + 1)
        vobs_03 = zeros(int(max_pattern[0:pattern_length - 2:], 2) + 1)

        for i in range(length_of_binary_data):

            vobs_01[int(binary_data[i:i + pattern_length:], 2)] += 1
            vobs_02[int(binary_data[i:i + pattern_length - 1:], 2)] += 1
            vobs_03[int(binary_data[i:i + pattern_length - 2:], 2)] += 1

        vobs = [vobs_01, vobs_02, vobs_03]

        sums = zeros(3)
        for i in range(3):
            for j in range(len(vobs[i])):
                sums[i] += pow(vobs[i][j], 2)
            sums[i] = (sums[i] * pow(2, pattern_length - i) / length_of_binary_data) - length_of_binary_data

        nabla_01 = sums[0] - sums[1]
        nabla_02 = sums[0] - 2.0 * sums[1] + sums[2]
        p_value_01 = gammaincc(pow(2, pattern_length - 1) / 2, nabla_01 / 2.0)
        p_value_02 = gammaincc(pow(2, pattern_length - 2) / 2, nabla_02 / 2.0)

        if verbose:
            print('Serial Test DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_binary_data)
            print('\tValue of Sai:\t\t', sums)
            print('\tValue of Nabla:\t\t', nabla_01, nabla_02)
            print('\tP-Value 01:\t\t\t', p_value_01)
            print('\tP-Value 02:\t\t\t', p_value_02)
            print('DEBUG END.')

        return ((p_value_01, p_value_01 >= 0.01), (p_value_02, p_value_02 >= 0.01))