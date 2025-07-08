import pandas as pd
import numpy as np

class component:
    def __init__(self, name="default", value=1, tol=1, sigma=3, minval=0.99, maxval=1.01, step = 0.01, usetol=True, makestep=False, logspace=False, clip=True):
        self.name = name
        self.logspace = logspace
        self.typ = value
        self.step = step
        self.valsize = 0
        self.maxval = value
        self.minval = value
        self.sigma = sigma
        self.clip = clip
        self.tolp = 0.0
        self.toln = 0.0
        self.value = value

        if makestep:
            self.maxval = minval
            self.minval = maxval
            self.step = step
            if logspace:
                stop = np.log10(maxval)
                start = np.log10(minval)
                num = int((stop-start)/step)
                self.value = np.logspace(start, stop, num=num, endpoint=True, base=10.0)
            else:
                self.value = np.arange(start=minval, stop=(maxval+step), step=step)
            self.valsize = len(self.value)
            #print("Makestep supposed to be true")
            #print(self.value)
            return

        if usetol:
            self.tolp = tol/100.0
            self.toln = tol/100.0
            self.maxval = value*(1.0+tol/100.0)
            self.minval = value*(1.0-tol/100.0)
        else:
            self.maxval = maxval
            self.minval = minval
            self.tolp = 1.0 - value/maxval
            self.toln = value/minval - 1.0

        #self.print_cmpnt()
    def reset_to_typical(self):
        if self.valsize <= 1:
            self.value = self.typ

    def run_monte_carlo(self):
        self.value = self.maxval #placeholder

    def print_cmpnt(self):
        print(f"{self.name}\t{self.minval}\t{self.typ}\t{self.maxval}")

class ipl:
    def __init__(self, configfile):
        self.cfile = configfile
        self.df = pd.read_excel(self.cfile)
        self.ingest_settings()
        self.generate_output_arrays()

    def ingest_settings(self):
        # first create a list of components from the dataframe
        df = self.df
        nrows = df.shape[0]
        self.components = []
        for r in range(nrows):
            name = df.loc[r, 'Parameter']
            typ = df.loc[r, 'Typ']
            tol = df.loc[r, 'Tol']
            minval = df.loc[r, 'Min']
            maxval = df.loc[r, 'Max']
            name = df.loc[r, 'Parameter']
            mul = df.loc[r, 'Multiplier']
            unit = df.loc[r, 'Unit']
            step = df.loc[r, 'Linstep']
            logstep = df.loc[r, 'Logstep']
            mulval = 1.0

            if mul == 'f':
                mulval = 1.0e-15
            if mul == 'p':
                mulval = 1.0e-12
            if mul == 'n':
                mulval = 1.0e-9
            if mul == 'u':
                mulval = 1.0e-6
            if mul == 'μ':
                mulval = 1.0e-6
            if mul == 'm':
                mulval = 1.0e-3
            if mul == '%':
                mulval = 0.01
            if mul == '-':
                mulval = 1.0
            if mul == 'k':
                mulval = 1.0e3
            if mul == 'M':
                mulval = 1.0e6
            if mul == 'G':
                mulval = 1.0e9
            if mul == 'T':
                mulval = 1.0e12

            if (step != "-") or (logstep != "-"):
                #print(f"step evaluated true on name {name} and stepval {step}")
                if (step != "-"):
                    cmpnt = component(name=name,value=typ*mulval, maxval=maxval*mulval, minval=minval*mulval, sigma=3.0,  usetol=False,clip=True,makestep=True, step=step)
                    self.components.append(cmpnt)
                    #print(cmpnt.value)
                else:
                    cmpnt = component(name=name,value=typ*mulval, maxval=maxval*mulval, minval=minval*mulval, sigma=3.0,  usetol=False,clip=True,makestep=True, step=logstep, logspace=True)
                    self.components.append(cmpnt)
                    #print(cmpnt.value)
            else:
                if tol != "-":
                    cmpnt = component(name=name,value=typ*mulval, tol=tol, sigma=3.0,usetol=True,clip=True,makestep=False)
                    self.components.append(cmpnt)
                if minval != "-" and maxval != "-":
                    cmpnt = component(name=name,value=typ*mulval, maxval=maxval*mulval, minval=minval*mulval, sigma=3.0,  usetol=False,clip=True,makestep=False)
                    self.components.append(cmpnt)


        self.assign_paramvals()

    #
    #  Assign variables used in computations to current value
    #    The current value is assumed to be pre-selected using
    #    a random selection based on specified distribution
    #    or it has been reset to typical
    #
    def assign_paramvals(self):
            #Next initialize all variables used for IPL computations
            dbg = self.get_cmpnt_val("debug")
            self.debug = False
            if dbg != 0:
                print("Debug messages enabled")
                self.debug = True
            else:
                print("DEBUG messages suppressed")

            self.vcg = self.get_cmpnt_val("Vcg")
            self.vdg = self.get_cmpnt_val("Vout")
            self.rcs = self.get_cmpnt_val("Rcs")
            self.rdg = self.get_cmpnt_val("Rdg")
            self.csfst = self.get_cmpnt_val("Csfst")
            self.vsns = self.get_cmpnt_val("Vsense")
            self.imax = self.vsns/self.rcs
            self.gvc = self.get_cmpnt_val("gVC")
            self.isfst = self.get_cmpnt_val("Isfst")
            self.lm = self.get_cmpnt_val("Lm")
            self.nps = self.get_cmpnt_val("Nps")
            cfs1 = self.get_cmpnt_val("Cfs1")
            cfs2 = self.get_cmpnt_val("Cfs2")
            cfs = cfs1 + cfs2
            self.fsw = 10e-6/cfs  #LT3837 Fsw approximation
                                  # Fosc = 100kHz*100/Cosc (pF)
                                  # = (100k*100/1e-12)*(1/Cosc)
                                  # = 10e-6/Cosc
            self.tsw = 1.0/self.fsw
            self.dstart = self.get_cmpnt_val("Dstart")
            self.dend = self.get_cmpnt_val("Dend")
            self.kcomp = self.get_cmpnt_val("Kcomp")
            self.mcmp = self.imax*self.kcomp*self.fsw/(self.dend-self.dstart)

            self.vout = self.get_cmpnt_val("Vout")
            self.cf = self.get_cmpnt_val("Cf")
            self.rf = self.get_cmpnt_val("Rfl")
            self.rfu1 = self.get_cmpnt_val("Rfu1")
            self.rfu2 = self.get_cmpnt_val("Rfu2")
            self.rfu3 = self.get_cmpnt_val("Rfu3")
            #print(self.rfu1, self.rfu2, self.rfu3)
            self.rru = self.get_cmpnt_val("Rru")
            self.rrl = self.get_cmpnt_val("Rrl")
            self.vref = self.get_cmpnt_val("Vref")
            self.tp = self.get_cmpnt_val("Tprop")

            self.fplot = self.get_cmpnt_val("Fplot")

            if self.debug:
                self.spew_typical()
                print(f"Cfs = {cfs*1e12} pF")
                print(f"Slope comp = {self.mcmp/100.0e3:.2f} kA/s")
                print(f"Fsw= {self.fsw/1.0e3:.2f} kHz")

    def spew_typical(self):
        df = self.df

        nrows = df.shape[0]

        for r in range(nrows):
            typ = df.loc[r, 'Typ']
            name = df.loc[r, 'Parameter']
            mul = df.loc[r, 'Multiplier']
            unit = df.loc[r, 'Unit']

            if mul == 1:
                print(f"{name}\t{typ:.2f}\t{unit}")
            else:
                print(f"{name}\t{typ:.2f}\t{mul}{unit}")

    def find_cmpnt(self,findname):
        for c in range(len(self.components)):
            if self.components[c].name == findname:
                if self.debug:
                    print(f"Found component \"{findname}\":")
                    self.components[c].print_cmpnt()
                return self.components[c]

    def get_cmpnt_val(self,findname):
        for c in range(len(self.components)):
            if self.components[c].name == findname:
                #print(f"Current Value \"{findname}\"= {self.components[c].value}")
                return self.components[c].value

    def compute_mcmp(self):
        cfs1 = self.get_cmpnt_val("Cfs1")
        cfs2 = self.get_cmpnt_val("Cfs2")
        cfs = cfs1 + cfs2
        self.fsw = 10e-6/cfs
        self.tsw = 1.0/self.fsw
        self.mcmp = self.imax*self.kcomp*self.fsw/(self.dend-self.dstart)

        return self.mcmp

    #
    # Calculate equivalent 'trip' current threshold
    #   accounting for RC filter, comparator overdrive/prop delay
    #
    def compute_itrip_eq(self, vin):
        vout = self.vout
        lm = self.lm
        rcs = self.rcs
        cf = self.cf
        rf = self.rf
        rru = self.rru
        rrl = self.rrl
        rfu1 = self.rfu1
        rfu2 = self.rfu2
        rfu3 = self.rfu3
        vref = self.vref
        tp = self.tp
        ts = self.tsw

        rh = rfu1 + rfu2 + rfu3

        voffst = vin*rf/(rh+rf)

        # RC Filter settles to constant offset, Cfilter*dVrcs/dt
        dvdt_sns = rcs*vin/lm #change of sense voltage
        dVsense = rf*cf*dvdt_sns #current through filter resistor settles to constant C*dV/dt before cycle finishes

        # Offset due to propagation delay & rise time
        #   Cannot begin to respond more quickly than min prop delay
        dvP = dvdt_sns*tp

        # filter delay added to prop delay results in
        # equivalent increase to Vtrip
        vt0 = vref*rrl/(rru + rrl)

        # Equivalaent Vtrip accounting for triggering delays
        vt = vt0 + dVsense + dvP # Add offset due to filter cap

        #Equivalent Itrip, reflected back to current sense resistor
        Itrip = (vt - voffst)/rcs

        return Itrip

    #
    # Compute k_vc, piecewise function of duty cycle and itrip
    #
    def compute_kvc(self, Itrip=10.0, df=0.5 ):
        kcomp = self.kcomp
        imax = self.imax
        dstart = self.dstart
        dend = self.dend
        Rcs = self.rcs
        gVC = self.gvc

        kVC = 1.0 + Itrip*Rcs/gVC

        if (df <1.0) and (df > dstart):
            kVC = 1.0 + (Rcs/gVC)*(Itrip + imax*kcomp*(df - dstart)/(dend - dstart))

        return kVC

    #
    # Compute vs, piecewise function of duty cycle and itrip
    #
    def compute_vs(self, vin=12.0, Itrip=10.0, df=0.5 ):
        Rcs = self.rcs
        gVC = self.gvc

        kvc = self.compute_kvc(Itrip=Itrip, df=df )
        idpk = self.compute_idpk(vin=vin, kvc=kvc )

        Vs = kvc + idpk*Rcs/gVC

        return Vs

    #
    # Compute  I_Delta_PK, piecewise function of duty cycle and itrip
    #
    def compute_idpk(self, vin=12.0, kvc=2.0 ):
        kcomp = self.kcomp
        rcs = self.rcs
        rdg = self.rdg
        gvc = self.gvc
        lm = self.lm
        tsw = self.tsw
        isfst = self.isfst

        IdPK = (np.sqrt( (kvc*gvc/rcs)**2 + 4.0*vin*isfst*rdg*tsw*gvc/(lm*rcs)) - kvc*gvc/rcs)/2.0

        return IdPK

    #
    #  SFST pin IIR coefficient
    #
    def compute_as(vs=2.0, vin=8.5, lm=35.0e-6, rdg=1000, ci=100.0e-9):
        return vs*lm/(vin*rdg*ci)

    #
    # Generate arrays of all variables dependent on Vin
    #
    def generate_output_arrays(self):
        md = self.vdg*self.nps/self.lm
        lm = self.lm
        ci = self.csfst
        rdg = self.rdg
        tsw = self.tsw
        mc = 0.0
        self.s = 1j*2.0*np.pi*self.fplot
        self.z = np.exp(-self.s*self.tsw)

        self.md = md
        self.mc_ = []
        self.duty_ = []
        self.itrip_ = []
        self.kvc_ = []
        self.vs_ = []
        self.idpk_ = []
        self.ipk_ = []
        self.icg_ = []
        self.pin_ = []
        for vc in self.vcg:
            mc = vc/self.lm
            duty = md/(mc + md)
            itrip = self.compute_itrip_eq(vc)
            kvc = self.compute_kvc(Itrip=itrip, df=duty)
            vs = self.compute_vs(vin=vc, Itrip=itrip, df=duty )
            idpk = self.compute_idpk(vin=vc, kvc=kvc )
            Ipk = itrip + idpk
            Icg = (Ipk - mc*duty*tsw/2.0)*duty
            Pin = Icg*vc
            self.mc_.append(mc)
            self.duty_.append(duty)
            self.itrip_.append(itrip)
            self.kvc_.append(kvc)
            self.vs_.append(vs)
            self.idpk_.append(idpk)
            self.ipk_.append(Ipk)
            self.icg_.append(Icg)
            self.pin_.append(Pin)
            #print(vc,duty,itrip,kvc,vs,idpk,Ipk,Icg,Pin)








