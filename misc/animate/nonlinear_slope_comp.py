import numpy as np
import matplotlib.pyplot as plt

kHz=1000.0
uH=1.0e-6

Fs = 100*kHz
Ts = 1.0/Fs
Tus = np.array(1e6*Ts)

def get_freqz(Fmax=100.0*kHz, Fmin=10.0, ptsPerDec=100.0):
    fstart = np.log10(Fmin)
    fstop = np.log10(Fmax)
    ndec = fstop/fstart
    num = int(ndec*ptsPerDec + 0.5)
    Frq = np.logspace(start=fstart, stop=fstop, num=num, endpoint=True, base=10.0)
    z1 = np.exp(-1j*2.0*np.pi*Frq/Fmax)
    
    return Frq, z1
   
def get_mcmpD(Fsw=100.0*kHz, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, duty=0.5, gpeak=2.0):
    
    g = gpeak
    md = (Nps**2.0)*Vout/Lm
    dp = 1.0 - duty
    mcmp_const = 840000.0
    # Algebraic steps to combine to a single expression
    #mcmp = md*(1+g)/(2*g*duty) - md*dp/duty
    #mcmp = md*(1+g)/(2*g*duty) - md*(1-duty)/duty
    #mcmp = (md*(1+g) - md*2*g*(1-duty))/(2*g*duty)
    #mcmp = md*((1+g) - 2*g*(1-duty))/(2*g*duty)
    #mcmp = md*(1+g - 2*g + 2*g*duty)/(2*g*duty)
    mcmp = md*(1+ g*(2*duty - 1))/(2*g*duty)
    mcmp = md*(1/(2*duty))*(1-g)/g + md
    mcmp = (1/duty)*md*(1-g)/(2*g) + md
    mcmp_ = 0.0
    Hmag = 1.0/(2.0*(- 1.0)*duty + 1.0) 
    Hx = 1.0/(2.0*(- 1.0)*duty + 1.0) 
    Hy = 1.0/(2.0*(mcmp_const/md - 1.0)*duty + 1.0) 
    if duty >= (g-1)/(2*g):
        mcmp_ = (md/Fsw)*(np.log(duty)*(1-g)/(2*g) + duty + (1-g)/(2*g) + np.log((g-1)/(2*g))*(g-1)/(2*g) )
        #Hmag = 20.0*np.log10( 1.0/(2.0*(mcmp_const/md - 1.0)*duty + 1.0) )
        Hmag = 1.0/(2.0*(mcmp_const/md - 1.0)*duty + 1.0) 
        Hx = 1.0/(2.0*(mcmp/md - 1.0)*duty + 1.0) 
    
    return duty, mcmp, mcmp_, Hmag, Hx, Hy

def get_mcmp(Fsw=100.0*kHz, Vin= 48.0, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, gpeak=2.0):
    mc = Vin/Lm
    md = (Nps**2.0)*Vout/Lm
    
    mcmp = (1.0 + gpeak)*(mc+md)/(2.0*gpeak) - mc
    D = md/(mc + md)

    return D, mcmp

def dBV(v):
    return 20.0*np.log10(v)

Vs = []
D = []
Dx = []
mcmp = []
mcmpx = []
acmp = []
acmp_ = []
Hm = []
Hx = []
Hy = []
gpk = 2.0
nps = 10.0/7.3
lm = 18.0*uH
vo = 12.5
fsw = 100.0*kHz
ac = 0.0
dstart = 0.0

Vs.append(0.0)
D.append(0.0)
Dx.append(0.0)
mcmp.append(0.0)
mcmpx.append(0.0)
acmp.append(0.0)
acmp_.append(0.0)
Hm.append(1.0)
Hx.append(1.0)
Hy.append(1.0)

for Vi in np.arange(500.0,9.0,-1.0):
    d0, m0 = get_mcmp(Fsw=fsw, Vin=Vi+1.0, Vout=vo, Lm=lm, Nps=nps, gpeak=gpk)
    da, ma = get_mcmp(Fsw=fsw, Vin=Vi, Vout=vo, Lm=lm, Nps=nps, gpeak=gpk)
    db, mb, mb_, hmag, hx, hy = get_mcmpD(Fsw=fsw, Vout=vo, Lm=lm, Nps=nps, duty=da, gpeak=gpk)
    
    if(ma > 0.0):
        ac += (da-d0)*ma/fsw
    else:
        ma = 0.0
        mb = 0.0
        dstart = da
    
    Vs.append(Vi)
    D.append(da)
    Dx.append(db)
    mcmp.append(ma)
    mcmpx.append(mb*1.0e-3)
    acmp.append(ac)
    acmp_.append(mb_)
    Hm.append(hmag)
    Hx.append(hx)
    Hy.append(hy)
    
    
fig = plt.figure(figsize=(14, 10))
plt.subplot(311)

#plt.plot(D, mcmp, label="Required slope comp")
plt.plot(100.0*np.array(Dx), mcmpx, label="Slope comp to maintain 6dB peaking")
plt.title("Slope compensation needed for constant peaking gain \n as a function of duty cycle")
plt.xlabel("Duty (%)\n")
plt.ylabel("Slope Compensation (kA/s)")
plt.grid()
plt.legend(loc="upper right", prop={'size': 10})
plt.xlim(0.0, 100.0)
plt.xticks(np.linspace(0.0,100.0,21, endpoint=True))
#plt.ylim(-2.0, 16.0)

maxD = np.max(D)
maxm = np.max(mcmp)
imax = maxD*maxm/fsw
istart = -dstart*maxm/fsw
iend = imax + istart



plt.subplot(312)
D.append(maxD+0.001)
D.append(1.0)
acmp_.append(0.0)
acmp_.append(0.0)
plt.plot(D*Tus, acmp_, label="Nonlinear slope comp")
plt.plot([0,maxD*Tus,maxD*(0.001 + Tus), Tus], [0, imax,0,0], label="Linear slope comp")
plt.plot([0,dstart*Tus, maxD*Tus,maxD*(0.001 + Tus), Tus], [0,0, iend,0,0], dashes=[3,3], linewidth=3, label="Linear slope comp w/ offset, clipped")

plt.title("Slope compensation synthesized ramp waveforms")
plt.xlabel("Time (μs)\n")
plt.ylabel("Current (A)")
plt.grid()
plt.legend(loc="upper right", prop={'size': 10})
plt.xlim(0.0, 10.0)
plt.xticks(np.linspace(0.0,10.0,21, endpoint=True))
plt.subplot(313)

plt.plot(100.0*np.array(Dx), dBV(Hx), label="Nonlinear slope comp")
plt.plot(100.0*np.array(Dx), dBV(Hy), label="Linear slope comp")
plt.plot(100.0*np.array(Dx), dBV(Hm), dashes=[3,3], linewidth=3 ,label="Linear slope comp, w/ offset, clipped")

plt.title("Peaking magnitude vs Duty Cycle")
plt.xlabel("Duty (%)")
plt.ylabel("Gain (dB)")
plt.grid()
plt.legend(loc="upper right", prop={'size': 10})
plt.xlim(0.0, 100.0)
plt.xticks(np.linspace(0.0,100.0,21, endpoint=True))
plt.tight_layout()

plt.show()



        
        
        
        
