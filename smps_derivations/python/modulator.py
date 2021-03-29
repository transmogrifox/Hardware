import numpy as np
#import matplotlib as mpl
import matplotlib.pyplot as plt

#
# 1) Create a steadyState object to define the system
# 2) Pass the steadyState object into smallSignal for modulator small signal
#      AC response.

class modulatorSystem:
    def __init__(self, Vin, Vout, Vdiode, iload, Fsw, Ls, Lmag, mcmp, Nps, topology, rectifierMode ):
        self.Vin = Vin                      #Converter input voltage
        self.Vout = Vout                    #Converter output voltage
        self.Vdiode = Vdiode                #Drop across rectifier output
        self.iload = iload                  #Output load current
        self.Fsw = Fsw                      #Switching frequency
        self.Ls = Ls                        #Switched inductor in all topologies
        self.Lmag = Lmag                    #Magnetizing inductane in case of
                                            #  isolated forward
        self.mcmp = mcmp                    #Artificial ramp (slope compensation)
        self.Nps = Nps                      #Primary to secondary turns ratio
                                            #  (for isolated or coupled topologies)
        self.top = topology                 #Converter topology
        self.rectifierMode = rectifierMode  #Force CCM or diode operation


################################################################################
##                                                                            ##
##              Converter steady state operating conditions                   ##
##                                                                            ##
################################################################################

class steadyState:
    def __init__(self, sys ):
        self.Vin = sys.Vin
        self.Vout = sys.Vout
        self.Vdiode = sys.Vdiode
        self.iload = sys.iload
        self.Fsw = sys.Fsw
        self.Ls = sys.Ls
        self.Lmag = sys.Lmag
        self.mcmp = sys.mcmp
        self.Nps = sys.Nps
        self.top = sys.top
        self.rectifierMode = sys.rectifierMode

        ##
        ## Internal variables
        ##

        self.mode = "CCM"   #CCM, DCM or BCM
        #Inductor voltages
        self.vCG = 0.0      #Voltage across inductor during charging cycle
        self.vDG = 0.0      #Voltage across inductor during discharging cycle

        #Inductor currents
        self.ic = 0.0       #Peak current control set point
        self.ipk = 0.0      #Peak current
        self.iv = 0.0       #Inductor valley current
        self.iCG = 0.0      #Charging cycle average inductor current
        self.iDG = 0.0      #Discharging cycle average inductor current
        self.iRMS_in = 0.0  #RMS input current
        self.iRMS_out = 0.0 #RMS output current

        #Helpful variables
        self.Tsw = 0.0      #Switching period
        self.mc = 0.0       #Charging cycle inductor current slope
        self.md = 0.0       #Discharging cycle inductor current slope
        self.alpha = 0.0    #IIR coefficient
        
        #Output characteristics
        self.duty = 0.0     #Duty Cycle
        self.dcg = 0.0      #Discharge duty if operating in DCM
        self.idle = 0.0     #Idle time after discharge if operating in DCM
        self.iDG_bcm = 0.0  #Loading at specified input/output voltages 
                            #  for which the converter is operating in 
                            #  boundary conduction mode

        ##
        ## Initialize internal variables
        ##
        self.compute_sys_params()

    def update(self, sys ):
        self.Vin = sys.Vin
        self.Vout = sys.Vout
        self.Vdiode = sys.Vdiode
        self.iload = sys.iload
        self.Fsw = sys.Fsw
        self.Ls = sys.Ls
        self.Lmag = sys.Lmag
        self.mcmp = sys.mcmp
        self.Nps = sys.Nps
        self.top = sys.top
        self.rectifierMode = sys.rectifierMode
        self.compute_sys_params()


    def compute_ic(self):
        if self.mode == "CCM" :
            self.ic =   self.iDG*(self.vCG + self.vDG)/self.vCG \
                        - (self.Tsw/(2*self.Ls))*self.vCG*self.vDG/(self.vCG + self.vDG) \
                        + self.Tsw*self.md/self.alpha
        else:
            self.compute_ipk()
            self.ic = self.ipk*(self.mc + self.mcmp)/self.mc;

    def compute_ipk(self):
        if self.mode == "CCM" :
            self.ipk =   self.iDG*(self.vCG + self.vDG)/self.vCG \
                        + (self.Tsw/(2*self.Ls))*self.vCG*self.vDG/(self.vCG + self.vDG)
        else:
            self.ipk = np.sqrt(2*self.Tsw*self.vDG*self.iDG/self.Ls)

    def compute_iv(self):
        if self.mode == "CCM" :
            self.iv =   self.iDG*(self.vCG + self.vDG)/self.vCG \
                        - (self.Tsw/(2*self.Ls))*self.vCG*self.vDG/(self.vCG + self.vDG)
        else:
            self.iv = 0.0;

    def compute_alpha(self):
        self.alpha =      (self.mc + self.md) \
                        /(self.mc + self.mcmp)

    def compute_duty(self):
        if self.mode == "DCM" :
            self.compute_ipk()
            self.duty =  self.ipk/(self.Tsw*self.mc)
            self.dcg =  self.ipk/(self.Tsw*self.md)
            self.idle = 1.0 - (self.duty + self.dcg)
        else:
            self.duty =  self.vDG/(self.vCG + self.vDG)
            self.dcg =  1.0 - self.duty
            self.idle = 0.0

    def compute_rms(self):
        irmscg = 0.0
        irmsdg = 0.0
        if self.mode == "CCM" :
            irmscg = np.sqrt(self.duty)*np.sqrt(self.iv*self.iv \
                     + self.iv*(self.ipk - self.iv) \
                     + (self.ipk - self.iv)*(self.ipk - self.iv)/3.0)
            irmsdg = np.sqrt(self.dcg)*np.sqrt(self.iv*self.iv \
                     + self.iv*(self.ipk - self.iv) \
                     + (self.ipk - self.iv)*(self.ipk - self.iv)/3.0)
        else:
            irmscg = self.ipk/np.sqrt(3*self.Tsw*self.mc)
            irmsdg = self.ipk/np.sqrt(3*self.Tsw*self.md)

        #Initialize as if a buck-boost
        self.iRMS_in = irmscg
        self.iRMS_out = irmsdg

        if self.top == "BOOST":
            self.iRMS_in = irmscg
            self.iRMS_out = irmsdg
        if self.top == "BUCK":
            self.iRMS_in = irmscg
            self.iRMS_out = irmsdg + irmscg
        if self.top == "BUCKBOOST":
            self.iRMS_in = irmscg
            self.iRMS_out = irmsdg
        if self.top == "FORWARD": #Evaluated as buck with Vin reflected to secondary
            self.iRMS_in = irmscg/self.Nps
            self.iRMS_out = irmsdg + irmscg
        if self.top == "FLYBACK":
            self.iRMS_in = irmscg
            self.iRMS_out = irmsdg*self.Nps

    def compute_bcm(self):
        self.iDG_bcm = self.Nps*(self.Tsw/(2.0*self.Ls))*self.vDG*self.vDG*self.vCG/\
                       ((self.vCG + self.vDG)*(self.vCG + self.vDG))

    def compute_sys_params(self):

        ## Configure inductor voltages based upon topology ##

        #Initialize as buck-boost
        self.vCG = self.Vin
        self.vDG = self.Vout + self.Vdiode
        self.iDG = self.iload
        self.iCG = self.iDG*self.vDG/self.vCG

        #Then determine if it's something else
        if self.top == "BOOST":
            self.vCG = self.Vin
            self.vDG = self.Vout + self.Vdiode - self.Vin
            self.iDG = self.iload
            self.iCG = self.iDG*self.vDG/self.vCG
        if self.top == "BUCK":
            self.vCG = self.Vin - self.Vout
            self.vDG = self.Vout + self.Vdiode
            self.iDG = self.iload*self.vCG/(self.vCG + self.vDG)
            self.iCG = self.iDG*self.vDG/self.vCG
        if self.top == "BUCKBOOST":
            self.vCG = self.Vin
            self.vDG = self.Vout + self.Vdiode
            self.iDG = self.iload
            self.iCG = self.iDG*self.vDG/self.vCG
        if self.top == "FORWARD": #Evaluated as buck with Vin reflected to secondary
            self.vCG = self.Vin/self.Nps - (self.Vout + self.Vdiode)
            self.vDG = self.Vout + self.Vdiode
            self.iDG = self.iload*self.vCG/(self.vCG + self.vDG)
            self.iCG = self.iDG*self.vDG/self.vCG
        if self.top == "FLYBACK":
            self.vCG = self.Vin
            self.vDG = (self.Vout + self.Vdiode)*self.Nps
            self.iDG = self.iload/self.Nps
            self.iCG = self.iDG*self.vDG/self.vCG

        #Helpful variables
        self.Tsw = 1/self.Fsw           #Switching period
        self.mc = self.vCG/self.Ls      #Charging cycle inductor current slope
        self.md = self.vDG/self.Ls      #Discharging cycle inductor current slope
        self.compute_alpha()   #IIR coefficient

        #Test CCM or DCM
        self.compute_iv()

        #Evaluate mode based on valley current
        if self.iv == 0:
            self.mode = "BCM"
        if self.iv > 0:
            self.mode = "CCM"
        if self.iv < 0:
            self.mode = "DCM"
        if self.rectifierMode == "FCCM":
            self.mode = "CCM"

        #Re-compute according to mode
        self.compute_ic()
        self.compute_ipk()
        self.compute_iv()
        self.compute_duty()
        self.compute_rms()
        self.compute_bcm()


    def print_sys_params(self):
        #System inputs
        print("Topology =\t", self.top)
        print("Input Voltage = \t", self.Vin, "\tVolts")
        print("Output Voltage =\t", self.Vout, "\tVolts")
        print("Rectifier Drop =\t", self.Vdiode, "\tVolts")
        print("Load Current =\t", self.iload, "\tAmps")
        print("Switching Frequency =\t", self.Fsw, "\tHz")
        print("Switching Period =\t", self.Tsw, "\ts")
        print("Switched Inductor =\t", self.Ls, "\tH")

        if self.top == "FORWARD":
            print("Isolation XFMR Magnetizing Inductance =\t", self.Lmag, "\tH")

        print("Primary to secondary turns ratio =\t", self.Nps, "\tTurns")

        #Inductor voltages
        print("Inductor charging voltage =\t", self.vCG, "\tVolts")
        print("Inductor discharging voltage =\t", self.vDG, "\tVolts")

        #Inductor currents
        print("Peak current control set point =\t", self.ic, "\tAmps")
        print("Inductor peak current =\t", self.ipk, "\tAmps")
        print("Inductor valley current =\t", self.iv, " \tAmps")
        print("Charge cycle average current =\t", self.iCG, " \tAmps")
        print("Discharge cycle average current =\t",self.iDG, " \tAmps")
        print("Input RMS current =\t",self.iRMS_in, " \tAmps")
        print("Output RMS current =\t",self.iRMS_out, " \tAmps")

        #Helpful variables
        print("Charging current slope =\t", self.mc, "\tA/s")
        print("Discharging current slope =\t",self.md, "\tA/s")
        print("Slope Compensation=\t", self.mcmp, "\tA/s")
        print("alpha =\t ", self.alpha, "Unitless")
        print("Duty Cycle =\t ", self.duty, "\tUnitless")
        print("Discharge duty =\t ", self.dcg, "\tUnitless")
        print("Idle duty =\t ", self.idle, "\tUnitless")
        print("Load at BCM =\t ", self.iDG_bcm, "\tAmps")
        print("Operating in mode: ", self.mode)

################################################################################
##                                                                            ##
##                   Small Signal AC response                                 ##
##                                                                            ##
################################################################################

#
# Instance of steadyState variables are needed to compute the
#   small signal gain model
# Assumes frequency response is wanted:
#  fstart = lowest frequency of interest
#  fend = highest frequency of interest
#  npoints = number of log-spaced components between fstart...fend
#

class smallSignal:
    def __init__(self, steadyState, fstart, fend, npoints):
        self.sys = steadyState
        self.f =  np.logspace(np.log10(fstart), np.log10(fend), npoints)
        self.s = 2j*np.pi*self.f
        self.z1 = np.exp(-self.s*self.sys.Tsw)

        #Peak-to-valley current transfer function
        self.Hv = []

        #Valley-to-average current transfer functions
        self.Hcg = []
        self.Hdg = []
        
        #Output reconstruction filters
        self.Gcg = []
        self.Gdg = []
        
        #Combined control-to-output transfer function
        self.Fcg = []
        self.Fdg = []
        
        #Run the filters
        self.compute_Hv()
        self.compute_Hcg()
        self.compute_Hdg()
        self.compute_G()
        self.compute_F()

    def compute_Hv(self):
        a = self.sys.alpha
        z1 = self.z1
        f = self.f
        self.Hv = a/(1.0 - (1.0 - a)*z1)

    def compute_Hcg(self):
        self.Hcg =  (self.sys.iv/(self.sys.mc + self.sys.md))\
                    *(self.sys.md/self.sys.iv + self.s)

    def compute_Hdg(self):
        self.Hdg =  (self.sys.iv/(self.sys.mc + self.sys.md))\
                    *(self.sys.mc/self.sys.iv - self.s)

    def compute_G(self):
        Iv = self.sys.iv
        mc = self.sys.mc
        md = self.sys.md
        D = self.sys.duty
        Dp = self.sys.dcg
        Tsw = self.sys.Tsw
        s = self.s
        
        #Charging cycle reconstruciton filter
        Gcg = Iv*(1.0 - np.exp(-s*D*Tsw))/s \
                  + mc*( (1.0 - (1.0 + s*D*Tsw)*np.exp(-s*D*Tsw))/s**2)
                   
        #Discharging cycle reconstruction filter
        Gdg = np.exp(-s*D*Tsw)*(Iv + md*Dp*Tsw)*(1.0 - np.exp(-s*Dp*Tsw))/s \
                  - np.exp(-s*D*Tsw)*md*( (1.0 - (1.0 + s*Dp*Tsw)*np.exp(-s*Dp*Tsw))/s**2)
                  
        #Normalization functions
        normCG = 2.0/(D*D*Tsw*Tsw*mc + 2.0*D*Tsw*Iv)
        normDG = 2.0/(Dp*Dp*Tsw*Tsw*md + 2.0*Dp*Tsw*Iv)
        
        #Normalize
        self.Gcg = normCG*Gcg
        self.Gdg = normDG*Gdg

    def compute_F(self):
        self.Fcg = self.Hv*self.Hcg*self.Gcg
        self.Fdg = self.Hv*self.Hdg*self.Gdg
    
    def plot_response(self, f, H):
        mag_dB = 20.0*np.log10(np.abs(H))
        phase_deg = 180.0*np.unwrap(np.angle(H))/np.pi
        
        fig, ax = plt.subplots(nrows=2,ncols=1)
        plt.subplot(2, 1, 1)
        plt.semilogx(f, mag_dB,"r")
        plt.grid()
        plt.subplot(2, 1, 2)
        plt.semilogx(f, phase_deg,"b-")
        plt.grid()
        plt.show()
        
        
        

