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
    # shape_name = "_doublefreq_%.2f_%.1f" % (pul_len / 10 ** 6, o1)
    if add is None:
        shape_name = "g_%.0f_ACT_shape_%.0f" % (pul_len / 10 ** 3, o1 * 10)
    else:
        shape_name = "3_off_15C_%.0f_3CH3Py_shape_%.0f" % (pul_len / 10 ** 3, o1 * 10) + "_%s" % add
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


def make_shape_files(freq1, freq2, pul_len, number_of_points, std):
    o1 = (freq1 + freq2) / 2
    offset_freq = (freq1 - freq2) / 2
    tau = pul_len * 10 ** -6 / (number_of_points - 1)
    mean = number_of_points / 2

    t = np.zeros(number_of_points)
    shape = np.zeros(number_of_points)
    amplitude = np.zeros(number_of_points)
    phase = np.zeros(number_of_points)
    for i in range(number_of_points):
        t[i] = i * tau
        if np.cos(2 * np.pi * offset_freq * tau * i) < 0:
            phase[i] = 180
            amplitude[i] = -np.exp(- 1 / 2 * ((i - mean) / std) ** 2) * np.cos(2 * np.pi * offset_freq * tau * i)
        else:
            phase[i] = 0
            amplitude[i] = np.exp(- 1 / 2 * ((i - mean) / std) ** 2) * np.cos(2 * np.pi * offset_freq * tau * i)
        shape[i] = amplitude[i] * np.cos(phase[i] / 180 * np.pi)
    make_topspin_file(o1, amplitude, phase)


'''
def make_concatenated_shapes(freq1, freq2, pul_len, number_of_points, std):
    # number_of_points = in one shape!!!
    # pul_len = full pulse_len (shape1 + shape2)
    o1 = (freq1 + freq2) / 2
    offset_freq = (freq1 - freq2) / 2
    tau = pul_len * 10 ** -6 / (2 * number_of_points - 1)
    mean = number_of_points

    shape = np.zeros(number_of_points)
    amplitude = np.zeros(number_of_points)
    phase = np.zeros(number_of_points)
    for i in range(number_of_points):
        if np.cos(2 * np.pi * offset_freq * tau * i) < 0:
            phase[i] = 180
            amplitude[i] = -np.exp(- 1 / 2 * ((i - mean) / (2 * std)) ** 2) * np.cos(2 * np.pi * offset_freq * tau * i)
        else:
            phase[i] = 0
            amplitude[i] = np.exp(- 1 / 2 * ((i - mean) / (2 * std)) ** 2) * np.cos(2 * np.pi * offset_freq * tau * i)
        shape[i] = amplitude[i] * np.cos(phase[i] / 180 * np.pi)
    make_topspin_file(o1, amplitude, phase, add="p1")
    plt.plot(shape)
    plt.show()

    for i in range(number_of_points):
        if np.cos(2 * np.pi * offset_freq * tau * (i + number_of_points)) < 0:
            phase[i] = 180
            amplitude[i] = -np.exp(- 1 / 2 * ((i + number_of_points - mean) / (2 * std)) ** 2) * \
                           np.cos(2 * np.pi * offset_freq * tau * (i + number_of_points))
        else:
            phase[i] = 0
            amplitude[i] = np.exp(- 1 / 2 * ((i + number_of_points - mean) / (2 * std)) ** 2) * \
                           np.cos(2 * np.pi * offset_freq * tau * (i + number_of_points))
        shape[i] = amplitude[i] * np.cos(phase[i] / 180 * np.pi)
    make_topspin_file(o1, amplitude, phase, add="p2")
    plt.plot(shape)
    plt.show()
'''


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
        # plt.plot(shape)
        # plt.show()
        make_topspin_file(o1, amplitude, phase, add=p[j])

    '''
    ## RECTANGULAR
    for j in range(number_of_parts):
        for i in range(number_of_points):
            if np.cos(2 * np.pi * offset_freq * tau * (i + j * number_of_points)) < 0:
                phase[i] = 180
                amplitude[i] = -np.cos(2 * np.pi * offset_freq * tau * (i + j * number_of_points))
            else:
                phase[i] = 0
                amplitude[i] = np.cos(2 * np.pi * offset_freq * tau * (i + j * number_of_points))
            shape[i] = amplitude[i] * np.cos(phase[i] / 180 * np.pi)
        # plt.plot(shape)
        # plt.show()
        make_topspin_file(o1, amplitude, phase, add=p[j])
    '''


# in ref frame rotating with nu_ref
def H(I, nu_1_max, nu_ref, nu_res, shape):
    h = - 2 * np.pi * (nu_res - nu_ref) * I[0][2] - 2 * np.pi * nu_1_max * shape * I[0][0]
    return h


# in us
pul_len = int(0.3 * 10 ** 6)
number_of_points = int(0.26 * 10 ** 5)
std = int(0.26 * 17000)

# make_shape_files(3000, -100, pul_len, number_of_points, std)
# make_shape_files(4000, -1000, pul_len, number_of_points, std)
'''
make_concatenated_shapes(8900, -3400, pul_len, 6, number_of_points, std)
make_concatenated_shapes(8900, -3410, pul_len, 6, number_of_points, std)
make_concatenated_shapes(8900, -3420, pul_len, 6, number_of_points, std)
make_concatenated_shapes(8900, -3430, pul_len, 6, number_of_points, std)
make_concatenated_shapes(8900, -3440, pul_len, 6, number_of_points, std)
make_concatenated_shapes(8900, -3450, pul_len, 6, number_of_points, std)
make_concatenated_shapes(8900, -3460, pul_len, 6, number_of_points, std)
make_concatenated_shapes(8900, -3470, pul_len, 6, number_of_points, std)
'''

number_of_freqs = 25
freq_hyd = -8837
freq = np.linspace(3220, 3340, number_of_freqs)
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


'''
freq = np.linspace(3200, 3350, 51)
for i in range(len(freq)):
    make_shape_files(freq[i], -8904, pul_len, number_of_points, std)
'''

'''
freq1 = 640
freq2 = -640
pul_len = int(0.01 * 10 ** 6)
number_of_points = int(0.7 * 10 ** 5)
std = int(0.7 * 20000)
o1 = (freq1 + freq2) / 2
offset_freq = (freq1 - freq2) / 2
tau = pul_len * 10 ** -6 / (number_of_points - 1)
mean = number_of_points / 2

t = np.zeros(number_of_points)
shape = np.zeros(number_of_points)
amplitude = np.zeros(number_of_points)
phase = np.zeros(number_of_points)


for i in range(number_of_points):
    t[i] = i * tau
    if np.cos(2 * np.pi * offset_freq * tau * i) < 0:
        phase[i] = 180
        amplitude[i] = -np.exp(- 1 / 2 * ((i - mean) / std) ** 2) * np.cos(2 * np.pi * offset_freq * tau * i)
    else:
        phase[i] = 0
        amplitude[i] = np.exp(- 1 / 2 * ((i - mean) / std) ** 2) * np.cos(2 * np.pi * offset_freq * tau * i)
    shape[i] = amplitude[i] * np.cos(phase[i] / 180 * np.pi)


####### Spin 1/2 excitation profie
I = make_spin_operators(1)
p_zero = I[0][2]
p = p_zero
number_of_freqs = 20
nu_1_max = 100

freqs = np.linspace(500, 800, number_of_freqs)
M_x = np.zeros(number_of_freqs)
M_y = np.zeros(number_of_freqs)
M_z = np.zeros(number_of_freqs)

for i in range(number_of_freqs):
    for j in range(number_of_points):
        p = la.expm(-1j * H(I, nu_1_max, o1, freqs[i], shape[j]) * tau) @ p @ \
            la.expm(1j * H(I, nu_1_max, o1, freqs[i], shape[j]) * tau)
    M_x[i] = 2 * np.real(np.trace(p @ I[0][0]))
    M_y[i] = 2 * np.real(np.trace(p @ I[0][1]))
    M_z[i] = 2 * np.real(np.trace(p @ I[0][2]))
    p = p_zero
    print(str(freqs[i]) + ' ' + str(M_x[i]) + ' ' + str(M_y[i]) + ' ' + str(M_z[i]))

plt.plot(freqs, M_y)
plt.show()
'''