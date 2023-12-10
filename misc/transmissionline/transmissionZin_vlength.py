#
#  Compute input impedance to coaxial cable terminated into an RC
#  matching network
#
#                                                 Rload (zt)
#                    z0                       ---/\/\/\/-----------
#         /\============================/\    |   Rmatch   Cblock |
#  Zin-> +++)++++++++++++++++++++++++++(++++--+--/\/\/\/----||----|
#         \/============================\/________________________|
#                                                                 |
#                                                               -----
#                                                                ---
#                                                                 -
#  z0 = Transmission line (coax) characteristic impedance
#  Rload = end-of-line input impedance (e.g. oscilloscope may be 1Meg | 10pF)
#
#  Rmatch should be selected such that (Rmatch | Rload) = z0,
#  Specifically,
#    Rmatch = Rload*z0/(Rload - z0)
#
#  Cblock is for the purpose of DC blocking.
#  Cblock should be selected to achiev a cut-off frequency
#  at which transmission line effect is negligible, and practically
#  zero impedance at higher frequencies where the transmission line 
#  effect is dominant.
#


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

#
# Constants
#
j=1j
pi = np.pi
C = 2.998e8 # Speed of light, meters/second
Ccoax = 2/3 # Propagation speed in coax as ratio of C

#
#  Default line parameters
#
z0_default = 50.0
zload = 1.0e6


#
# A transmission line input impedance
#  z0 = transmission line characteristic impedance
#  zL = load impedance at the terminating end
#  length = length of transmission line in meters
#  cline = propagation speed in transmission line expressed as a ratio
#          of the speed of light (C)
#
def computeZin(z0, zL, frequency, length, cline):

    cwire = cline*C          # Propagation speed in coax
    lmbda = cwire/frequency
    beta = 2.0*np.pi/lmbda

    # Reflection coefficient
    rL = (zL - z0) / (zL + z0)

    # return Zin
    return z0*(np.exp(j*beta*length) + rL*np.exp(-j*beta*length))/( np.exp(j*beta*length) - rL*np.exp(-j*beta*length) )

#
# Function: zinVlength
## Compute transmission line input impedance as a function of
##  length at a specific frequency
# z0 : transmission line characteristic impedance (ohms)
# zt : termination impedance (ohms)
# f0 : signal frequency of interest (Hz)
## Remaining parameters are for output data limits and density
# lstart : minimum length to process (meters)
# lstop : maximum length to process (meters)
# ppd : data density, points-per-decade
#
def zinVlength(z0=50, zt=1e4, fc=2.0e6, f0=66e6, lstart=0.001, lstop=4, ppd=1000):
    # Transmission line characteristics
    Cp = 1/(2*pi*fc*z0)

    # zx is the high frequency termination impedance such that
    # z0 = zt | zx, for a perfect match at frequencies well above
    # the RC filter cutoff
    if zt == z0:
        zx = zt
        fc = -1.0
    else:
        zx =  zt/(zt/z0 - 1)
    
    if fc > 0.0 :
        zc = zx + 1.0/(2j*pi*f0*Cp) # Load terminated to R + Xc (capacitor series resistor)
        zL = zt*zc/(zc+zt)
        legend = "f={:.2f}".format(f0/1e6) + "MHz" + ", fc={:.2f}".format(fc/1e6) + "MHz"
    else :
        zc = zx
        zL = zt

    ndec = int(np.log10(lstop/(10*lstart)))
    length = np.logspace(start=np.log10(lstart), stop=np.log10(lstop), num=ndec*ppd)  # Meters
    print("C = ", Cp)
    print("ndec= ", ndec, "\nstart= ", np.log10(lstart), "\nstop= ", np.log10(lstop), "\nnum= ", ndec*ppd)

    # Compute transmission line input impedance
    Zin = computeZin(z0, zL, f0, length, Ccoax)

    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.suptitle('Transmission Line Input Impedance vs. Length, '+legend)

    ax1.semilogx(length, abs(Zin))
    ax1.set_ylabel('Impedance Magnitude (ohms)')
    #ax1.set_xlabel('Length (meters)')

    ax2.semilogx(length, 180*np.angle(Zin)/np.pi)
    
    ax2.set_xlabel('Length (meters)')
    ax2.set_ylabel('Impedance Phase (deg)')

    plt.show()

    return length, Zin

#
# Function: zinVfreq   
## Compute transmission line input impedance as a function of
##  frequency at a specific length.
## In this function the termination impedance is a real-value "zt" (resistive)
##  in parallel with a series R-C network with R = z0 and C = 1/(2*pi*fc*z0)
# z0 : transmission line characteristic impedance (ohms)
# zt : termination impedance (ohms)
# fc : cut-off frequency of the RC termination
# length : transmission line length (meters)
## Remaining parameters are for output data limits and density
# fstart : minimum frequency to process (meters)
# fstop : maximum frequency to process (meters)
# ppd : data density, points-per-decade
#
def zinVfreq(z0=z0_default, zt=zload, fc=2.0e6, length=1.5, fstart=1e3, fstop=300e6, ppd=1000):
    # Transmission line characteristics
    ndec = int(np.log10(fstop/(10*fstart)))
    f0 = np.logspace(start=np.log10(fstart), stop=np.log10(fstop), num=ndec*ppd)  # Meters
    #fc = Ccoax*C/length  # Frequency at one wavelength
    Cp = 1/(2*pi*fc*z0)
    
    if zt == z0:
        zx = zt
        fc = -1.0
    else:
        zx =  zt/(zt/z0 - 1)
    
    if fc > 0.0 :
        zc = zx + 1.0/(2j*pi*f0*Cp) # Load terminated to R + Xc (capacitor series resistor)
        zL = zt*zc/(zc+zt)
    else :
        zc = zx
        zL = zt
    #zc = 1.0/(2j*pi*f0*Cp) 

    print("zx = ", zx)    
    print("fc = ", fc, "C = ", Cp)
    print("ndec= ", ndec, "\nstart= ", np.log10(fstart), "\nstop= ", np.log10(fstop), "\nnum= ", ndec*ppd)

    # Compute transmission line input impedance
    Zin = computeZin(z0, zL, f0, length, Ccoax)
    
    return f0, Zin


x,y = zinVfreq()

# Create the figure and the line that we will manipulate

fig, (ax1, ax2) = plt.subplots(2, 1)
fig.suptitle('Transmission Line Input Impedance vs. Frequency at Fixed Length')

line1, = ax1.semilogx(x, abs(y))
ax1.set_ylabel('Impedance Magnitude (ohms)')
#ax1.set_xlabel('Frequency (Hz)')

line2, = ax2.semilogx(x, 180*np.angle(y)/np.pi)

ax2.set_xlabel('Frequency (Hz)')
ax2.set_ylabel('Impedance Phase (deg)')

# adjust the main plot to make room for the sliders
plt.subplots_adjust(left=0.25, bottom=0.25)

# Make a horizontal slider to control the length.
axlen = plt.axes([0.25, 0.1, 0.65, 0.02])
len_slider = Slider(
    ax=axlen,
    label='Length [m]',
    valmin=0.01,
    valmax=30,
    valinit=1.5,
)

# Make a horizontal slider to control the RC termination cut-off.
axfc = plt.axes([0.25, 0.05, 0.65, 0.02])
fc_slider = Slider(
    ax=axfc,
    label='Cutoff [MHz]',
    valmin=0.01,
    valmax=100,
    valinit=2,
)

# The function to be called anytime a slider's value changes
def update(val):
    x,y = zinVfreq(length=len_slider.val, fc=1e6*fc_slider.val)
    line1.set_xdata(x)
    line1.set_ydata(abs(y))
    line2.set_xdata(x)
    line2.set_ydata(180*np.angle(y)/np.pi)
    fig.canvas.draw_idle()


# register the update function with each slider
len_slider.on_changed(update)
fc_slider.on_changed(update)

plt.show()




