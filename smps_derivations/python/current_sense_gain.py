
## Current sensing network transfer function
#
#
#                         RfBULK        Rmcmp
#              [VBULK]___/\/\/\____x___/\/\/\___[Vmcmp]
#                                  |
#                        Rf5V      |              ~~~
#           [+5Vref]___/\/\/\______x               | 
#                                  |              \./ Ipri
#    [Ve]                          |               |
#     _________x___/\/\/\__________x____/\/\/\_____x___ [Vcs]
#    |         |    RfFB           |      RfCS     |
#   _-_        |                   |               |
#  / . \       /            [Vfb]__|               \
# | /|\ | Ie   \ Rpd                               / 
# |  |  |      /                                   \ Rcs
#  \_ _/       \                                   /
#    :         |                                   \
#    |         |                                   |
#    |_________x___________________________________x
#  Optocoupler                                     | 
#  Emitter                                         |
#                                                -----
#                                                 ---
#          Vfb                                    -
#  Gcs = -------  Volts/Volt at FB node
#          Ie
#
#          Ic
#  Gav = ------  Amps/Volt, Vfb node voltage to peak current control set point
#          Vfb
#
#  This circuit is assumed to have frequency response that is negligible
#   below converter Nyquist frequency (Fsw/2).  A DC gain value is returned
#   as a single scalar value.
#

import numpy as np

##
## Engineering notation shorthand
##
p = 1e-12
n = 1e-9
u = 1e-6
m = 1e-3
k = 1e3
M = 1e6

class currentSenseGain:

    def __init__(self, Rcs, RfCS, RfFB, Rpd, Rmcmp, Rf5V, RfBULK):

        # Current sense network default component values
        self.Rcs = 0.33
        self.RfCS = 1.24*k
        self.RfFB = 2.21*k
        self.Rpd = 2.21*k
        self.Rmcmp = 20.0*k
        self.Rf5V = 15.4*k
        self.RfBULK = 1.18*M
        
        self.Gav = 1.0

        self.updateParams(Rcs, RfCS, RfFB, Rpd, Rmcmp, Rf5V, RfBULK)

    def updateParams(self, Rcs, RfCS, RfFB, Rpd, Rmcmp, Rf5V, RfBULK):
        # Current sense network
        self.Rcs = Rcs
        self.RfCS = RfCS
        self.RfFB = RfFB
        self.Rpd = Rpd
        self.Rmcmp = Rmcmp
        self.Rf5V = Rf5V
        self.RfBULK = RfBULK
        
        self.compute_G()
            
        ##
        ## System transfer functions
        ##
    def compute_G(self) :
        Rcs = self.Rcs
        RfCS = self.RfCS
        RfFB = self.RfFB
        Rpd = self.Rpd
        Rmcmp = self.Rmcmp
        Rf5V = self.Rf5V
        RfBULK = self.RfBULK
        
        # Disconnecting RfFB from Ve, express equivalent resistance
        # looking from Vfb end of RfFB to ground
        Rthev_vfb = 1.0/(1.0/(RfCS + Rcs) + 1.0/Rf5V + 1.0/RfBULK \
                    + 1.0/Rmcmp)
        # Reconnect RfFB and disconnect Rpd, express equivalent resistance
        # from Ve to ground
        Rve = Rthev_vfb + RfFB
        
        # Finally reconnect Rpd and express equivalent resistance
        # from Ve to ground
        Rthev_ve = Rve*Rpd/(Rve + Rpd)
        
        # Ve is I_e*Rthev_ve.  Skipping a few steps,
        # Vfb = Ve*Rthev_vfb/(Rthev_fb + RfFB)
        # Gcs = Vfb/Ie = 
        Gcs = Rthev_ve*Rthev_vfb/(Rthev_vfb + RfFB) #Units of Volts
        
        # Next gain for Vfb/Ipri is needed to get A/V gain at Vfb
          # First get V/A (Vfb/Ipri)
        Rthev_vfba = 1.0/(1.0/(RfFB + Rpd) + 1.0/Rf5V + 1.0/RfBULK \
                    + 1.0/Rmcmp)
          # Gfbcs = Vfb/Vcs (V/V)
        Gfbcs = Rthev_vfba/(Rthev_vfba + RfCS) 
          # Gain, Volts/A from Vcs to Vfb
        Gva = Rcs*Gfbcs
        
        self.Gav = 1.0 - Gcs/Gva  # Inverse is A/V
        print("Feedback gain = ", self.Gav, " Amps/Volt")
        
                 





