k = 1000;
u = 1e-6;

fsw = 130*k
Ts = 1/fsw;

ff = 10:10:fsw;
ws = 2*pi*ff;
w0 = 2*pi*fsw;
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

hs = Ts*s./((1-e.^(-s*Ts)));
w0 = 0.5*(w0 + w0/2.14)
haprx = (e.^(s*0.65*Ts)).*w0*w0./(s.*s+s.*w0./(2) + (w0*w0) );
xx = length(hs)-1
xx2 = length(hs)/2 
ix = hs;
for ix=(1:6499)
  tmp = hs(xx2 - ix);
  hs(ix+xx2) = tmp;
end
tmp = hs(1)
hs(12999) = tmp;
hs(13000) = tmp;

subplot(2,1,1)
semilogx(ff, 20*log10(abs(hs)),"r", ff, 20*log10(abs(haprx)),"g")
subplot(2,1,2)
semilogx(ff, 180*unwrap(angle(hs))/pi, "m",ff, 180*unwrap(angle(haprx))/pi, "g")
