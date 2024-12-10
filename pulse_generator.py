import sys
from scipy import signal
import numpy as np
import scipy.linalg as la
from scipy.fft import fft, fftfreq
import matplotlib.pyplot as plt

shape_names = []
o1_names = []


def make_spin_operators(n):
    """
    function to make spin operators in a spin system
    which contains n 1/2 spins
    :param n: number of spins
    :return: list of lists of spin operators using sparse matrices
    """
    single_spin = [np.array([[0, 0.5], [0.5, 0]], dtype=np.complex_),
                   np.array([[0, -0.5 * 1j], [0.5 * 1j, 0]], dtype=np.complex_),
                   np.array([[0.5, 0], [0, -0.5]], dtype=np.complex_)]
    unity = np.eye(2, dtype=np.complex_)
    I = [single_spin.copy()]

    for i in range(n - 1):
        for j in range(len(I)):
            for k in range(3):
                I[j][k] = np.kron(I[j][k], unity)
        lst = []
        for k in range(3):
            lst.append(np.kron(np.eye(2 ** (i + 1)), single_spin[k]))
        I.append(lst)
    return I


# !!70.000 is the maximal shape size in TopSpin!!
# Each shape requires O1 adjustment - don't forget!
# Amplitude normalized (100 is max, 0 is min)
# Phase in degrees (0, 360)

def make_topspin_file(o1, amplitude, phase, add=None):
    with open("header", 'r') as f:
        header = "".join(f.readlines())
        f.close()

    # !!IMPORTANT!!
    # In variable "shape_name" enter the name of the shape. We recommend to use the following template:
    # "name_300_1000", where the first number is the length of the DRF pulse in ms,
    # and the second number is O1p which should be used in the experiment with the pulse. O1p is
    # calculated automatically in the code; for the pul_len we recommend to use 300 ms.
    
    shape_name = "Py_%.0f_%.0f" % (pul_len / 10 ** 3, o1 * 10) + "_%s" % add
    shape_names.append(shape_name)
    with open(shape_name, 'w') as f:
        sys.stdout = f
        print(header)
        for i in range(len(amplitude)):
            st = str('{:.5e}'.format(round(amplitude[i] * 100, 5))) + ', ' + str('{:.5e}'.format(int(phase[i])))
            print(st)
        print('##END=')
        f.close()
    sys.stdout = sys.__stdout__


def make_concatenated_shapes(freq1, freq2, pul_len, number_of_parts, number_of_points, std):
    # number_of_points = in one shape!!!
    # number_of_parts = number of concatenated shapes (odd!!!)
    # pul_len = full pulse_len (shape1 + shape2)
    p = []
    for i in range(number_of_parts):
        p.append("p" + "%d" % i)
    o1 = (freq1 + freq2) / 2
    o1_names.append(round(o1, 2))
    offset_freq = (freq1 - freq2) / 2
    tau = pul_len * 10 ** -6 / (number_of_parts * number_of_points - 1)
    mean = number_of_parts * number_of_points / 2

    shape = np.zeros(number_of_points)
    amplitude = np.zeros(number_of_points)
    phase = np.zeros(number_of_points)
    for j in range(number_of_parts):
        for i in range(number_of_points):
            if np.cos(2 * np.pi * offset_freq * tau * (i + j * number_of_points)) < 0:
                phase[i] = 180
                amplitude[i] = -np.exp(- 1 / 2 * ((i + j * number_of_points - mean) / (number_of_parts * std)) ** 2) *\
                               np.cos(2 * np.pi * offset_freq * tau * (i + j * number_of_points))
            else:
                phase[i] = 0
                amplitude[i] = np.exp(- 1 / 2 * ((i + j * number_of_points - mean) / (number_of_parts * std)) ** 2) *\
                               np.cos(2 * np.pi * offset_freq * tau * (i + j * number_of_points))
            shape[i] = amplitude[i] * np.cos(phase[i] / 180 * np.pi)
        make_topspin_file(o1, amplitude, phase, add=p[j])
        

# in us
pul_len = int(0.3 * 10 ** 6)

# Number of points in one shape. We strongly recommend not to change this parameter
number_of_points = int(0.26 * 10 ** 5)

# std / number_of_points is sigma (~ to the width of the Gaussian)
std = int(0.26 * 17000)

# number of nu_rf_s to be scanned
number_of_freqs = 25
# in "freq" enter the frequencies to be scanned to excite the complex-bound nucleus of interest
freq = np.linspace(3220, 3340, number_of_freqs)

# in "freq_hyd" enter the frequency of the "trans"-hydride proton with respect to the molecule of interest
freq_hyd = -8837

for i in range(number_of_freqs):
    make_concatenated_shapes(freq[i], freq_hyd, pul_len, 4, number_of_points, std)

with open('shape_names.txt', 'w') as f:
    sys.stdout = f
    for name in shape_names:
        print('"' + name + '"' + ',')

with open('o1_names.txt', 'w') as f:
    sys.stdout = f
    for o1 in o1_names:
        print(str(o1) + ',')
