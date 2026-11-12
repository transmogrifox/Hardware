# Impulse Response Model for Switched Inductor Converters — Technical Audit & Rewrite Context Log

**Authors:** Ryan J. Billing, Joseph Amodemo (Schweitzer Engineering Laboratories)  
**Purpose:** Complete technical reference, error log, mathematical derivations, and structural roadmap for rewriting and completing the manuscript.

---

## 1. Core Thesis, Pedagogical Philosophy & Positioning

* **Primary Goal (Understandability Over Complexity):** The paper's primary objective is **not** simply to introduce yet another complex SMPS model, but to break the traditional trade-off between **high-frequency accuracy** and **practical, intuitive application**. The framework keeps the math anchored directly to **pulse geometry** and **basic discrete-time DSP / sampling theory**.
* **Two-Tier Modeling Architecture:**
  1. **The "Simple" Pedagogical Model (Feedback-Free Core):** By omitting slope-feedback terms ($\hat{m}_c, \hat{m}_d$), the core model reduces to a remarkably clean mathematical cascade (1st-order IIR $\rightarrow$ iZOH $\rightarrow$ 2-tap FIR $\rightarrow$ Pulse Reconstruction). New or less-experienced engineers can build immediate intuition for how current-mode control, sampling peaking, and the RHPZ/LHPZ work without wrestling with state-space matrices or circuit averaging tricks.
  2. **The "Full" Validated Model (Credibility & Hardware Parity):** Adding the intrinsic converter output impedance $Z_{out,conv}(s)$ (which captures $\hat{m}_d$ slope feedback) demonstrates complete mathematical consistency with established literature (Erickson/Maksimović, Ridley, Basso) and reproduces measured Vector Network Analyzer (VNA) gain/phase plots—including high-frequency nulls—up to the Nyquist rate.
* **Overcoming Limitations of the 3-Terminal PWM Switch Model:**
  * Conventional averaged-switch models treat the switch network as a 3-terminal device that must be mentally and topologically re-oriented for every converter family (Buck, Boost, Buck-Boost, Flyback, Forward), which is notoriously unintuitive to learn and error-prone to apply.
  * By replacing the switch and inductor with **two separate behavioral current sources**—a charging cycle source ($i_{cg}$) and a discharging cycle source ($i_{dg}$) paired with an intrinsic parallel output impedance ($Z_{out,conv}$)—the **exact same equations and filter expressions apply universally across all common topologies**. Only the external port connections change.

---

## 2. Section-by-Section Audit of Original Draft

### Section IV-A: Valley Current IIR Derivation (Equations 1–4) — **VERIFIED**
* Equations (1)–(4) are mathematically sound and internally consistent.
* The discharging slope $m_d$ is consistently defined and treated as a **positive scalar magnitude** throughout Sections IV and V-A/B/C/D.

### Section IV-B: Z-Transform of Peak Current Controller (Equations 5–10) — **ERROR IDENTIFIED & FIXED**
* **The Error:** Equations (6)–(9) attempt to eliminate the constant term $-T_{SW}m_d$ by invoking $u[n-1] + u[-n] = 1$ and summing their Z-transforms to zero. While $u[n-1] + u[-n] = 1$ is valid in discrete time, their bilateral Z-transforms have **mutually exclusive Regions of Convergence (ROCs)**: $|z| > 1$ for $u[n-1]$ and $|z| < 1$ for $u[-n]$. Summing them divides by zero at the DC bin ($z = 1$) and falsely implies a constant sequence has zero Z-transform.
* **Academically Accepted Fix:** Remove Table I and Equations (6)–(9). Invoke **superposition** (or small-signal perturbation around the steady-state DC operating point $I_{v\infty}, I_{c\infty}$) directly on the affine difference equation in (3). Because $-T_{SW}m_d$ is a constant offset independent of the perturbations $\hat{i}_c[n]$ and $\hat{i}_v[n]$, it balances the steady-state DC operating point and drops out of the small-signal Z-transform immediately:
  $$H_v(z) = \frac{\hat{I}_v(z)}{\hat{I}_c(z)} = \frac{\alpha z^{-1}}{1 - (1 - \alpha)z^{-1}}$$

### Sections IV-C to IV-F: Stability, Peaking & Inverse ZOH (Equations 11–22) — **MINOR TYPOS**
* **Equations (12), (20), (21):** Evaluation limit notation states $z = \frac{\omega_{SW}}{2}$ or $z = \frac{1}{2}\omega_{SW}$. Should be $\omega = \frac{\omega_{SW}}{2}$ (or $z = e^{j\pi} = -1$).
* **Page 5 Text (between Eqs. 15 & 16):** States *"when $i_v[n] - i_v[n-1]$"* — missing $= 0$.
* **Equation (16):** Typo $T_{sSW}$ instead of $T_{SW}$.
* **Segue Clarification for $H_{IZOH}(s)$:** Clearly state *why* the artificial ZOH is used: in the physical comparator, $i_c(t)$ is naturally sampled at the turn-off instant $t_n + D T_{SW}$, which leads to a transcendental equation for arbitrary perturbations. Sampling $i_c$ at the rising clock edge $t_n$ and holding it with a $T_{SW}$-wide boxcar linearizes the geometry (Eq. 2). Multiplying by $H_{IZOH}(s) = \frac{s}{1 - e^{-sT_{SW}}}$ deconvolves that artificial boxcar in the frequency domain. Note also that $H_{IZOH}(0) = \frac{1}{T_{SW}}$ (units of Hz), which cancels the $T_{SW}$ integration factor in the final continuous-time reconstruction stage.

### Sections V-A & V-B: Geometric Area & FIR Polynomial Coefficients (Equations 23–31) — **VERIFIED**
* All twelve quadratic/linear coefficients ($a_{cg} \dots f_{cg}$ in Eq. 27 and $a_{dg} \dots f_{dg}$ in Eq. 31) are **100% algebraically exact**.
* Equation (28) is valid because the text explicitly defines a time-reversed integration axis starting from $i_0$ at the end of discharge back to the peak.

### Section V-C: Small-Signal Linearization of FIR Filters (Equations 32–48) — **VERIFIED**
* Partial derivatives $k_0 = 2a i_{v\infty} + c i_{v\infty} + d$ and $k_1 = 2b i_{v\infty} + c i_{v\infty} + e$ in Equation (45) are **100% exact**.

### Section V-D: Continuous-Time RHPZ & LHPZ Limits (Equations 49–86) — **TYPESETTING TYPO FIXED**
* **Copy-Paste Typo in Eqs. (52)–(54) and (68)–(69):** When transitioning from Eq. (51) to Eq. (52), an extraneous $i_{v\infty}$ factor was accidentally multiplied into the non-derivative terms ($m_c^2 \mathbf{i_{v\infty}} \hat{i}_v(t) + m_c m_d \mathbf{i_{v\infty}} \hat{i}_v(t - T_{SW})$) and carried into (53)–(54). The same typo appears in Eqs. (68)–(69) ($+ m_d(m_c + m_d)\mathbf{i_{v\infty}}\hat{i}_v(t)$). Both Eqs. (55) and (70) self-correct upon factoring, so all final RHPZ and LHPZ equations (55–86) are completely valid. Simply delete the extraneous $i_{v\infty}$ from Eqs. (52)–(54) and (68)–(69).
* **Pedagogical Note on $i_{v\infty}$ as $T_{SW} \to 0$:** Explicitly note in Eqs. (53)–(55) that as $T_{SW} \to 0$, inductor current ripple $\Delta I_L \to 0$, so $i_{v\infty} \to I_L$ (the midpoint average inductor current), directly connecting the discrete geometry to state-space averaging.

### Section V-E: Discrete-to-Continuous Reconstruction (Equations 87–88) — **MAJOR REVISION REQUIRED**
* **Errors in Original Draft:**
  1. Equation (87) has a missing $s$ in the first exponential: $e^{-t_c}$ instead of $e^{-st_c}$.
  2. Equation (88) has an incorrect upper integration limit ($T_{SW} + t_d$ instead of $T_{SW}$) and an unshifted time variable $t$ inside $(i_{v\infty} + m_d t_d - m_d t)$ while integrating from $t_c$ to $T_{SW}$.
  3. **Conceptual Issue:** Equations (87)–(88) take the Laplace transform of the *full steady-state waveform pulse* rather than the *small-signal perturbation pulse*, and omit normalization by the cycle-averaged perturbation.

---

## 3. Corrected Closed-Form VNA Reconstruction Kernels & ZOH Equivalence

To reproduce VNA measurements (including high-frequency phase lag and switching nulls) without taking $T_{SW} \to 0$, keep the discrete IIR + iZOH + FIR cascade intact and cascade it with the Laplace transform of the **small-signal differential current pulse**, normalized by the discrete FIR output:

$$H_{VNA}(s) = H_v(e^{sT_{SW}}) \cdot H_{IZOH}(s) \cdot H_{FIR}(e^{sT_{SW}}) \cdot H_{rec}(s)$$

### Perturbation Geometry
When valley currents perturb by $\hat{i}_v[n-1]$ and $\hat{i}_v[n]$, the turn-off boundary $t_c = D T_{SW}$ shifts by:
$$\hat{t}_c = \frac{\hat{i}_v[n] - \hat{i}_v[n-1]}{m_c + m_d}$$
with steady-state peak current $i_{pk} = i_{v\infty} + m_c t_c = i_{v\infty} + m_d t_d$.

### Closed-Form Charging Kernel $H_{rec,cg}(s)$
Consists of a vertical shift $\hat{i}_v[n-1]$ over $[0, t_c]$ plus a width-modulation sliver of area $i_{pk}\hat{t}_c$ at $t = t_c$:
$$H_{rec,cg}(s) = \frac{\left(\frac{i_{pk}}{m_c + m_d}\right)e^{-st_c}\left(1 - e^{-sT_{SW}}\right) + \left(\frac{1 - e^{-st_c}}{s}\right)e^{-sT_{SW}}}{k_{0cg} + k_{1cg}e^{-sT_{SW}}}$$

### Closed-Form Discharging Kernel $H_{rec,dg}(s)$
Consists of a vertical shift $\hat{i}_v[n]$ over $[t_c, T_{SW}]$ minus a width-modulation sliver of area $i_{pk}\hat{t}_c$ at $t = t_c$:
$$H_{rec,dg}(s) = \frac{\left(\frac{e^{-st_c} - e^{-sT_{SW}}}{s}\right) - \left(\frac{i_{pk}}{m_c + m_d}\right)e^{-st_c}\left(1 - e^{-sT_{SW}}\right)}{k_{0dg} + k_{1dg}e^{-sT_{SW}}}$$

* **DC Gain Check:** Both kernels satisfy $H_{rec}(0) = T_{SW}$, which cancels $H_{IZOH}(0) = \frac{1}{T_{SW}}$ to yield exact unity DC gain while preserving high-frequency phase and VNA nulls.
* **Pedagogical Value of Retaining the FIR Stage:** Even though $H_{FIR}(e^{sT_{SW}})$ cancels algebraically against the denominator of $H_{rec}(s)$, keeping it as an explicit block is valuable because it exposes the discrete-time geometric origin of the RHPZ/LHPZ and aligns with behavioral circuit modeling.

### Equivalence Between ZOH Reconstruction and Ridley / Basso CPM Models
* **Why Convolving with a ZOH Matches Basso's Model:** In Ridley/Basso's continuous-time CPM framework, the feedback sampling gain is $H_e(s) = \frac{s T_{SW}}{e^{s T_{SW}} - 1} = T_{SW} e^{-s T_{SW}} H_{IZOH}(s)$, yielding the closed-loop control-to-inductor-current transfer function:
  $$\frac{\hat{i}_L(s)}{\hat{i}_c(s)} = \left(\frac{\alpha}{1 - (1 - \alpha)e^{-s T_{SW}}}\right) \cdot \left(\frac{1 - e^{-s T_{SW}}}{s T_{SW}}\right)$$
  Convolving the deconvolved controller $H_v(e^{s T_{SW}}) \cdot H_{IZOH}(s)$ with a standard ZOH $\frac{1 - e^{-s T_{SW}}}{s}$ cancels $H_{IZOH}(s)$ and reproduces Basso's exact continuous-time CPM expression.
* **Exactness in Buck vs. Approximation in Flyback/Boost:**
  * Summing the exact charging and discharging kernels for a **Buck converter** ($\hat{I}_{cg,\text{cont}}(s) + \hat{I}_{dg,\text{cont}}(s)$) causes the pulse-width modulation slivers at $t_c$ to cancel identically, leaving $\left(\frac{1 - e^{-s T_{SW}}}{s}\right)e^{-s t_c}$—proving that a ZOH (with an intra-cycle delay $e^{-s t_c}$) is the **exact** reconstruction kernel for total Buck inductor current.
  * For **Flyback or Boost** converters (where only $i_{dg}$ reaches the output during $t \in [t_c, T_{SW}]$), using a full-period ZOH smears the $t_d$-wide discharge pulse across $T_{SW}$ (matching Basso's averaged-switch approximation), whereas $H_{rec,dg}(s)$ preserves the true pulse width $t_d$ and turn-off modulation to capture high-frequency phase lag and VNA nulls.

---

## 4. Extending to the "Full" Model: Source- & Load-Independent Output Impedance $Z_{out,conv}(s)$

To capture the intrinsic small-signal feedback of terminal voltages on inductor slopes ($\hat{m}_c = \hat{v}_{cg}/L_m$, $\hat{m}_d = \hat{v}_{dg}/L_m$) without hardcoding specific source or load components:

1. **Perturbed Discrete Valley Equation:**
   $$\hat{i}_v[n] = \alpha \hat{i}_c[n-1] + (1 - \alpha)\hat{i}_v[n-1] + \beta_c \hat{m}_c[n-1] - \beta_d \hat{m}_d[n-1]$$
   where $\beta_c = D T_{SW}(1 - \alpha)$ and $\beta_d = T_{SW}(D' + \alpha D)$.
2. **Intrinsic Norton Output Impedance $Z_{out,conv}(s)$:**
   Treating $\hat{V}_{dg}(s)$ as an independent port perturbation defines a source- and load-independent Norton admittance $Y_{out,conv}(s) = \frac{1}{Z_{out,conv}(s)} = -\left.\frac{\partial \hat{I}_{dg}(s)}{\partial \hat{V}_{dg}(s)}\right|_{\hat{I}_c=0, \hat{V}_{cg}=0}$ placed directly in parallel with the $i_{dg}$ current source in Fig. 1:
   $$\hat{I}_{dg}(s) = G_{di}(s)\hat{I}_c(s) - \frac{1}{Z_{out,conv}(s)}\hat{V}_{dg}(s)$$
3. **Closed-Loop Control-to-Output for Any Arbitrary Load $Z_L(s)$:**
   $$\frac{\hat{V}_{out}(s)}{\hat{I}_c(s)} = G_{di}(s) \cdot \left(Z_{out,conv}(s) \parallel Z_L(s)\right)$$
   This fulfills the assertion on Page 12 of the original draft, reproduces Erickson's low-frequency damping resistance $R_e$ as $s \to 0$, and keeps the switched-inductor cell completely decoupled from external circuitry.

---

## 5. Draft Literature Review & Positioning Paragraph (Ready for Section I / II)

> **Draft Text for Manuscript:**
> *"Existing high-frequency modeling frameworks for current-mode converters generally navigate a trade-off between mathematical complexity and circuit intuition. Sampled-data circuit-averaging methods, pioneered by Ridley [ref] and Tan and Middlebrook [ref] (and widely implemented in SPICE behavioral templates by Basso [ref]), map discrete-time modulator sampling into the continuous frequency domain using a second-order Padé approximation ($H_e(s)$) paired with a Zero-Order-Hold reconstruction and a three-terminal averaged switch. While effective for standard loop compensation, re-orienting the three-terminal switch across diverse topologies (such as buck, boost, flyback, and forward) is often unintuitive for engineers learning small-signal modeling, and the continuous-time Padé and ZOH approximations lose phase accuracy near the Nyquist rate when intra-cycle discharge pulse shaping dominates. Conversely, exact sampled-data state-space formulations by Brown and Middlebrook [ref] and Verghese et al. [ref], as well as multifrequency describing-function models by Jian Li and Fred C. Lee [ref], accurately predict high-frequency phase lag and variable-frequency behavior, but rely on matrix exponentials or Fourier-Bessel sideband expansions that obscure simple geometric intuition. The impulse-response framework presented in this paper bridges this gap by prioritizing physical understandability grounded directly in pulse geometry and elementary sampling theory. By separating the power stage into universal charging ($i_{cg}$) and discharging ($i_{dg}$) behavioral current sources, a single, topology-agnostic cascade of basic discrete-time filters (IIR and FIR) and pulse-shaping reconstruction kernels applies uniformly across converter topologies—providing an accessible, feedback-free pedagogical model for rapid intuition while extending naturally via a parallel Norton output impedance ($Z_{out,conv}$) to match established models and measured VNA frequency responses up to the Nyquist rate."*

---

## 6. Recommended Manuscript Structure & Next Steps

1. **Section I (Introduction):** Frame the accuracy-vs.-understandability trade-off and insert the Literature Review paragraph above.
2. **Section II (Unified Behavioral Topology):** Present Fig. 1 as a universal template ($i_{cg}$ and $i_{dg}$ sources + optional parallel $Z_{out,conv}$).
3. **Section III (The "Simple" Model):** Present the clean, feedback-free cascade ($H_v(z)$ via superposition $\rightarrow$ $H_{IZOH}(s)$ $\rightarrow$ FIR filters $\rightarrow$ ZOH approximation vs. exact small-signal $H_{rec}(s)$ kernels).
4. **Section IV (Classical Equivalence & $T_{SW} \to 0$ Limit):** Show how the FIR stage geometrically explains the RHPZ, LHPZ, and their cancellation in Buck converters (with the Eq. 52/68 $i_{v\infty}$ typos fixed).
5. **Section V (The "Full" Model & Experimental VNA Validation):** Derive $Z_{out,conv}(s)$, verify low-frequency damping parity with Erickson/Basso, and add the measured fixed-frequency flyback VNA plots comparing the Simple Model, Full Model, Conventional Averaged Model, and Hardware Data.
6. **Section VI (Conclusion & References):** Replace placeholder citations (`[ref]`, `Reference 1`) and draft the final summary.
