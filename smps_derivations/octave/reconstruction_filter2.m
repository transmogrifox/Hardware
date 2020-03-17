k=1000;
u=1e-6;

fs = 100*k

f = 10:10:(fs*6);
w = 2*pi*f;
s = j*w;

Ts = 1/fs 
Ls = 230*u
Vcg = 24
Vdg = 5.45*4

mc = Vcg/Ls 
md = Vdg/Ls 

D = Vdg/(Vcg + Vdg) 
tc = D*Ts

iv = 1/D

% Charging cycle pulse response "x"
x1 = iv*(1 - e.^(-s*tc))./s;
x2 = mc*( (1 - (1 + s*tc).*e.^(-s*tc))./(s.^2) );

x1l = 20*log10(fs*abs(x1));
x2l = 20*log10(fs*abs(x2));
x1p = 180*angle(fs*x1)/pi;
x2p = 180*angle(fs*x2)/pi;

xl = 20*log10(fs*(x1 + x2));
xp = 180*angle(fs*(x1 + x2))/pi;

subplot(4,1,1)
semilogx(f, x1l, f, x2l)
subplot(4,1,2)
semilogx(f, x1l)
subplot(4,1,3)
semilogx(f, x1p, f, x2p)
subplot(4,1,4)
semilogx(f, xp)