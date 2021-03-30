
## Type II compensator with optocoupler fast-lane
#
#   [Vfb]--*-----------------*
#          |                 |
#          |                 \
#          \                 /
#          / Ri              \ Ro
#          \                 /
#          /                 |
#          |                 __
#          |            LED _\/_ ~^~>[CTR]-->[Iemitter]
#          |      Cp         |
#          *------||---------*
#          |                 |
#          |   Cf     Rf     |
#          *---||---/\/\/----*-->[Vk]
#          |                 |
#          |                 |
#          |               \____
#          |                 /\ \
#          *----------------/  \
#          |            +  ------
#          |           Vref-  |
#          /                  |
#          \  Rdc_bias        |
#          /                  |
#          \                  |
#          |                  |
#          *------------------*
#                             |
#                           -----
#                            ---
#                             -
#             Vk(s)
# Hk(s) =  -------------
#             Vfb(s)
#
#          Iemitter(s)
# Hc(s) = -------------
#             Vfb(s)
#

import numpy as np

##
## Engineering notation shorthand
##
p = 1e-12
n = 1e-9
u = 1e-6
k = 1e3

class errorAmp:

    def __init__(self, Vref, Rdc_Bias, Ro, Ri, Rf, Cf, Cp, CTR, fc_opto, fstart, fend, npoints):
        # Plotting range defaults
        self.fstart = 10.0
        self.fend = 120.0*k
        self.npoints = 1000
        self.f =  np.logspace(np.log10(self.fstart), np.log10(self.fend), self.npoints)
        self.s = 2j*np.pi*self.f

        # Error amp default component values
        self.Vref = 2.5
        self.Rdc_Bias = 8.25*k
        self.Cp = 100.0*n
        self.Cf = 22.0*n
        self.Rf = 121.0*k
        self.Ri = 33.0*k
        self.Ro = 1.0*k
        self.fc_opto = 100.0*k
        self.CTR = 0.4
        
        # Transfer functions
        
        
        self.updateParams(Vref, Rdc_Bias, Ro, Ri, Rf, Cf, Cp, CTR, fc_opto, fstart,\
                     fend, npoints)

    def updateParams(self, Vref, Rdc_Bias, Ro, Ri, Rf, Cf, Cp, CTR, fc_opto, \
                     fstart, fend, npoints) :
        # Plotting ranges
        self.fstart = fstart
        self.fend = fend
        self.npoints = npoints
        self.f =  np.logspace(np.log10(fstart), np.log10(fend), npoints)
        self.s = 2j*np.pi*self.f

        # Error amp component values
        self.Vref = Vref
        self.Rdc_Bias = Rdc_Bias
        self.Cp = Cp
        self.Cf = Cf
        self.Rf = Rf
        self.Ri = Ri
        self.Ro = Ro
        self.fc_opto = fc_opto
        self.CTR = CTR
        
        self.compute_H()
            
        ##
        ## System transfer functions
        ##
    def compute_H(self) :
        s = self.s
        p0 = 1.0/(s*self.Ri*self.Cp)
        p1 = (self.Cf + self.Cp)/(self.Rf*self.Cf*self.Cp)
        z0 = 1.0/(self.Rf*self.Cf)
        Ro = self.Ro
        
        wopt = 2.0*np.pi*self.fc_opto
        popt = self.CTR*wopt/(s + wopt)
        self.Hk = -(1.0/self.Ro)*p0*(s + z0)/(s + p1) #Without "fast lane"
        self.Hc = (1.0/Ro - self.Hk)*popt  #Add "fast lane" effect





