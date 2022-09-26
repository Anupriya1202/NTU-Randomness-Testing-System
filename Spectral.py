from math import fabs as fabs
from math import floor as floor
from math import log as log
from math import sqrt as sqrt
from numpy import where as where
from scipy import fftpack as sff
from scipy.special import erfc as erfc

class SpectralTest:

    @staticmethod
    def spectral_test(binary_data:str, verbose=False):

        length_of_binary_data = len(binary_data)
        plus_one_minus_one = []

        for char in binary_data:
            if char == '0':
                plus_one_minus_one.append(-1)
            elif char == '1':
                plus_one_minus_one.append(1)


        spectral = sff.fft(plus_one_minus_one)

        slice = floor(length_of_binary_data / 2)
        modulus = abs(spectral[0:slice])
        tau = sqrt(log(1 / 0.05) * length_of_binary_data)

        n0 = 0.95 * (length_of_binary_data / 2)
        n1 = len(where(modulus < tau)[0])
        d = (n1 - n0) / sqrt(length_of_binary_data * (0.95) * (0.05) / 4)
        p_value = erfc(fabs(d) / sqrt(2))

        if verbose:
            print('Discrete Fourier Transform (Spectral) Test DEBUG BEGIN:')
            print('\tLength of Binary Data:\t', length_of_binary_data)
            print('\tValue of T:\t\t\t\t', tau)
            print('\tValue of n1:\t\t\t', n1)
            print('\tValue of n0:\t\t\t', n0)
            print('\tValue of d:\t\t\t\t', d)
            print('\tP-Value:\t\t\t\t', p_value)
            print('DEBUG END.')

        return (p_value, (p_value >= 0.01))
