import numpy as np
import matplotlib.pyplot as plt

kHz=1000.0
uH=1.0e-6

Fs = 67.7*kHz
gpk = 2.0
nps = 32.0/8.0
lm = 200.0*uH
vmin=22.0
vmax = 375.0
vo = 15.0+1.0
fsw = Fs
Ts = 1.0/Fs
Tus = np.array(1e6*Ts)

rcs=27.0
ncs=100.0
gcs=rcs/ncs #V/A
mdx = vo*nps/lm
mcmpx = 0.75*mdx
mvcs = gcs*mcmpx
cramp = 10.0e-9 #Ramp synthesizer capacitance
vramp = 15.0 #Ramp synthesizer 'on' state voltage
dVramp = mvcs*Ts
rramp = (vramp-dVramp)/(mvcs*cramp)
print(f"Down-slope, reflected to primary: {mdx/1000.0:.1f} kA/s")
print(f"Slope compensation, 75% down-slope:  {0.75*mdx/1000.0:.1f} kA/s")
print(f"Current sense voltage ramp: {mvcs/1000.0:.1f} kV/s")
print(f"Ramp synth R&C: {cramp*1e9:.2f} nF & {rramp/1000:.1f} kOhm")
print(f"Ramp capacitor voltage change: {dVramp:.2f} V")

def get_freqz(Fmax=260.0*kHz, Fmin=10.0, ptsPerDec=100.0, Fsw=67.0*kHz,Vin=30.0,Vout=15.0,Vbr=1.8,Vd=0.5,Lm=200.0*uH,Nps=4.0, kCOMP=0.75,ZOH=True):

    mcg = (Vin - Vbr)/Lm
    mdg = (Vout + Vd)*Nps/Lm
    mcomp = kCOMP*mdg
    
    alpha = (mcomp - mdg)/(mcomp + mcg)
    beta = 1.0 - alpha
    
    fstart = np.log10(Fmin)
    fstop = np.log10(Fmax)
    ndec = fstop/fstart
    num = int(ndec*ptsPerDec + 0.5)
    Frq = np.logspace(start=fstart, stop=fstop, num=num, endpoint=True, base=10.0)
    z1 = np.exp(-1j*2.0*np.pi*Frq/Fsw)
    s=1j*2.0*np.pi*Frq
    Tsw = 1.0/Fsw
    
    Hzoh = Fsw*(1.0-np.exp(-s*Tsw))/s
    
    Hz = beta*z1/(1.0-alpha*z1)
    if ZOH:
        Hz = Hz*Hzoh
    
    HzMAG = dBV(np.abs(Hz))
    HzPH = np.unwrap(np.angle(Hz,deg=True), period=360.0)
    
    return Frq, HzMAG, HzPH, mcomp
   
def get_mcmp(Fsw=100.0*kHz, Vin= 48.0, Vout=12.5, Lm=18.0*uH, Nps=4.0, gpeak=2.0):
    mc = Vin/Lm
    md = Nps*Vout/Lm
    
    mcmp = (1.0 + gpeak)*(mc+md)/(2.0*gpeak) - mc
    D = md/(mc + md)
    #D = Vout/(Vout+Vin/Nps)

    return D, mcmp

def dBV(v):
    return 20.0*np.log10(v)

##
## Start main prog
##


usezoh = False
Fn, Hmag, Hphase, mcmp = get_freqz(Fmax=67.0*kHz, Fmin=10.0, ptsPerDec=100.0,Fsw=67.0*kHz,Vin=30.0,Vout=15.0,Vbr=1.8,Vd=0.5,Lm=200.0*uH,Nps=4.0, kCOMP=0.75, ZOH=usezoh)

figH = plt.figure(figsize=(14, 10))

plt.subplot(211)

plt.semilogx(Fn, Hmag, label="Vin = 30V")
plt.title("Peak Current Mode Controller Frequency Response\nSlope Compensation, $m_{cmp}$ =" + f" {mcmp/1000.0:.0f} kA/s \n\nMagnitude")
plt.xlabel("Frequency (Hz)\n")
plt.ylabel("Magnitude (dB)")
plt.grid()
plt.legend(loc="upper left", prop={'size': 10})
plt.ylim(-1.0, 5.0)

plt.tight_layout()

plt.subplot(212)

plt.semilogx(Fn, Hphase, label="Vin = 30V")
plt.title("Phase")
plt.xlabel("Frequency (Hz)\n")
plt.ylabel("Phase (°)")
plt.grid()
plt.legend(loc="lower left", prop={'size': 10})
plt.ylim(-180.0, 30.0)
plt.tight_layout()

for vx in [48.0,80.0,170.0,375.0]:
    Fn, Hmag, Hphase, mcmp = get_freqz(Fmax=67.0*kHz, Fmin=10.0, ptsPerDec=100.0,Fsw=67.0*kHz,Vin=vx,Vout=15.0,Vbr=1.8,Vd=0.5,Lm=200.0*uH,Nps=4.0, kCOMP=0.75, ZOH=usezoh)
    plt.subplot(211)
    plt.semilogx(Fn, Hmag, label=f"Vin = {vx:.1f}")
    plt.legend(loc="upper left", prop={'size': 10})
    plt.subplot(212)
    plt.semilogx(Fn, Hphase, label=f"Vin = {vx:.1f}")
    plt.legend(loc="lower left", prop={'size': 10})

plt.show()

quit()




        
        
        
        
