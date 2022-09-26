from math import floor as floor
from numpy import array as array
from numpy import exp as exp
from numpy import zeros as zeros
from scipy.special import gammaincc as gammaincc
from scipy.special import hyp1f1 as hyp1f1


class TemplateMatching:

    @staticmethod
    def non_overlapping_test(binary_data:str, verbose=False, template_pattern='000000001', block=8):

        length_of_binary = len(binary_data)
        pattern_size = len(template_pattern)
        block_size = floor(length_of_binary / block)
        pattern_counts = zeros(block)

        for count in range(block):
            block_start = count * block_size
            block_end = block_start + block_size
            block_data = binary_data[block_start:block_end]
            inner_count = 0
            while inner_count < block_size:
                sub_block = block_data[inner_count:inner_count+pattern_size]
                if sub_block == template_pattern:
                    pattern_counts[count] += 1
                    inner_count += pattern_size
                else:
                    inner_count += 1


            mean = (block_size - pattern_size + 1) / pow(2, pattern_size)
            variance = block_size * ((1 / pow(2, pattern_size)) - (((2 * pattern_size) - 1) / (pow(2, pattern_size * 2))))

        xObs = 0
        for count in range(block):
            xObs += pow((pattern_counts[count] - mean), 2.0) / variance
        p_value = gammaincc((block / 2), (xObs / 2))

        if verbose:
            print('Non-Overlapping Template Test DEBUG BEGIN:')
            print("\tLength of input:\t\t", length_of_binary)
            print('\tValue of Mean (µ):\t\t', mean)
            print('\tValue of Variance(σ):\t', variance)
            print('\tValue of W:\t\t\t\t', pattern_counts)
            print('\tValue of xObs:\t\t\t', xObs)
            print('\tP-Value:\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))

    @staticmethod
    def overlapping_patterns(binary_data:str, verbose=False, pattern_size=9, block_size=1032):
        length_of_binary_data = len(binary_data)
        pattern = ''
        for count in range(pattern_size):
            pattern += '1'

        number_of_block = floor(length_of_binary_data / block_size)


        lambda_val = float(block_size - pattern_size + 1) / pow(2, pattern_size)

        eta = lambda_val / 2.0

        pi = [TemplateMatching.get_prob(i, eta) for i in range(5)]
        diff = float(array(pi).sum())
        pi.append(1.0 - diff)

        pattern_counts = zeros(6)
        for i in range(number_of_block):
            block_start = i * block_size
            block_end = block_start + block_size
            block_data = binary_data[block_start:block_end]

            pattern_count = 0
            j = 0
            while j < block_size:
                sub_block = block_data[j:j + pattern_size]
                if sub_block == pattern:
                    pattern_count += 1
                j += 1
            if pattern_count <= 4:
                pattern_counts[pattern_count] += 1
            else:
                pattern_counts[5] += 1

        xObs = 0.0
        for i in range(len(pattern_counts)):
            xObs += pow(pattern_counts[i] - number_of_block * pi[i], 2.0) / (number_of_block * pi[i])

        p_value = gammaincc(5.0 / 2.0, xObs / 2.0)

        if verbose:
            print('Overlapping Template Test DEBUG BEGIN:')
            print("\tLength of input:\t\t", length_of_binary_data)
            print('\tValue of Vs:\t\t\t', pattern_counts)
            print('\tValue of xObs:\t\t\t', xObs)
            print('\tP-Value:\t\t\t\t', p_value)
            print('DEBUG END.')


        return (p_value, (p_value >= 0.01))

    @staticmethod
    def get_prob(u, x):
        out = 1.0 * exp(-x)
        if u != 0:
            out = 1.0 * x * exp(2 * -x) * (2 ** -u) * hyp1f1(u + 1, 2, x)
        return out