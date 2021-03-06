Derivations supporting an unconventional approach to expressing the frequency domain transfer function of a peak current control switch-mode converter.  This method deviates from the construct of the averaged-switch model (ASM) first credited to Vatche Vorperian.

In this derivation strategy,
1) The peak current control signal is sampled with an impulse train (Zero-order-hold), then re-sampled at time coincident to the valley currents. 
2) The transfer function relating control current (trip threshold) to valley currents is expressed as difference equation (discrete-time IIR filter).  A similar approach is presented in almost all analyses of the current control inner loop, but I am currently unaware of any work in which the significance of the relationship between valley currents and average currents is appreciated as a discrete-time system, e.g. as a convoloution of an FIR response with an IIR response.
3) The transfer function relating valley currents to average input (charge cycle) and output (discharge cycle) currents is expressed as a discrete time FIR filter.
4) It is observed the FIR filter is non-LTI. Small-signal analysis is applied to the nonlinear function to arrive at a first-order discrete-time FIR filter response. The right-half plane zero in flyback converters appears in this step while this approach suggests that the right-half plane zero disappears in DCM due to aliasing.
5) The sequence of impulses generated by convolution of control current with valley current and average current transfer functions is reconstructed interpreting the ramp + box waveform as an impulse response. The impulse response shape is characteristic to the inductor charge and discharge current waveforms.

An interesting historical perspective on analysis of switch-mode converters:
https://ieeetv.ieee.org/ieeetv-specials/keytalk-vatche-vorperian-a-historical-perspective-of-the-development-of-the-pwm-switch-model-apec-2017
