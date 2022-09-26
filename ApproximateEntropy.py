from math import log as log
from numpy import zeros as zeros
from scipy.special import gammaincc as gammaincc

class ApproximateEntropy:

    @staticmethod
    def approximate_entropy_test(binary_data:str, verbose=False, pattern_length=10):

        length_of_binary_data = len(binary_data)

        binary_data += binary_data[:pattern_length + 1:]
        max_pattern = ''
        for i in range(pattern_length + 2):
            max_pattern += '1'

        vobs_01 = zeros(int(max_pattern[0:pattern_length:], 2) + 1)
        vobs_02 = zeros(int(max_pattern[0:pattern_length + 1:], 2) + 1)

        for i in range(length_of_binary_data):
            # Work out what pattern is observed
            vobs_01[int(binary_data[i:i + pattern_length:], 2)] += 1
            vobs_02[int(binary_data[i:i + pattern_length + 1:], 2)] += 1

        vobs = [vobs_01, vobs_02]

        sums = zeros(2)
        for i in range(2):
            for j in range(len(vobs[i])):
                if vobs[i][j] > 0:
                    sums[i] += vobs[i][j] * log(vobs[i][j] / length_of_binary_data)
        sums /= length_of_binary_data
        ape = sums[0] - sums[1]

        xObs = 2.0 * length_of_binary_data * (log(2) - ape)

        p_value = gammaincc(pow(2, pattern_length - 1), xObs / 2.0)

        if verbose:
            print('Approximate Entropy Test DEBUG BEGIN:')
            print("\tLength of input:\t\t\t", length_of_binary_data)
            print('\tLength of each block:\t\t', pattern_length)
            print('\tApEn(m):\t\t\t\t\t', ape)
            print('\txObs:\t\t\t\t\t\t', xObs)
            print('\tP-Value:\t\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))