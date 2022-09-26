from math import fabs as fabs
from math import floor as floor
from math import sqrt as sqrt
from scipy.special import erfc as erfc
from scipy.special import gammaincc as gammaincc

class FrequencyTest:

    @staticmethod
    def monobit_test(binary_data:str, verbose=False):

        length_of_bit_string = len(binary_data)

        count = 0
        for bit in binary_data:
            if bit == '0':
                count -= 1
            elif bit == '1':
                count += 1

        sObs = count / sqrt(length_of_bit_string)

        p_value = erfc(fabs(sObs) / sqrt(2))

        if verbose:
            print('Frequency Test (Monobit Test) DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_bit_string)
            print('\t# of \'0\':\t\t\t', binary_data.count('0'))
            print('\t# of \'1\':\t\t\t', binary_data.count('1'))
            print('\tS(n):\t\t\t\t', count)
            print('\tsObs:\t\t\t\t', sObs)
            print('\tf:\t\t\t\t\t',fabs(sObs) / sqrt(2))
            print('\tP-Value:\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))

    @staticmethod
    def block_frequency(binary_data:str, block_size=128, verbose=False):

        length_of_bit_string = len(binary_data)


        if length_of_bit_string < block_size:
            block_size = length_of_bit_string

        number_of_blocks = floor(length_of_bit_string / block_size)

        if number_of_blocks == 1:

            return FrequencyTest.monobit_test(binary_data[0:block_size])

        block_start = 0
        block_end = block_size
        proportion_sum = 0.0


        for counter in range(number_of_blocks):

            block_data = binary_data[block_start:block_end]
            one_count = 0
            for bit in block_data:
                if bit == '1':
                    one_count += 1

            pi = one_count / block_size


            proportion_sum += pow(pi - 0.5, 2.0)

            block_start += block_size
            block_end += block_size

        result = 4.0 * block_size * proportion_sum
        p_value = gammaincc(number_of_blocks / 2, result / 2)

        if verbose:
            print('Frequency Test (Block Frequency Test) DEBUG BEGIN:')
            print("\tLength of input:\t", length_of_bit_string)
            print("\tSize of Block:\t\t", block_size)
            print('\tNumber of Blocks:\t', number_of_blocks)
            print('\tCHI Squared:\t\t', result)
            print('\t1st:\t\t\t\t', number_of_blocks / 2)
            print('\t2nd:\t\t\t\t', result / 2)
            print('\tP-Value:\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))