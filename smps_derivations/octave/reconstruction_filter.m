k = 1000;
u = 1e-6;

fsw = 130*k
Ts = 1/fsw;

ff = 10:10:fsw*4;
ws = 2*pi*ff;
s = j*ws;
z1 = e.^(-s*Ts);

Lm = 23*u
Vin = 18
Vout = 5.25
Nsp = 4
Vo = Nsp*Vout
D = Vo/(Vin + Vo)
Dp = 1-D

iv = 7.5

mc = Vin/Lm
md = Vo/Lm

hs = md*(Ts*Dp./s + 1./(s.*s)).*(e.^(-s*Ts) - e.^(-s*Ts*D)) + (mc*D + iv).*(e.^(-s*Ts.*D)).*(1 - e.^(-s*Ts*Dp))./s;

subplot(2,1,1)
semilogx(ff, 20*log10(abs(hs)),"r")
subplot(2,1,2)
semilogx(ff, 180*unwrap(angle(hs))/pi, "m")
