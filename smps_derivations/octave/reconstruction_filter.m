k = 1000;
u = 1e-6;

fsw = 100*k
Ts = 1/fsw;

ff = 10:10:5*fsw;
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

tc = D*Ts;
%hs = md*(Ts*Dp./s + 1./(s.*s)).*(e.^(-s*Ts) - e.^(-s*Ts*D)) + (mc*D + iv).*(e.^(-s*Ts.*D)).*(1 - e.^(-s*Ts*Dp))./s;

h1 = iv*(1 - e.^(-s*tc))./s;
h2 = mc*(1 - (1 + s*tc).*e.^(-s*tc))./(s.^2);

hs = h2;
g0 = 20*log10(abs(h1(1)))
g0lim =  20*log10(abs(iv*tc))

g1 = 20*log10(abs(h2(1)))
g1lim =  20*log10(abs((1/2)*mc*tc^2))

c0 = abs(h1(1))
c0lim = iv*tc
c1 = abs(h2(1))
c1lim = (mc*tc^2)/2

glim = 20*log10(fsw*(c0lim + c1lim))
g = 20*log10(fsw*(abs(h1(1) + h2(1))))

subplot(2,1,1)
semilogx(ff, 20*log10(abs(hs)),"r")
subplot(2,1,2)
semilogx(ff, 180*unwrap(angle(hs))/pi, "m")
