
## Converter output impedance network
#
#  [Zout] -->          _-_  _-_  _-_  _-_  
#     __________x_____/   \/   \/   \/   \_____x_______________x___ [Vout]
#    |  [Vfb]   |             Lout+ESRl        |               |
#   _-_         |                              |               |
#  / . \      __|__                          __|__             \
# | /|\ |     ----- Cout                     ----- Cload       / 
# |  |  |       |                              |               \ Rload
#  \_ _/      /ESRco/                        /ESRcl/           /
#    :          |                              |               \
#    |          |                              |               |
#    |__________x______________________________x_______________x
#                                                              |
#                                                            -----
#                                                             ---
#                                                              -

import numpy as np

##
## Engineering notation shorthand
##
p = 1e-12
n = 1e-9
u = 1e-6
m = 1e-3
k = 1e3

class outputZ:

    def __init__(self, Cout, Cload, Lout, ESRco, ESRcl, ESRl, Rload, fstart,\
                       fend, npoints):
        # Plotting range defaults
        self.fstart = 10.0
        self.fend = 120.0*k
        self.npoints = 1000
        self.f =  np.logspace(np.log10(self.fstart), np.log10(self.fend), self.npoints)
        self.s = 2j*np.pi*self.f

        # Error amp default component values
        self.Cout = 3.0*330.0*u;
        self.Cload = 330.0*u
        self.Lout = 470.0*n
        self.Rco = 14.0*m/3.0
        self.Rcl = 14.0*m
        self.Rl = 4.0*m
        self.Rload = 4.2
        
        self.Zout = []

        self.updateParams(Cout, Cload, Lout, ESRco, ESRcl, ESRl, Rload, fstart,\
                          fend, npoints)

    def updateParams(self, Cout, Cload, Lout, ESRco, ESRcl, ESRl, Rload, fstart,\
                       fend, npoints):
        # Plotting ranges
        self.fstart = fstart
        self.fend = fend
        self.npoints = npoints
        self.f =  np.logspace(np.log10(fstart), np.log10(fend), npoints)
        self.s = 2j*np.pi*self.f

        # Error amp component values
        self.Cout = Cout;
        self.Cload = Cload
        self.Lout = Lout
        self.Rco = ESRco
        self.Rcl = ESRcl
        self.Rl = ESRl
        self.Rload = Rload
        
        self.compute_Z()
            
        ##
        ## System transfer functions
        ##
    def compute_Z(self) :
        s = self.s
        
        zCout = 1.0/(s*self.Cout) + self.Rco
        zCload = 1.0/(s*self.Cload) + self.Rcl
        zLout = s*self.Lout + self.Rl
        
        zLoad = zLout + zCload*self.Rload/(zCload + self.Rload)
        self.Zout = zLoad*zCout/(zLoad + zCout)
        





