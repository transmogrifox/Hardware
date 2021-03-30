import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from modulator import steadyState, modulatorSystem, smallSignal
from output_impedance import outputZ
from error_amp import errorAmp
from current_sense_gain import currentSenseGain


def plot_response(f, H, G):
    H_dB = 20.0*np.log10(np.abs(H))
    G_dB = 20.0*np.log10(np.abs(G))

    H_deg = 180.0*np.unwrap(np.angle(H))/np.pi
    G_deg = 180.0*np.unwrap(np.angle(G))/np.pi

    #Import measured data
    dp = pd.read_csv("./data/rev_j_2021-03-29T17_29_52_125VDC_3A_neg45C.csv")
    fm = dp['Frequency (Hz)']
    m = dp['Trace 1: Gain: Magnitude (dB)']
    p = dp['Trace 2: Gain: Phase (deg)']


    fig, ax = plt.subplots(nrows=2,ncols=1)
    fig.subplots_adjust(hspace=0.35, wspace=0)
    plt.subplot(2, 1, 1)
    #plt.semilogx(f, H_dB,"r")
    plt.semilogx(f, G_dB,"g", label="Simulated")
    plt.semilogx(fm, m,"m", label="Measured")
    plt.title('B1309 Open Loop Gain Response: \nVin = 125 VDC, Load = 3A, Tamb = -45 \xb0C\n\nMagnitude')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    plt.legend(loc="upper right")
    plt.grid()
    plt.subplot(2, 1, 2)
    #plt.semilogx(f, H_deg,"b")
    plt.semilogx(f, G_deg,"g", label="Simulated")
    plt.semilogx(fm, p,"m", label="Measured")
    plt.title('Phase')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (\xb0)')
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()


##
## Test Program
##

# Steady State parameters
sys = modulatorSystem(75.0, 12.5, 0.75, 3.0, 120000.0, 580e-6, 0.0, 80000.0, (54.0/8.0), "FLYBACK", "DCMCCM")
ss =  steadyState(sys)
ss.print_sys_params()

sys.Vin = 123.0
print("\n\nChange input voltage to ", sys.Vin, " Volts")
ss.update(sys)
ss.print_sys_params()

# Modulator small signal response
slsg = smallSignal(ss, 10.0, 120.0e3, 1000)
#slsg.plot_response(slsg.f, slsg.Fdg)

# Error amplifier and loop compensation
CTR = 0.78
fopto = 50e3
ea1 = errorAmp(2.5, 8250.0, 1000.0, 33000.0, 121000.0, 22e-9, 100e-12, CTR, \
              fopto, 10.0, 120e3, 1000)

ea2 = errorAmp(2.5, 8250.0, 1000.0, 33000.0, 121000.0, 33e-9, 100e-12, CTR, \
              fopto, 10.0, 120e3, 1000)

# Current sensing node feedback gain (Ic/ea)
cs = currentSenseGain(0.333, 1.24e3, 2.21e3, 2.21e3, 20.0e3, 15.4e3, 1.18e6)

# Output Impedance
cout = 0.95*3.0*330.0e-6
cload = 0.95*330.0e-6
lout = 470.0e-9
cesr = 0.008
lesr = 0.004

zo = outputZ(cout, cload, lout, cesr/3.0, cesr, lesr, 4.2,\
             10.0, 120e3, 1000)


plot_response(ea1.f, ea1.Hc*cs.Gav*slsg.Fdg*zo.Zout, ea2.Hc*cs.Gav*slsg.Fdg*zo.Zout)
