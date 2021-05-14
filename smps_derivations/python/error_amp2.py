
## Type II compensator with optocoupler fast-lane
#
#   [Vfb]--*-----------------*-------*
#          |                 |        |
#          |                 |        \
#          \                 \        /
#          / Ri              / Ro     \ R_LED
#          \                 \        /
#          /                 /        |
#          |                 |        __
#          |                 |   LED _\/_ ~^~>[CTR]-->[Iemitter]
#          |      Cp         |        |
#          *------||---------*--------*
#          |                 |
#          |   Cf1   Rf1     |
#          *---||---/\/\/----*-->[Vk]
#          |                 |
#          |   Cf2   Rf2     |
#          *---||---/\/\/----*-
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

class errorAmp2z:

    def __init__(self, Vref, gm, Rdc_Bias, Ro, Rled, Ri, Rf1, Cf1, Rf2, Cf2, Cp, CTR, \
                 fc_opto, fstart, fend, npoints):
        # Plotting range defaults
        self.fstart = 10.0
        self.fend = 120.0*k
        self.npoints = 1000
        self.f =  np.logspace(np.log10(self.fstart), np.log10(self.fend), self.npoints)
        self.s = 2j*np.pi*self.f

        # Error amp default component values
        self.Vref = 2.5
        self.gm = 3.0
        self.Rdc_Bias = 8.25*k
        self.Cp = 100.0*n
        self.Cf1 = 10.0*n
        self.Rf1 = 200.0*k
        self.Cf2 = 150.0*n
        self.Rf2 = 332.0*k
        self.Ri = 33.0*k
        self.Ro = 1.0*k
        self.Rled = 1.0*k
        self.fc_opto = 100.0*k
        self.CTR = 0.4

        # Transfer functions
        self.Hk = []
        self.Hc = []

        self.updateParams(Vref, gm, Rdc_Bias, Ro, Rled, Ri, Rf1, Cf1, Rf2, Cf2, Cp, CTR, \
                          fc_opto, fstart, fend, npoints)

    def updateParams(self, Vref, gm, Rdc_Bias, Ro, Rled, Ri, Rf1, Cf1, Rf2, Cf2, Cp, CTR, \
                 fc_opto, fstart, fend, npoints) :
        # Plotting ranges
        self.fstart = fstart
        self.fend = fend
        self.npoints = npoints
        self.f =  np.logspace(np.log10(fstart), np.log10(fend), npoints)
        self.s = 2j*np.pi*self.f

        # Error amp component values
        self.Vref = Vref
        self.gm = gm
        self.Rdc_Bias = Rdc_Bias
        self.Cp = Cp
        self.Cf1 = Cf1
        self.Rf1 = Rf1
        self.Cf2 = Cf2
        self.Rf2 = Rf2
        self.Ri = Ri
        self.Ro = Ro
        self.Rled = Rled
        self.fc_opto = fc_opto
        self.CTR = CTR

        self.compute_H()

        ##
        ## System transfer functions
        ##
    def compute_H(self) :
        s = self.s

        Cf1 = self.Cf1
        Rf1 = self.Rf1
        Cf2 = self.Cf2
        Rf2 = self.Rf2
        Cp = self.Cp
        Ro = self.Ro
        Rl = self.Rled
        gm = self.gm
        Rb = self.Rdc_Bias
        Rh = self.Ri

        wopt = 2.0*np.pi*self.fc_opto
        Hopt = self.CTR*wopt/(s + wopt)

        zcf1 = 1.0/(s*Cf1)
        zcf2 = 1.0/(s*Cf2)
        zcp =  1.0/(s*Cp)
        
        zf1 = zcf1 + Rf1
        zf2 = zcf2 + Rf2
        zf12 = zf1*zf2/(zf1 + zf2)

        Zf = zf12*zcp/(zf12 + zcp)
        Zi = Rl*Rh/(Rl + Rh)
        Zo = Ro*Rl/(Ro+Rl)
        Gth = Rl/(Rl + Rh)

        # Transconductance amp open loop gain
        fbw = 2.0*np.pi*6.0*k #TL431 LF pole
        Gs = (1.0/100.0)*gm*(s+100.0*fbw)/(s + fbw)

        # Closed loop transfer function
        self.Hk = Zf/Zi

        Hled = (1.0/Rl)*(Zi + Gth*(Zf - 1.0/Gs) + 1.0/Gs)/(Zi + ((Zf + Zi)/Zo + 1.0)/Gs)
        self.Hc = Hled*Hopt  #Add optocoupler response





        ### EOF ###
