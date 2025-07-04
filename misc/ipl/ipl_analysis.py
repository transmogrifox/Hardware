import pandas as pd
import lib.ipl_lib as iplib

ipl0 = iplib.ipl(configfile="ipl_config.xlsx")

#ipl0.spew_typical()
dstart = ipl0.find_cmpnt("Dstart").value
print(f"Dstart = {dstart*100.0:.0f} %")
cfs1 = ipl0.get_cmpnt_val("Cfs1")

it60 = ipl0.compute_itrip_eq(60.0)
it8 = ipl0.compute_itrip_eq(8.0)

print(f"Cfs1 = {cfs1*1e12:.2f} pF")
print(f"Slope Compensation, mcmp = {ipl0.compute_mcmp()/1000.0:.1f} kA/s")
print(f"Itrip [8Vin, 60Vin] = {it8:.2f}, {it60:.2f} A")








