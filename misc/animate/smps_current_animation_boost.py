import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib.animation import FFMpegWriter

vLength = 1200

kHz=1000.0
uH=1.0e-6

# Fixing random state for reproducibility
np.random.seed(19680801)

Fs = 100*kHz
Ts = 1.0/Fs
pctSW = 0.25 # percent of switching cycle allocated to rise & fall time
tTrans = pctSW*Ts/100.0 # time to transition between states

def get_freqz(Fmax=100.0*kHz, Fmin=10.0, ptsPerDec=100.0):
    fstart = np.log10(Fmin)
    fstop = np.log10(Fmax)
    ndec = fstop/fstart
    num = int(ndec*ptsPerDec + 0.5)
    Frq = np.logspace(start=fstart, stop=fstop, num=num, endpoint=True, base=10.0)
    z1 = np.exp(-1j*2.0*np.pi*Frq/Fmax)
    
    return Frq, z1
   
def get_cycle(Fsw=100.0*kHz, offset=0.0, maxDuty=0.95, iv1=1.0, ic0=8.0, Vin= 48.0, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, mcmp=0.0, ccmdcm=True):
    global tTrans
    Tsw = 1.0/Fsw
    maxD = maxDuty

    mc = Vin/Lm
    md = (Nps**2.0)*Vout/Lm
    iv1n = iv1
    iv0 = 0.0
    tcg = 0.0
    tdg = 0.0
    tdgEnd = 0.0

    if ccmdcm:
        iv0 = 0.0
        if (iv1n < 0.0):
            iv1n = 0.0
        tcg = (ic0 - iv1n)/(mcmp + mc)
        if tcg > maxD*Tsw:
            tcg = maxD*Tsw
        ipk = iv1n + mc*tcg
        tdg = ipk/md
        tdgEnd = tcg + tdg - tTrans
        if tdgEnd > (Tsw - tTrans):
            tdg = Tsw - tcg - tTrans
            iv0 = ipk - tdg*md
            if iv0 < 0.0:
                print(f"Error! iv0 = {iv0}, can't be <0.0 during DCM.")
            tdgEnd = Tsw - tTrans
    else:
        tcg = (ic0 - iv1)/(mcmp + mc)
        if tcg > maxD*Tsw:
            tcg = maxD*Tsw
        tdg = Tsw - tcg
        ipk = iv1 + tcg*mc
        iv0 = ipk - tdg*md
        tdgEnd = Tsw - tTrans
        
        
    
    tns = np.array([offset, offset+tTrans, offset+tcg, offset+tcg + tTrans, offset+tdgEnd, offset+Tsw])
    tn = tns*1.0e6
    icg = np.array([0.0, iv1n, ipk, 0.0, 0.0, 0.0])
    cs = np.array([0.0, iv1n, ipk+tcg*mcmp, 0.0, 0.0, 0.0])
    idg = np.array([0.0, 0.0, 0.0, ipk, iv0, 0.0])
    
    Frq, z1 = get_freqz(Fmax=100.0*kHz, Fmin=10.0, ptsPerDec=100.0)
    hv = Frq/Frq
    if iv0 > 0:
        ap = (mc + md)/(mc + mcmp)
        hv = (Fsw*(1.0-z1)/(1j*2*np.pi*Frq))*ap*z1/(1.0 - (1.0-ap)*z1)
    else:
        hv = ((1.0-np.exp(2j*np.pi*Frq*tdgEnd))/(1j*2*np.pi*Frq*tdgEnd))
    return tn,icg,idg,cs,iv0,(tcg/Tsw), Frq, 20.0*np.log10(abs(hv))

#metadata = dict(title='Slope Compensation demo')
#writer = FFMpegWriter(fps=20, metadata=metadata)
writer = FFMpegWriter(fps=20)

fig = plt.figure()
plt.subplot(211)
l4, = plt.plot([], [], linestyle='dotted', label="Peak current trip threshold")
l3, = plt.plot([], [], linestyle='--', label="Sensed current with slope compensation")
l2, = plt.plot([], [], linestyle='--', label = "Discharging cycle inductor current")
l1, = plt.plot([], [], label = "Charging cyle inductor current")

plt.title("Inductor current waveform - DCM")
plt.xlabel("Time (μs)")
plt.ylabel("Current (A)")
plt.xlim(-15, 25)
plt.ylim(-0.5, 4.5)
plt.yticks([0, 1, 2, 3, 4])
plt.grid()
plt.legend(loc="upper right", prop={'size': 6})
plt.subplot(212)
plt.title("Peak current controller frequency resopnse")
l0, = plt.semilogx([], [], label = "Peak current contoller transfer function")
plt.grid()
plt.xlabel("Frequency (kHz)\n--")
plt.ylabel("Magnitude (dB)")
plt.xlim(0.01, 100.0)
plt.ylim(-6.0, 24.0)

x0, y0 = 0, 0
n = 0
m = 0

ivn = 1.0
Vin = 48.0
Vout = 85.0 - Vin
Nps = 1.0
lm = 220.0*uH

mcmp = 60000.0
d = 0.0
dn = d
ad = 0.99
bd = 1.0 - ad
ic0i = 24.0/(Vin + Vout)
ic0 = ic0i

noiseLevel = 0.01
inoiseLevel = 0.02
nomcmp = True

hvv = []

with writer.saving(fig, "slope_comp_demo_boost.mp4", vLength/13):
    for i in range(vLength):
        plt.subplot(211)
        n = n+1
        if n < 13:
            continue
        tn = []
        icg = []
        idg = []
        cs = []
        
        Vin *= 0.998
        Vout = 85.0 - Vin
        ic0i = 24.0/(Vin)
        ic0 = ic0i
        
        if Vin <= 30.0:
            if Vin <= 18.0:
                Vin = 18.0
            if ic0 <= 4.25:
                mcmp += 500.0
                if mcmp > 250000.0:
                    mcmp = 250000.0
                if n >= 30:
                    nomcmp = False
                    if mcmp < 230e3:
                        ptitle = f"Vin = {Vin:.1f} VDC - CCM (Unstable) - Slope compensation {mcmp/1000.0:.1f} kA/s"
                    else:
                        ptitle = f"Vin = {Vin:.1f} VDC - CCM (Stabilizing) - Slope compensation {mcmp/1000.0:.1f} kA/s"
                    plt.title(ptitle)
                    plt.xlabel("Time (μs)")
                    plt.ylabel("Current (A)")
                    n = 0
                n += 1
            #d = Vout*Nps/(Vout*Nps + Vin)
            disns = mcmp*dn*(Ts+tTrans)
            ic0 = ic0i + disns
        vnoise = Vin*noiseLevel * np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        
        
        tnx, icgx, idgx, csx, ivn, d, Fn, hz = get_cycle(Fsw=Fs, offset=-2.0*Ts, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=Vout, Lm=lm, Nps=Nps, mcmp=mcmp, ccmdcm=True)
        dn = ad*dn + bd*d
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)
        vnoise = noiseLevel * np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        tnx, icgx, idgx, csx, ivn, d, Fn, hz = get_cycle(Fsw=Fs, offset=-Ts, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=Vout, Lm=lm, Nps=Nps, mcmp=mcmp, ccmdcm=True)
        dn = ad*dn + bd*d
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)
        vnoise = noiseLevel* np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        tnx, icgx, idgx, csx, ivn, d, Fn, hz = get_cycle(Fsw=Fs, offset=0.0, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=Vout, Lm=lm, Nps=Nps, mcmp=mcmp, ccmdcm=True)
        dn = ad*dn + bd*d
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)
        vnoise = noiseLevel * np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        tnx, icgx, idgx, csx, ivn, d, Fn, hz = get_cycle(Fsw=Fs, offset=Ts, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=Vout, Lm=lm, Nps=Nps, mcmp=mcmp, ccmdcm=True)
        dn = ad*dn + bd*d
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)
        vnoise = noiseLevel * np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        tnx, icgx, idgx, csx, ivn, d, Fn, hz = get_cycle(Fsw=Fs, offset=2.0*Ts, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=Vout, Lm=lm, Nps=Nps, mcmp=mcmp, ccmdcm=True)
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)

        if (m >= 30) and nomcmp:          
            if (ivn > 0.025):
                ptitle = f"Vin = {Vin:.1f} VDC - CCM - Slope compensation {mcmp/1000.0:.1f} kA/s"
            else:
                ptitle = f"Vin = {Vin:.1f} VDC - DCM - Slope compensation {mcmp/1000.0:.1f} kA/s"  
            plt.title(ptitle)
            plt.xlabel("Time (μs)")
            plt.ylabel("Current (A)")
            m = 0
        m+=1

        l1.set_data(tn,icg)
        l2.set_data(tn,idg)
        l3.set_data(tn,cs)
        l4.set_data([np.min(tn), np.max(tn)],[ic0, ic0])
        
        plt.subplot(212)
        if (Vin>20.5) or (mcmp > 45000.0):
            hvv = hz
        l0.set_data(Fn/1000.0,hvv)
        
        
        plt.tight_layout()
        
        writer.grab_frame()
        
        
        
        
