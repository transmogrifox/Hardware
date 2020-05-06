Version 4
SymbolType BLOCK
LINE Normal -71 -27 -71 -54
LINE Normal -71 -27 -71 -27
LINE Normal -78 -37 -71 -27
LINE Normal -64 -37 -78 -37
LINE Normal -71 -27 -64 -37
LINE Normal 73 -52 73 -25
LINE Normal 73 -52 73 -52
LINE Normal 80 -42 73 -52
LINE Normal 66 -42 80 -42
LINE Normal 73 -52 66 -42
LINE Normal 73 0 73 -16
LINE Normal 124 0 73 0
LINE Normal 73 -80 73 -63
LINE Normal 124 -80 73 -80
LINE Normal -72 0 -124 0
LINE Normal -72 -16 -72 0
LINE Normal -71 -80 -71 -63
LINE Normal -124 -80 -71 -80
RECTANGLE Normal -128 -104 127 213
RECTANGLE Normal -32 213 -128 48
RECTANGLE Normal 71 213 127 112
CIRCLE Normal -47 -16 -95 -63
CIRCLE Normal 49 -63 97 -16
TEXT -116 96 Left 2 Icg
TEXT -115 125 Left 2 Idg
TEXT 93 159 Left 2 Ic
TEXT 97 125 Left 2 +
TEXT 98 190 Left 2 -
TEXT -57 -73 Left 2 Icg
TEXT 19 -15 Left 2 Idg
TEXT -116 64 Left 2 DUTY
WINDOW 0 0 -104 Bottom 2
WINDOW 39 -171 230 Left 2
WINDOW 40 -49 261 Center 2
SYMATTR SpiceLine Fsw=100k Lm=100u mcmp=50k
SYMATTR SpiceLine2 Dmin=0 Dmax=0.96
PIN 128 128 NONE 8
PINATTR PinName Ic+
PINATTR SpiceOrder 1
PIN 128 192 NONE 8
PINATTR PinName Ic-
PINATTR SpiceOrder 2
PIN -128 -80 NONE 8
PINATTR PinName Vcg+
PINATTR SpiceOrder 3
PIN -128 0 NONE 8
PINATTR PinName Vcg-
PINATTR SpiceOrder 4
PIN 128 -80 NONE 8
PINATTR PinName Vdg+
PINATTR SpiceOrder 5
PIN 128 0 NONE 8
PINATTR PinName Vdg-
PINATTR SpiceOrder 6
PIN -128 96 NONE 8
PINATTR PinName Icharge
PINATTR SpiceOrder 7
PIN -128 128 NONE 8
PINATTR PinName Idischarge
PINATTR SpiceOrder 8
PIN -128 160 LEFT 8
PINATTR PinName Ipeak
PINATTR SpiceOrder 9
PIN -128 192 LEFT 8
PINATTR PinName Ivalley
PINATTR SpiceOrder 10
PIN -128 64 NONE 8
PINATTR PinName DUTY
PINATTR SpiceOrder 11
