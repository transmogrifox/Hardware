import numpy as np
import matplotlib.pyplot as plt

kHz=1000.0
uH=1.0e-6

Fs = 67.7*kHz
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
   
def get_mcmpD(Fsw=100.0*kHz, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, duty=0.5, gpeak=2.0, mdr=0.5):
    
    g = gpeak
    md = (Nps**2.0)*Vout/Lm
    dp = 1.0 - duty
    mcmp_const = md*mdr
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
H0p5 = []
H0p75 = []
H1p0 = []
gpk = 2.0
nps = 32.0/8.0
lm = 200.0*uH
vo = 15.0+1.0
fsw = 67.7*kHz
ac = 0.0
dstart = 0.0

Vs.append(0.0)
D.append(0.0)
Dx.append(0.0)
mcmp.append(0.0)
mcmpx.append(0.0)
acmp.append(0.0)
acmp_.append(0.0)
Hm.append(0.0)
Hx.append(0.0)
H0p5.append(0.0)
H0p75.append(0.0)
H1p0.append(0.0)

for da in np.arange(0.1,1.0,0.005):
    db, mb, mb_, hmag, hx, hy = get_mcmpD(Fsw=fsw, Vout=vo, Lm=lm, Nps=nps, duty=da, gpeak=gpk, mdr=0.5)
    Dx.append(da)
    H0p5.append(dBV(hy))
for da in np.arange(0.1,1.0,0.005):
    db, mb, mb_, hmag, hx, hy = get_mcmpD(Fsw=fsw, Vout=vo, Lm=lm, Nps=nps, duty=da, gpeak=gpk, mdr=0.75)
    #Dx.append(da)
    H0p75.append(dBV(hy))  
for da in np.arange(0.1,1.0,0.005):
    db, mb, mb_, hmag, hx, hy = get_mcmpD(Fsw=fsw, Vout=vo, Lm=lm, Nps=nps, duty=da, gpeak=gpk, mdr=1.0)
    #Dx.append(da)
    H1p0.append(dBV(hy))
    
fig = plt.figure(figsize=(12, 5))

#plt.plot(D, mcmp, label="Required slope comp")
plt.plot(100.0*np.array(Dx), H0p5, label=r"$m_{cmp} = \frac{1}{2} m_d$")
plt.plot(100.0*np.array(Dx), H0p75, label=r"$m_{cmp} = \frac{3}{4} m_d$")
plt.plot(100.0*np.array(Dx), H1p0, label=r"$m_{cmp} = m_d$")

plt.title('Peaking magnitude at several recommended slope compensation values (function of duty cycle)')
plt.xlabel("Duty (%)\n")
plt.ylabel("Peaking Magnitude (dB)")
plt.grid()
plt.legend(loc="upper left", prop={'size': 10})
plt.xlim(0.0, 100.0)
plt.ylim(-0.5, 17.5)
plt.xticks(np.linspace(0.0,100.0,21, endpoint=True))
#plt.ylim(-2.0, 16.0)


plt.show()



        
        
        
        
