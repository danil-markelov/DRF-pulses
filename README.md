# DRF-pulses

"Pulse_generator.py" generates DRF-pulses to excite desired frequencies. As a result, you will have a set of TopSpin(TS)-compatible shapes and two txt-files entitled as "shape_names" and "o1_names". "shape_names" contains the name of the pulses, whereas "o1_names" contains corresponding O1 (carrier frequency in TS in Hz) that should be set in TS for the correct behavior of the shapes. The shape pulses could be directly transfered to the TS shapes without any changes required. To run the DRF-SABRE experiment, we recommend to use the AU-program "AU_DRF" to automatically run the experiments. In this experiments, nu_rf_t (frequency which excites the "trans"-proton) remains constant (preferably, resonant), while nu_rf_s is varied in the desired range.

Within the code, we reccomend not to change any variables, except of:
1) "shape_name", where you enter the name of the pulse. For example, "Py_300_1000". The first number is the length of the pulse. The second number is O1p (carrier freqeuncy) that have to be set in the experiment in order to provide correct DRF excitation. Note that O1p is varied from pulse to pulse and used in the filename to distinguish them.
2) "number_of_points", where you set the number of nu_rf_s to be excited.
3) "freq", where you set the range of frequencies excited by nu_rf_s.
4) "freq_hyd", where you set the frequency of the "trans"-hydride proton in the complex (preferably, on-resonant to this proton).

# Guideline
1) Use the TS-program "DRF_TS_program". As you can see, 4 shapenames are required. Each DRF-shape is represented as a sequence of 4 consectuive pulses (we are not going into details of the technical implementation). Set the length of each pulse equal to pul_len / 4. For example, if you enetered 300 ms of pulse duration in "pulse_generator.py", you should set p11 = 300 ms / 4 = 75 ms. The amplitudes of the pulses have to be set indetical (for example, the amplitudes of all 4 pulses of 40 Hz).
2) Then use AU-program "DRF_AU_program". This program 
