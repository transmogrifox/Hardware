[Transient Analysis]
{
   Npanes: 5
   Active Pane: 3
   {
      traces: 2 {524292,0,"V(vout)"} {524294,0,"V(vstab)"}
      X: ('m',0,0,0.002,0.02)
      Y[0]: (' ',0,-1,1,13)
      Y[1]: ('_',0,1e+308,0,-1e+308)
      Volts: (' ',0,0,0,-1,1,13)
      Log: 0 0 0
   },
   {
      traces: 1 {524297,0,"V(n020)"}
      X: ('m',0,0,0.002,0.02)
      Y[0]: ('m',0,0,0.07,0.77)
      Y[1]: ('m',0,1e+308,0.09,-1e+308)
      Volts: ('m',0,0,0,0,0.07,0.77)
      Log: 0 0 0
   },
   {
      traces: 4 {524290,0,"V(n010)"} {524291,0,"V(dc)"} {524293,0,"0.85V"} {524296,0,"10mV"}
      X: ('m',0,0,0.002,0.02)
      Y[0]: (' ',1,-0.9,0.9,9)
      Y[1]: ('m',0,1e+308,0.09,-1e+308)
      Volts: (' ',0,0,0,-0.9,0.9,9)
      Log: 0 0 0
   },
   {
      traces: 2 {524298,0,"V(dummy_on)"} {524295,0,"V(dummy_off)"}
      X: ('m',0,0,0.002,0.02)
      Y[0]: (' ',0,-2,2,18)
      Y[1]: (' ',1,1e+308,0.9,-1e+308)
      Volts: (' ',0,0,0,-2,2,18)
      Log: 0 0 0
   },
   {
      traces: 1 {524299,0,"V(audio)"}
      X: ('m',0,0,0.002,0.02)
      Y[0]: (' ',1,-0.3,0.3,2.7)
      Y[1]: (' ',0,1e+308,2,-1e+308)
      Volts: (' ',0,0,1,-0.3,0.3,2.7)
      Log: 0 0 0
   }
}