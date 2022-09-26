from math import isnan as isnan
from numpy import abs as abs
from numpy import append as append
from numpy import array as array
from numpy import clip as clip
from numpy import cumsum as cumsum
from numpy import ones as ones
from numpy import sqrt as sqrt
from numpy import sum as sum
from numpy import transpose as transpose
from numpy import where as where
from numpy import zeros as zeros
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc

class RandomExcursions:

    @staticmethod
    def random_excursions_test(binary_data:str, verbose=False, state=1):


        length_of_binary_data = len(binary_data)

        sequence_x = zeros(length_of_binary_data)
        for i in range(len(binary_data)):
            if binary_data[i] == '0':
                sequence_x[i] = -1.0
            else:
                sequence_x[i] = 1.0

        cumulative_sum = cumsum(sequence_x)

        cumulative_sum = append(cumulative_sum, [0])
        cumulative_sum = append([0], cumulative_sum)

        x_values = array([-4, -3, -2, -1, 1, 2, 3, 4])
        index = x_values.tolist().index(state)
        position = where(cumulative_sum == 0)[0]

        cycles = []
        for pos in range(len(position) - 1):

            cycles.append(cumulative_sum[position[pos]:position[pos + 1] + 1])
        num_cycles = len(cycles)

        state_count = []
        for cycle in cycles:

            state_count.append(([len(where(cycle == state)[0]) for state in x_values]))
        state_count = transpose(clip(state_count, 0, 5))

        su = []
        for cycle in range(6):
            su.append([(sct == cycle).sum() for sct in state_count])
        su = transpose(su)

        pi = ([([RandomExcursions.get_pi_value(uu, state) for uu in range(6)]) for state in x_values])
        inner_term = num_cycles * array(pi)
        xObs = sum(1.0 * (array(su) - inner_term) ** 2 / inner_term, axis=1)
        p_values = ([gammaincc(2.5, cs / 2.0) for cs in xObs])

        if verbose:
            print('Random Excursion Test DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_binary_data)
            count = 0
            print('\t\t STATE \t\t\t xObs \t\t\t\t\t\t p_value  \t\t\t\t\t Result')
            for item in p_values:
                print('\t\t', repr(x_values[count]).rjust(2), ' \t\t ', xObs[count],' \t\t ', repr(item).rjust(21), ' \t\t\t ', (item >= 0.01))
                count += 1
            print('DEBUG END.')

        states = ['-4', '-3', '-2', '-1', '+1', '+2', '+3', '+4',]
        result = []
        count = 0
        for item in p_values:
            result.append((states[count], x_values[count], xObs[count], item, (item >= 0.01)))
            count += 1

        return result

    @staticmethod
    def variant_test(binary_data:str, verbose=False):

        length_of_binary_data = len(binary_data)
        int_data = zeros(length_of_binary_data)

        for count in range(length_of_binary_data):
            int_data[count] = int(binary_data[count])

        sum_int = (2 * int_data) - ones(len(int_data))
        cumulative_sum = cumsum(sum_int)

        li_data = []
        index = []
        for count in sorted(set(cumulative_sum)):
            if abs(count) <= 9:
                index.append(count)
                li_data.append([count, len(where(cumulative_sum == count)[0])])

        j = RandomExcursions.get_frequency(li_data, 0) + 1

        p_values = []
        for count in (sorted(set(index))):
            if not count == 0:
                den = sqrt(2 * j * (4 * abs(count) - 2))
                p_values.append(erfc(abs(RandomExcursions.get_frequency(li_data, count) - j) / den))

        count = 0

        for data in li_data:
            if data[0] == 0:
                li_data.remove(data)
                index.remove(0)
                break
            count += 1

        if verbose:
            print('Random Excursion Variant Test DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_binary_data)
            print('\tValue of j:\t\t', j)
            print('\tP-Values:')
            print('\t\t STATE \t\t COUNTS \t\t P-Value \t\t Conclusion')
            count = 0
            for item in p_values:
                print('\t\t', repr(li_data[count][0]).rjust(4), '\t\t', li_data[count][1], '\t\t', repr(item).ljust(14), '\t\t', (item >= 0.01))
                count += 1
            print('DEBUG END.')


        states = []
        for item in index:
            if item < 0:
                states.append(str(item))
            else:
                states.append('+' + str(item))

        result = []
        count = 0
        for item in p_values:
            result.append((states[count], li_data[count][0], li_data[count][1], item, (item >= 0.01)))
            count += 1

        return result

    @staticmethod
    def get_pi_value(k, x):

        if k == 0:
            out = 1 - 1.0 / (2 * abs(x))
        elif k >= 5:
            out = (1.0 / (2 * abs(x))) * (1 - 1.0 / (2 * abs(x))) ** 4
        else:
            out = (1.0 / (4 * x * x)) * (1 - 1.0 / (2 * abs(x))) ** (k - 1)
        return out

    @staticmethod
    def get_frequency(list_data, trigger):

        frequency = 0
        for (x, y) in list_data:
            if x == trigger:
                frequency = y
        return frequency