from modulator import steadyState, modulatorSystem, smallSignal

##
## Test Program
##
sys = modulatorSystem(75.0, 12.5, 0.75, 3.0, 120000.0, 580e-6, 0.0, 80000.0, (54.0/8.0), "FLYBACK", "DCMCCM")
ss =  steadyState(sys)
ss.print_sys_params()

sys.Vin = 75.0
print("\n\nChange input voltage to ", sys.Vin, " Volts")
ss.update(sys)
ss.print_sys_params()

slsg = smallSignal(ss, 10.0, 120.0e3, 1000)

slsg.plot_response(slsg.f, slsg.Fdg)
