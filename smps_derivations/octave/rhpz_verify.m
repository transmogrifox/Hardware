k = 1000;
u = 1e-6;

fsw = 130*k
Ts = 1/fsw;

ff = 10:10:fsw*5;
ws = 2*pi*ff;
s = j*ws;
z1 = e.^(-s*Ts);

hizoh = Ts*s./((1-e.^(-s*Ts)));

Lm = 230*u
Vin = 18.75
Vout = 5.25
Nsp = 4

Vcg = Vin             % Inductor charging voltage
Vdg = Nsp*Vout        % Inductor discharging voltage
D = Vdg/(Vcg + Vdg)

iv = 7.5

mc = Vcg/Lm
md = Vdg/Lm

%% Charging current coefficients
acg = (1/(2*Ts)) * mc/(mc^2 + 2*mc*md + md^2)
bcg = (-1/(2*Ts)) * ((2*md + mc)/(mc^2 + 2*mc*md + md^2))
ccg = (1/(Ts)) * (md/(mc^2 + 2*mc*md + md^2) )
dcg = mc*md/(mc^2 + 2*mc*md + md^2)
ecg = md^2/(mc^2 + 2*mc*md + md^2)
fcg = (Ts/2)*mc*md^2/(mc^2 + 2*mc*md + md^2)

%% Discharging current coefficients
adg = (-1/(2*Ts)) * (2*mc + md)/(mc^2 + 2*mc*md + md^2)
bdg = (1/(2*Ts)) * (md/(mc^2 + 2*mc*md + md^2))
cdg = (1/Ts) * (mc/(mc^2 + 2*mc*md + md^2) )
ddg = mc^2/(mc^2 + 2*mc*md + md^2)
edg = mc*md/(mc^2 + 2*mc*md + md^2)
fdg = (Ts/2) * (md*mc^2/(mc^2 + 2*mc*md + md^2)) 

Icg = (acg + bcg + ccg)*iv*iv + (dcg + ecg)*iv + fcg
Idg = (adg + bdg + cdg)*iv*iv + (ddg + edg)*iv + fdg

%% Final charging current FIR coefficients 
kcg0 = 2*acg*iv + ccg*iv + dcg 
kcg1 = 2*bcg*iv + ccg*iv + ecg

%% Final discharging current FIR coefficients 
kdg0 = 2*adg*iv + cdg*iv + ddg 
kdg1 = 2*bdg*iv + cdg*iv + edg

%% Conventional Right-Half Plane Zero (RHPZ) computation
Pout = Idg*Vdg  % For a flyback
Rl = Vdg*Vdg/Pout
Dp2 = (1-D)*(1-D)
%Dp2 = D*D  %% Hacks to represent it as charge zero or discharge zero
%D = 1-D
frhpz = Rl*Dp2/(2*pi*Lm*D)
wrhpz = 2*pi*frhpz

%% Discharging current transfer function
hz = (1./(kdg0 + kdg1)) .* (kdg0 + kdg1*z1);
hcg = (1./(kcg0 + kcg1)) .* (kcg0 + kcg1*z1);
hs = (1/wrhpz)*(s - wrhpz);
%hz = A0 + A1*z1;

%% Sanity checks. Product of voltages and currents
%% should be equal
Pout = Idg*Vdg 
Pin = Icg*Vcg


%semilogx(ff, 20*log10(abs(hz)), 'b', ff, 20*log10(abs(hcg.*hizoh)), 'g', ff, 20*log10(abs(hz.*hizoh)), 'm', ff, 20*log10(abs(hs)), 'r' )
subplot(4,1,1)
semilogx(ff, 20*log10(abs(hz.*hizoh)), 'b', ff, 20*log10(abs(hcg.*hizoh)), 'g')
subplot(4,1,2)
semilogx(ff,  (180/pi)*angle(hz.*hizoh), 'b', ff, (180/pi)*angle(hcg.*hizoh), 'g' )
subplot(4,1,3)
semilogx(ff, 20*log10(abs((hz + hcg).*hizoh)), 'r')
subplot(4,1,4)
semilogx(ff, (180/pi)*angle((hz + hcg).*hizoh), 'r' )


