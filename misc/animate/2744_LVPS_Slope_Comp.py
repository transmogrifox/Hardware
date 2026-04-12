import numpy as np
import matplotlib.pyplot as plt

k = 1000.0
kHz=1000.0
uH=1.0e-6
m = 1e-3
mΩ = m
mV = m
uA = 1.0e-6

usezoh = True

Fs = 130.0*kHz
gpk = 2.0
nps = 10.0/7.0
lm = 18.0*uH
vmin=8.0
vmax = 60.0
vo = 12.75+0.5
fsw = Fs
Ts = 1.0/Fs
Tus = np.array(1e6*Ts)
kmd = 0.75
md = (nps*vo)/lm

rcs=6.0*mΩ
vcs=98.0*mV
iCOMP = 50.0*uA
kCOMP = 0.24
dstart = 0.37
dend = 0.8
Rext = 24.9
Rint = kCOMP*vcs/iCOMP
Req = Rint + Rext
kCOMPeq = Req*iCOMP/vcs
gcs=rcs #V/A
mdx = vo*nps/lm
mcmpx = kmd*mdx
mcmpr = kCOMPeq*vcs/(Ts*rcs*(dend-dstart))
kmdr = mcmpr/md

print(f"Rint = {Rint:.1f}")
print(f"Req = {Req:.1f}")
print(f"kCOMPeq = {kCOMPeq:.3f}")


print(f"Down-slope, reflected to primary: {mdx/1000.0:.1f} kA/s")
print(f"Slope compensation, 75% down-slope:  {0.75*mdx/1000.0:.1f} kA/s")
print(f"Slope compensation, circuit implementation:  {mcmpr/k:.1f} kA/s")
print(f"kmd = {mcmpr/md:0.3f} (as implemented)")

def get_freqz(Fmax=260.0*kHz, Fmin=10.0, ptsPerDec=100.0, Fsw=67.0*kHz,Vin=30.0,Vout=15.0,Vbr=1.8,Vd=0.5,Lm=200.0*uH,Nps=4.0, kmd=0.75,ZOH=True,dstart = 0.37):

    mcg = (Vin - Vbr)/Lm
    mdg = (Vout + Vd)*Nps/Lm
    D = mdg/(mcg+mdg)
    mcomp = 0.0
    if D>dstart:
        mcomp = kmd*mdg
    
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

Fn, Hmag, Hphase, mcmp = get_freqz(Fmax=Fs, Fmin=10.0, ptsPerDec=100.0,Fsw=Fs,Vin=8.0,Vout=12.75,Vbr=0.5,Vd=0.5,Lm=lm,Nps=nps, kmd=kmdr, ZOH=usezoh)

figH = plt.figure(figsize=(14, 10))

plt.subplot(211)

plt.semilogx(Fn, Hmag, label="Vin = 30V")
plt.title("Peak Current Mode Controller Frequency Response\nSlope Compensation, $m_{cmp}$ =" + f" {mcmpr/1000.0:.0f} kA/s" + ", $k_{md}$ =" + f" {kmdr*100.0:.0f} % \n\nMagnitude")
plt.xlabel("Frequency (Hz)\n")
plt.ylabel("Magnitude (dB)")
plt.grid()
plt.legend(loc="upper left", prop={'size': 10})
plt.xlim(10.0, 130.0*kHz)
plt.ylim(-6.0, 8.0)

plt.tight_layout()

plt.subplot(212)

plt.semilogx(Fn, Hphase, label="Vin = 30V")
plt.title("Phase")
plt.xlabel("Frequency (Hz)\n")
plt.ylabel("Phase (°)")
plt.grid()
plt.legend(loc="lower left", prop={'size': 10})
plt.xlim(10.0, 130.0*kHz)
plt.ylim(-180.0, 30.0)
plt.tight_layout()

for vx in [10.8,12.0,24.0,36.0,48.0,60.0]:
    Fn, Hmag, Hphase, mcmp = get_freqz(Fmax=Fs, Fmin=10.0, ptsPerDec=100.0,Fsw=Fs,Vin=vx,Vout=12.75,Vbr=0.5,Vd=0.5,Lm=lm,Nps=nps, kmd=kmdr, ZOH=usezoh)
    plt.subplot(211)
    plt.semilogx(Fn, Hmag, label=f"Vin = {vx:.1f}")
    plt.legend(loc="upper left", prop={'size': 10})
    plt.subplot(212)
    plt.semilogx(Fn, Hphase, label=f"Vin = {vx:.1f}")
    plt.legend(loc="lower left", prop={'size': 10})

plt.show()

quit()




        
        
        
        
