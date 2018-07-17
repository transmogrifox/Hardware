% Define multiplier constants
k=1000;
n=1e-9;
u=1e-6;

% Simulation parameters
dp=2*pi;
f=100:1:10000;
w=dp*f;
s=j.*w;

% Specify number of output traces to generate
ntrace = 4

% Gain of first-stage BJT amplifier
gf = -32
gv =  0

% Circuit parameters
Cf = 10*n
Ci = 10*n
Rp = 33*k
Lp = 0.5
Ri = 68*k
Rf = 1.5*k

%  Simplified approximate expression
for gv = 0:(1/ntrace):1
    Zi = Ri + 1./(s*Ci);
    %abpf = Rf./(Rf + Zi);
    %Ggv = 1 - gf*gv.*Zi./(Zi+Rf);
    %H1pHP = gf*abpf./Ggv;% Un-expanded to check my math
        
    %With 1P HPF out of the way, add approximations
    Ggv = 1 - gf*gv.*Ri./(Ri+Rf); % Assume XCin << Rin at resonance
    
    % First order high-pass term on the front-end
    H1pHP = gf.*(s.*Rf./(Rf + Ri.*(1 - gf.*gv))) ./ (s + 1./(Ci*Ri));

    % Biquad numerator
    Hnx = s.*s + s.*( 1./(Rp*Cf) + 1./(Rf*Cf) ) + 1./(Lp*Cf);
    % Biquad denominator
    Hdx = s.*s + s.*((1./(Rp.*Cf.*Ggv)).*(1 + Rp./(Zi + Rf)) ) + 1./(Lp.*Cf.*Ggv);
    
    % Final combined filter response
    Hds = H1pHP.*(Hnx./Hdx);
    semilogx(f, 20*log10(abs(Hds)),"g" )
    %semilogx(f, 20*log10(abs(H1pHP)),"g" )
    hold on
endfor
%hold off

% Check against derived expression
for gv = 0:(1/ntrace):1
    Zi = Ri + 1./(s*Ci);
    Ggv = 1 - gf*gv.*Zi./(Zi+Rf);
    
    %abpf = Rf./(Rf + Zi);
    %ahpf = Zi./(Rf + Zi);    
    %H1pHP = abpf.*gf./(1 - gf.*gv.*ahpf); % Un-expanded to check my math
    
    % First order high-pass term on the front-end
    H1pHP = gf.*(s.*Rf./(Rf + Ri.*(1 - gf.*gv))) ./ (s + 1./(Ci.*(Ri + Rf./(1 - gf.*gv))));
    % Biquad numerator
    Hnx = s.*s + s.*( 1./(Rp*Cf) + 1./(Rf*Cf) ) + 1./(Lp*Cf);
    % Biquad denominator
    Hdx = s.*s + s.*((1./(Rp.*Cf.*Ggv)).*(1 + Rp./(Zi + Rf)) ) + 1./(Lp.*Cf.*Ggv);
    
    % Final combined filter response
    Hds = H1pHP.*(Hnx./Hdx);
    semilogx(f, 20*log10(abs(Hds)),"r" )
    
    % Optional plot 1-Pole high pass filter responses to compare
    %semilogx(f, 20*log10(abs(H1pHP)),"r" )
    hold on
endfor

hold off



