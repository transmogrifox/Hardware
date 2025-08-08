import numpy as np
import matplotlib.pyplot as plt

#
# Engineering multipliers
#
p = 1e-12
n = 1e-9
u = 1e-6
m = 1e-3
k = 1e3
M = 1e6

#
# LT3837 Parameters
#
VsenseVc = 0.07 #dVsense/dVc
Vsense = 98.0*m #Volts, max current trip threshold
Isfst = 20.0*u  #Amps, SFST pin charging current

#
# Circuit parameters
#
Rsense = 6.0*m # Ohms, current sense resistor
Rpd = 1.0*k # SFST switched pull-down resistor
Csw = 100.0*u # Farads, SFST timing capacitor
Css = 100.0*p # Farads, SFST high frequency filter capacitor
Rss = 2.49*k  # Ohms, SFST filter resistor
Plimit = 45.0 # Watts (min line default limit)

#
# Valley current: small signal model
# Hz = Ivalley/Icontrol
#
def iv(Lm=385.0*u, Vin=8.0, Vout=12.0, Nps=2.0, Pload=45.0, Eff=0.75, Fsw=65.0*k, mcmp=250*k, Fstart=10.0, Fstop=130.0*k, PointsPerDecade=100 ):
    # Steady state operating point analysis
    wsw = 2.0*np.pi*Fsw
    pi2 = np.pi*np.pi
    Tsw = 1/Fsw
    Pin = Pload/Eff
    Icg = Pin/Vin
    D = Vout*Nps/(Vout*Nps + Vin)
    #LT3837 doesn't apply slope comp D<37%'
    if D<0.37:
        mcmp = 0.0
    Ia = Icg/D
    mc = Vin/Lm
    md = Nps*Vout/Lm
    Irip = D*Tsw*mc
    Ipk = Irip/2 + Ia
    Iv = Ipk - Irip
    print(f"D = {D*100.0:.1f} %\nIcg = {Icg:.1f} A\nIrip = {Irip:.1f} A\nIpk = {Ipk:.1f} A\nIv = {Iv:.1f} A\nmc = {mc*m:.1f} kA/s\nmd = {md*m:.1f} kA/s\nmcmp = {mcmp*m:.1f} kA/s")

    #Set up time axis variables
    Ndecs = np.floor(np.log10(Fstop/Fstart))
    Npts = int(Ndecs)*PointsPerDecade

    print(f"Ndecs = {Ndecs}, Npts = {Npts}")
    freqs = np.logspace(start=np.log10(Fstart), stop=np.log10(Fstop), num=Npts, endpoint=True, base=10.0)
    s = 2j*np.pi*freqs
    z1 = np.exp(-s*Tsw)

    #Small signal analysis, discrete time response
    #Control-to-valley current
    alpha = (mc + md) / (mc + mcmp)
    Hiv = alpha*z1/(1.0 - (1.0 - alpha)*z1)
    ZoH = (1.0 - z1)/(Tsw*s)
    Hz = ZoH*Hiv
    #Hz = ZoH

    #Continuous time approximation
    #Q = alpha/(2.0-alpha) #Approximate peaking Q to match amplitude of Hiv at peak, attenuate later with ZoH approx function
    Q = (2.0/np.pi)*alpha/(2.0-alpha) # Approximate Hiv*ZoH peaking response, adjust phase using all-pass delay
    w0 = np.pi*Fsw
    a0 = w0*w0
    a1 = w0/Q
    b2 = 1.0
    b1 = w0
    b0 = a0
    #Fit valley current modulator response
    Hvs = (b2*s*s - b1*s + b0)/(s*s + a1*s + a0) # Peaking all-pass approximation
    #Hvs = (b0)/(s*s + a1*s + a0) # Peaking low-pass approximtion

    #Approximate Zero-Order-Hold with first order filter
    wc = wsw*np.sqrt(1.0/(pi2 - 4.0))

    # Delay all-pass filter.  Right now numbers for phase match are guessed graphically
    # Might be better match if phase response of the whole cascaded system is worked out and set equal for wSW/2
    #wd = 2.0*wc # Used with Peaking all-pass, Q *not* adjusted by (2/pi)
    wd = (np.pi)*wc # Used with Peaking all-pass, Q adjusted by (2/pi)
    # ZoHs = (wc/(s+wc)) # Used with Peaking all-pass, Q *not* adjusted by (2/pi)
    Zdly = (wd - s)/(s+wd)

    #Hs = Hvs*ZoHs*Zdly # Used with Peaking all-pass, Q *not* adjusted by (2/pi)
    Hs = Hvs*Zdly*Zdly # Used with Peaking all-pass, Q adjusted by (2/pi)

    #Control-to-Peak current transfer function
    Hpkz = Hz*mcmp/(mc + mcmp) + mc/(mc+mcmp)
    #Hpks = (Hvs*ZoHs*mcmp/(mc + mcmp) + mc/(mc+mcmp))*Zdly # Used when Hs calculated using Q *not* adjusted by (2/pi)
    Hpks = (Hs*mcmp/(mc + mcmp) + mc/(mc+mcmp)) # Used with Hs calculated using Q adjusted by (2/pi). This approximation appears it will work better in a Spice model

    #return freqs, Hiv, Hvs   #Control-to-valley current transfer function without sampling effect (ZOH)
    return freqs, Hz, Hs   #Control-to-valley current transfer function
    return freqs, Hpkz, Hpks  #Control-to-peak current transfer function

#
# SFST pull-down current as a function of Ipk
#

def Gpd(Rpd=1.0*k, Csw=100.0*n, Isfst=20.0*u, Lm=35.0*u, Rsns=6.0*m, Vin=8.0, Vout=12.0, Nps=2.0, Ipk=8.3, gVc=0.07, mcmp=550.0*k, Eff=0.75, Fsw=65.0*k):
    tau = Rpd*Csw
    md = Vout*Nps/Lm
    mc = Vin/Lm
    Dpt = md/(mc+md)
    Iv = Ipk - Dpt*mc/Fsw
    Ic = Iv + Dpt*(mc+mcmp)/Fsw
    Vsfst = 1.0 + Ic*Rsns/gVc #Steady state SFST voltage

    #Ipd = (Vsfst - Isfst*Rpd)/Rpd
    #D*Ipd = Vsfst/Rpd - Isfst
    #D = (Vsfst/Rpd - Isfst)/Ipd
    #dT = D/Fsw
    Ipd = Vsfst/Rpd - Isfst
    D = (Vsfst-Ipd*Rpd)/Vsfst
    dT = D/Fsw
    dI = dT*mc

    #Gpd = Ipd/Ipk, small signal gain
    Gpd = -(Vsfst)/(dI)

    print("Steady state operating point parameters:")
    print(f"tau = {tau*M:.1f} μs")
    print(f"Vsfst = {Vsfst:.4f} V")
    print(f"D, tPulse = {D*100.0:.1f} %, {dT/n:.1f} ns")

    print("Small signal gain, Gpd = Vsfst/Ipk")
    print(f"Gpd = {Gpd:.1f} V/A ({20.0*np.log10(np.abs(Gpd)):.2f} dB)")

    return Gpd

#
# Ipd to Ic transfer function: small signal model
# Hpd = Icontrol/Vc
#
def Gic(Csw=100.0*n, Css=100.0*p, Rss=2.49*k, Rsns=6.0*m, gVc=0.07, Fsw=65.0*k, Fstart=10.0, Fstop=130.0*k, PointsPerDecade=100 ):
    #Set up time axis variables
    Ndecs = np.floor(np.log10(Fstop/Fstart))
    Npts = int(Ndecs)*PointsPerDecade

    #print(f"Ndecs = {Ndecs}, Npts = {Npts}")
    freqs = np.logspace(start=np.log10(Fstart), stop=np.log10(Fstop), num=Npts, endpoint=True, base=10.0)
    s = 2j*np.pi*freqs

    g0 = 1.0/(Rss*Csw*Css)
    g1 = gVc/Rsns #Gain from VSFST->Vc->Icontrol
    p0 = (Csw + Css)/(Rss * Css * Csw)
    p1 = 2*np.pi*13

    Gic = g1*p0*p1/((s+p1)*(s+p0))

    return freqs,Gic


def lt3837_slope_comp(Fsw=65.0*k,Vsns=98.0*m,Rcs=6.0*m):
    # Estimate internal slope compensation internal to LT3837.
    # LT applications support gave the following information
    # about the slope compensation function:
    #     0% starting at 34% duty cycle,
    #     Ramps to 24% Vsense max at 80% duty cycle
    #     Vsense max = "Vsns" = [88 ... 110] mV, typ = 98 mV
    #     imax = Vsns/Rcs
    # Amount of slope compensation is "mcmp" (A/s)
    # In this case, mcmp = 24%*imax/Tramp
    # Tramp = Don/Fsw = (80%-30%)/Fsw
    # mcmp = 24%*imax*Fsw/(80% - 34%)  = imax*Fsw*24/46
    # Therefore a typical slope comp with 100kHz Fsw be
    #    Fsw = 100k
    #    imax = 98mV/4.84m-ohm = 20.25 A
    #    mcmp = 20.25A*100kHz*24/(46) = 1.057 A/us
    #
    imax = Vsns/Rcs
    mcmp = imax*Fsw*24.0/46.0
    return mcmp

def plot_response(f, Hz, Hs):
    fp = np.asarray(f)
    Hz_dB = np.asarray(20.0*np.log10(np.abs(Hz)))
    Hz_deg = np.asarray(180.0*np.unwrap(np.angle(Hz))/np.pi)

    Hs_dB = np.asarray(20.0*np.log10(np.abs(Hs)))
    Hs_deg = np.asarray(180.0*np.unwrap(np.angle(Hs))/np.pi)

    plt.figure(figsize=(12, 8))
    #fig, ax = plt.subplots(nrows=2,ncols=1)
    plt.subplots_adjust(hspace=0.35, wspace=0)
    plt.subplot(2, 1, 1)
    plt.semilogx(f, Hz_dB,"r")
    plt.semilogx(f, Hs_dB,"g")
    plt.title('Peak Current Controller Gain Response\n\nMagnitude')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude (dB)')
    #plt.legend(loc="upper right")
    plt.grid()
    plt.ylim([-40.0,50.0])

    plt.subplot(2, 1, 2)
    plt.semilogx(f, Hz_deg,"b")
    plt.semilogx(f, Hs_deg,"g")
    plt.title('Phase')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Phase (\xb0)')
    #plt.legend(loc="upper right")
    plt.grid()
    plt.savefig('modulator.png')
    plt.show()



##
## Test Program
##
mcmp0 = lt3837_slope_comp(Fsw=65.0*k,Vsns=98.0*m,Rcs=6*m)
#print(f"Slope Compensation = {mcmp0*m:.1f} kA/s")

gpd = Gpd(Rpd=1.0*k, Csw=100.0*n, Isfst=20.0*u, Lm=35.0*u, Rsns=6.0*m, Vin=8.0, Vout=12.0, Nps=2.0, Ipk=10.3, gVc=0.07, Eff=0.95, Fsw=65.0*k)

f,Hgic = Gic(Csw=100.0*n, Css=100.0*p, Rss=2.49*k, Rsns=6.0*m, gVc=0.07, Fsw=65.0*k, Fstart=10.0, Fstop=130.0*k, PointsPerDecade=1000 )

f,Hz, Hs = iv(Lm=35.0*u, Vin=8.0, Vout=8.0, Nps=2.0, Pload=47.0, Eff=0.95, Fsw=65.0*k, mcmp=mcmp0, Fstart=10.0, Fstop=130.0*k, PointsPerDecade=1000 )


plot_response(f, gpd*Hgic*Hz, gpd*Hgic)
