from numpy import abs as abs
from numpy import array as array
from numpy import floor as floor
from numpy import max as max
from numpy import sqrt as sqrt
from numpy import sum as sum
from numpy import zeros as zeros
from scipy.stats import norm as norm

class CumulativeSums:

    @staticmethod
    def cumulative_sums_test(binary_data:str, mode=0, verbose=False):

        length_of_binary_data = len(binary_data)
        counts = zeros(length_of_binary_data)

        if not mode == 0:
            binary_data = binary_data[::-1]

        counter = 0
        for char in binary_data:
            sub = 1
            if char == '0':
                sub = -1
            if counter > 0:
                counts[counter] = counts[counter -1] + sub
            else:
                counts[counter] = sub

            counter += 1
        abs_max = max(abs(counts))

        start = int(floor(0.25 * floor(-length_of_binary_data / abs_max) + 1))
        end = int(floor(0.25 * floor(length_of_binary_data / abs_max) - 1))

        terms_one = []
        for k in range(start, end + 1):
            sub = norm.cdf((4 * k - 1) * abs_max / sqrt(length_of_binary_data))
            terms_one.append(norm.cdf((4 * k + 1) * abs_max / sqrt(length_of_binary_data)) - sub)

        start = int(floor(0.25 * floor(-length_of_binary_data / abs_max - 3)))
        end = int(floor(0.25 * floor(length_of_binary_data / abs_max) - 1))

        terms_two = []
        for k in range(start, end + 1):
            sub = norm.cdf((4 * k + 1) * abs_max / sqrt(length_of_binary_data))
            terms_two.append(norm.cdf((4 * k + 3) * abs_max / sqrt(length_of_binary_data)) - sub)

        p_value = 1.0 - sum(array(terms_one))
        p_value += sum(array(terms_two))

        if verbose:
            print('Cumulative Sums Test DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_binary_data)
            print('\tMode:\t\t\t\t', mode)
            print('\tValue of z:\t\t\t', abs_max)
            print('\tP-Value:\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))