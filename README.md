# DRF-pulses

# 1) Pulse generator
"Pulse_generator.py" generates the DRF-pulses to excite desired frequencies. As a result, you will have a set of TopSpin(TS)-compatible shapes and two txt-files entitled as "shape_names.txt" and "o1_names.txt". "shape_names.txt" contains the name of the pulses, whereas "o1_names.txt" contains corresponding O1 (the carrier frequency in TS in Hz) that should be set in a TS dataset for the correct behavior of the shapes. The shape pulses could be directly transfered to the TS shapes without any changes required. To run the DRF-SABRE experiment, we strongly recommend to use the AU-program "AU_DRF.txt" to automatically run the experiments.

Within the code, we recommend not to change any variables and functions, except of:

1) Variable "shape_name", where you enter the name of the pulse. In the code, use the following template: "Pyridine_300_1000". The first number is the length of the pulse (in ms). The second number is O1 (the carrier freqeuncy in Hz) that have to be set in the dataset in order to provide correct DRF excitation. No need to enter these numbers manually, as this procedure is automized, hoevever, you should manually change only the name of the molecule. We highlight that O1 is varied from pulse to pulse and used in the shape filename to distinguish them. Moreover, for the sake of technical implementation in TS, each DRF-pulse is represented as a sequence of 4 consecutive pulses. If, for example, we want to make the DRF pulse with 300 ms duration and O1 = 1000 Hz, the program will return us 4 shapes named as: "Pyridine_300_1000_p0"; "Pyridine_300_1000_p1"; "Pyridine_300_1000_p2"; "Pyridine_300_1000_p3" and two txt-files "shape_names.txt" and "o1_names.txt". The content of the files will be as follows:
   
 shape_names.txt = {"Pyridine_300_1000_p0",
                  "Pyridine_300_1000_p1",
                  "Pyridine_300_1000_p2",
                  "Pyridine_300_1000_p3",}
   
 o1_names.txt = {1000,}

2) Aray "freq", where you set the range of frequencies excited by nu_rf_s (the first and last frequency in Hz). For example, freq = np.linspace(3000, 4000, 20) makes frequency array from 3000 Hz to 4000 Hz, which consists of 20 equally spaced frequencies.

3) Variable "number_of_points", where you set the number of nu_rf_s to be excited. We recommend to adjust "number_of_points" and the first and last frequency in "freq" so that the increment in frequnecy will be 4-5 Hz (the increment is calculated as: increment = (last_freq - first_freq) / (number_of_points - 1)) 

4) Variable "freq_hyd", where you set the frequency nu_rf_t which excites the "trans"-hydride proton in the complex (Preferably, nu_rf_t = nu_res_t, i.e. set nu_rf_t on-resonance to this proton; nu_res_t can easily be found from the NMR spectrum).

5) Vairable "pul_len" which is the lenth of the DRF-pulse (in us). We recommend to use pul_len = 300 ms and do not exceed this value.

# 2) TS-program
The TS-program for DRF excitation can be found in "TS_program". As you can see, in this program we use 4 shapes in one experiment: sp1, sp2, sp3, sp4. This is because each DRF-shape is represented as a sequence of 4 consectuive shapes (we are not going into details of the technical implementation). Set the length of each pulse, p11, equal to pul_len / 4. For example, if you enetered 300 ms of pulse duration in "Pulse_generator.py", you should set p11 = 300 ms / 4 = 75 ms. Importantly, the amplitudes of the shape pulses have to be set indetical (for example, the amplitudes of all 4 pulses of 40 Hz).

# 3) AU-program
AU-program allows running the DRF-SABRE experiments automatically. In this experiments, nu_rf_t (excites the "trans"-hydride proton with respect to the complex-bound substrate) remains constant (preferably, resonant), while nu_rf_s (excites the complex-bound substrate) is varied in the desired range. In this program, you should change:
1) "N" is the number of different frequencies to be excited (N = number_of_points from "pulse_generator.py").
2) "char wavelist[][]" is an array which contains the names of all DRF-pulses. As we mentioned, DRF-pulse is a sequence of 4 pulses. Therefore, "wavelist" has the dimesion of 4*N (char walvelist[4*N][64]).
3) "double o1[]" is an array which contains all o1 frequencies (in Hz) that will be set in a dataset for correct behavior of the DRF excitation. The dimesion of "o1" is N (double o1[N])

# Guideline
1) Generate DRF pulses using "Pulse_generator.py". You will have a set of pulses and two .txt files. Transfer the DRF pulses into the TS-directory with your shape pulses.
2) Make a dataset with the TS-program attached. Set p11 (don't forget that p11 = pul_len / 4) and the amplitude of the shape pulses (they must be indetical).
3) Open the AU-program. Set N = number of frequencies, nu_rf_s, to be excited. Set dimesion of o1 = N (o1[N]), and the first dimension of wavelist = 4*N (wavelist[4*N][]). Copy the content of "shape_names.txt" into "wavelist", and the content of "o1_names.txt" into "o1".
4) Compile and then execute the AU-program. 
