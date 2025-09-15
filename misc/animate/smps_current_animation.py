import numpy as np

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from matplotlib.animation import FFMpegWriter

vLength = 1000

kHz=1000.0
uH=1.0e-6

# Fixing random state for reproducibility
np.random.seed(19680801)

Fs = 100*kHz
Ts = 1.0/Fs

def get_cycle(Fsw=100.0*kHz, offset=0.0, maxDuty=0.95, iv1=1.0, ic0=8.0, Vin= 48.0, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, mcmp=0.0, ccmdcm=True):
    Tsw = 1.0/Fsw
    maxD = maxDuty
    pctSW = 0.25 # percent of switching cycle allocated to rise & fall time
    tTrans = pctSW*Tsw/100.0 # time to transition between states
     
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
    
    return tn, icg, idg,cs, iv0

metadata = dict(title='Slope Compensation demo')
writer = FFMpegWriter(fps=30, metadata=metadata)

fig = plt.figure()
l4, = plt.plot([], [], linestyle='dotted')
l3, = plt.plot([], [], linestyle='--')
l2, = plt.plot([], [], linestyle='--')
l1, = plt.plot([], [])

plt.xlim(-15, 25)
plt.ylim(-2.0, 12.0)
plt.xlabel("Time (μs)")
plt.ylabel("Current (A)")
plt.title("Inductor current waveform - DCM")
plt.grid()

x0, y0 = 0, 0
n = 0
m = 0

ivn = 1.0
Vin = 60.0
Vout = 12.5
Nps = 10.0/7.3

mcmp = 0.0
d = 0.0
ic0i = 8.0
ic0 = ic0i

noiseLevel = 0.4
inoiseLevel = 0.05
nomcmp = True

with writer.saving(fig, "writer_test.mp4", vLength):
    for i in range(vLength):
        tn = []
        icg = []
        idg = []
        cs = []
        

        Vin -= 0.1
        if Vin <= 16.0:
            Vin = 16.0
            if ic0 < 10.0:
                mcmp += 500.0
                disns = mcmp*d*Ts
                ic0 = ic0i + disns
                if n >= 30:
                    nomcmp = False
                    if mcmp < 200e3:
                        ptitle = f"Vin = {Vin:.1f} VDC - CCM (Unstable) - Slope compensation {mcmp/1000.0:.1f} kA/s"
                    else:
                        ptitle = f"Vin = {Vin:.1f} VDC - CCM (Stabilizing) - Slope compensation {mcmp/1000.0:.1f} kA/s"
                    plt.title(ptitle)
                    n = 0
                n += 1
        vnoise = noiseLevel * np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        d = Vout*Nps/(Vout*Nps + Vin)
        
        tnx, icgx, idgx, csx, ivn = get_cycle(Fsw=Fs, offset=-2.0*Ts, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, mcmp=mcmp, ccmdcm=True)
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)
        vnoise = noiseLevel * np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        tnx, icgx, idgx, csx, ivn = get_cycle(Fsw=Fs, offset=-Ts, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, mcmp=mcmp, ccmdcm=True)
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)
        vnoise = noiseLevel* np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        tnx, icgx, idgx, csx, ivn = get_cycle(Fsw=Fs, offset=0.0, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, mcmp=mcmp, ccmdcm=True)
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)
        vnoise = noiseLevel * np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        tnx, icgx, idgx, csx, ivn = get_cycle(Fsw=Fs, offset=Ts, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, mcmp=mcmp, ccmdcm=True)
        tn.append(tnx)
        icg.append(icgx)
        idg.append(idgx)
        cs.append(csx)
        vnoise = noiseLevel * np.random.randn()
        inoise = inoiseLevel * np.random.randn()
        tnx, icgx, idgx, csx, ivn = get_cycle(Fsw=Fs, offset=2.0*Ts, iv1=ivn, ic0=ic0+inoise, Vin= Vin+vnoise, Vout=12.5, Lm=18.0*uH, Nps=10.0/7.3, mcmp=mcmp, ccmdcm=True)
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
            m = 0
        m+=1

        
        
        
        l1.set_data(tn,icg)
        l2.set_data(tn,idg)
        l3.set_data(tn,cs)
        l4.set_data([np.min(tn), np.max(tn)],[ic0, ic0])
        writer.grab_frame()
        
        
        
        
