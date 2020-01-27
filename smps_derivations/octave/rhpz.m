k = 1000;
u = 1e-6;

fsw = 130*k
Ts = 1/fsw;

ff = 10:10:fsw*5;
ws = 2*pi*ff;
s = j*ws;
z1 = e.^(-s*Ts);

hizoh = Ts*s./((1-e.^(-s*Ts)));

Lm = 2300*u
Vin = 18.75
Vout = 5.25
Nsp = 4
Vo = Nsp*Vout
D = Vo/(Vin + Vo)

iv = 7.5

mc = Vin/Lm
md = Vo/Lm

a = 1/(mc + md) 
b = Ts*(1-a*md) 

c = (0.5*md*a*a - a)/Ts
d = 0.5*md*a*a/Ts
ee = (a - md*a*a)/Ts
f = (b-md*a*b)/Ts
g = md*a*b/Ts
h = (0.5*md*b*b)/Ts

td = a*iv - a*iv + b
td = (1-D)*Ts
td2 = td*td
td2 = a*a*iv*iv + a*a*iv*iv - 2*a*a*iv*iv - 2*a*b*iv + 2*a*b*iv + b*b

tdio = (a*iv*iv - a*iv*iv + b)*iv
hmdtd2 = 0.5*md*td2 
Ioo = (tdio + hmdtd2)/Ts

Ioo = (c + d + ee)*iv*iv + (f + g)*iv + h
Ioo = (td*iv + 0.5*md*td*td)/Ts
Pout = Ioo*Vo
Rl = Vo*Vo/Pout
Dp2 = (1-D)*(1-D)

frhpz = Rl*Dp2/(2*pi*Lm*D)
wrhpz = 2*pi*frhpz


A0 = (2*c*iv + ee*iv + f)
A1 = (2*d*iv + ee*iv + g)

hz = (1./(A0 + A1)) .* (A0 + A1*z1);
hs = (1/wrhpz)*(s - wrhpz);
%hz = A0 + A1*z1;

semilogx(ff, 20*log10(abs(hz)), ff, 20*log10(abs(hz.*hizoh)), ff, 20*log10(abs(hs)) )

