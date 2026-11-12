# Context & Audit Log: Impulse Response Model for Switched Inductor Converters

**Authors:** Ryan J. Billing, Joseph Amodemo (Schweitzer Engineering Laboratories)  
**Purpose:** Comprehensive session log capturing mathematical audit findings, closed-form derivations, pedagogical framing, literature positioning, and structural blueprints for future AI-assisted writing and revision sessions.

---

## 1. Core Thesis & Pedagogical Philosophy

* **Primary Objective:** The goal of this paper is **not** merely to create a marginally more accurate small-signal model, but to create a **more understandable, geometrically intuitive model** grounded directly in **inductor pulse geometry and basic discrete-time sampling theory**.
* **Two-Tier Modeling Architecture:**
  1. **The "Simple" Model (Primary Pedagogical Tool):** By omitting slope-feedback terms ($\hat{m}_c, \hat{m}_d$), the model reduces to a straightforward, transparent cascade of basic DSP blocks (1st-order IIR filter $
ightarrow$ Inverse ZOH $
ightarrow$ 2-tap FIR filter $
ightarrow$ pulse-shaping kernel). This allows inexperienced or learning engineers to build deep physical intuition for how cycle-by-cycle current control works without getting lost in state-space matrix algebra.
  2. **The "Full" Model (Credibility & Hardware Validation):** Incorporating the slope-feedback terms via an intrinsic Norton output impedance $Z_{out,conv}(s)$ proves rigorous mathematical equivalence with established literature (Erickson/Maksimović, Middlebrook/Tan, Ridley/Basso) in the $T_{SW} 	o 0$ limit while accurately matching measured VNA gain, phase droop, and switching-frequency nulls up to the Nyquist rate.
* **Breaking the Accuracy vs. Intuitiveness Trade-Off:**
  * Conventional **Averaged Switch Models** rely on a 3-terminal PWM switch block that is unintuitive to learn and must be mentally re-oriented across different converter topologies.
  * Conventional **Exact Sampled-Data / Describing-Function Models** preserve high-frequency accuracy up to the Nyquist rate but require heavy matrix exponentials or Fourier/Bessel sideband expansions that obscure physical intuition.
  * **This Approach:** Replaces the switch and inductor with two separate behavioral current sources—charging ($i_{cg}$) and discharging ($i_{dg}$)—paired with a parallel output impedance $Z_{out,conv}(s)$. This makes every common topology (Buck, Boost, Buck-Boost, Isolated Flyback, Isolated Forward) visually obvious and allows engineers to apply the **exact same closed-form expressions** universally without memorizing topology-specific transfer function variants.

---

## 2. Section-by-Section Mathematical Audit

### Section IV-A: Control-to-Valley IIR Filter — **VERIFIED CORRECT**
* **Equations (1)–(4):** Algebraically sound and internally consistent.
* **Slope Convention:** $m_d$ is treated consistently as a **positive scalar magnitude** across Sections IV and V-A/B/C/D (e.g., $i_v[n] = i_v[n-1] + m_c D T_{SW} - m_d D' T_{SW}$).

### Section IV-B: Z-Transform of the Peak Current Controller — **ERROR IDENTIFIED & RESOLVED**
* **The Error (Equations 6–9 & Table I):** Using $u[n-1] + u[-n] = 1$ to claim $\mathcal{Z}\{T_{SW}m_d\} = 0$ is invalid because the Regions of Convergence (ROC) for $u[n-1]$ ($|z| > 1$) and $u[-n]$ ($|z| < 1$) are mutually exclusive ($	ext{ROC} = \emptyset$). Adding their closed-form rational expressions cancels the DC pole at $z = 1$ via an illegal division by zero.
* **The Fix:** Remove Table I and Equations (6)–(9). Invoke **superposition / small-signal perturbation** directly on the affine difference equation (3): decompose $i_v[n] = I_{v\infty} + \hat{i}_v[n]$ and $i_c[n] = I_{c\infty} + \hat{i}_c[n]$. The constant term $-T_{SW}m_d$ balances the DC operating point, leaving the strictly linear small-signal recurrence relation:
  $$\hat{i}_v[n] = lpha \hat{i}_c[n-1] + (1-lpha)\hat{i}_v[n-1] \implies H_v(z) = rac{\hat{I}_v(z)}{\hat{I}_c(z)} = rac{lpha z^{-1}}{1 - (1-lpha)z^{-1}}$$

### Section IV-C to IV-E: Stability & Magnitude Response — **MINOR TYPOS**
* **Page 5, line below Eq. (15):** Steady-state text reads $i_v[n] - i_v[n-1]$; change to $i_v[n] - i_v[n-1] = 0$.
* **Equation (16):** Typo $DT_{sSW}m_c$ should be $DT_{SW}m_c$.
* **Equations (12), (20), (21):** Evaluation subscripts read $z = rac{\omega_{SW}}{2}$ or $z = rac{1}{2}\omega_{SW}$; update to $\omega = rac{\omega_{SW}}{2}$ (or $z = e^{j\pi} = -1$).

### Section IV-F: Inverse Zero-Order-Hold ($H_{IZOH}$) — **CLARIFICATION & SCALING**
* **Physical Justification:** Sampling $i_c$ at the rising clock edge and holding it across $T_{SW}$ (artificial ZOH boxcar) avoids solving transcendental comparator trip-time equations. Multiplying by $H_{IZOH}(s) = rac{s}{1 - e^{-sT_{SW}}}$ deconvolves the artificial input boxcar.
* **Dimensional Scaling Note:** $H_{IZOH}(s)$ has a DC gain of $rac{1}{T_{SW}}$ (units of $	ext{Hz}$). This $rac{1}{T_{SW}}$ factor cancels with the $T_{SW}$ integration scaling in the final continuous-time pulse reconstruction kernel $H_{rec}(s)$, yielding exact unity DC gain ($H_{IZOH}(0)H_{rec}(0) = 1$).

### Section V-A & V-B: Geometric Area of Charging/Discharging Pulses — **VERIFIED CORRECT**
* **Equations (23)–(31):** Every algebraic step and all 12 quadratic polynomial coefficients ($a_{cg}\dots f_{cg}$ and $a_{dg}\dots f_{dg}$) are **100% correct**. Note that Equation (28) integrates backward in time from $i_0$, so $+m_d t$ is consistent with $m_d > 0$.

### Section V-C: Small-Signal Linearization ($k_0, k_1$) — **VERIFIED CORRECT**
* **Equations (36)–(48):** Partial derivatives $k_0 = 2a i_{v\infty} + c i_{v\infty} + d$ and $k_1 = 2b i_{v\infty} + c i_{v\infty} + e$ in Equation (45) are **100% correct**.

### Section V-D: Continuous-Time Limit ($T_{SW} 	o 0$) — **TYPESETTING TYPOS FIXED**
* **Copy-Paste Typo in Equations (52)–(54) & (68)–(69):** An extraneous factor of $i_{v\infty}$ was accidentally inserted into the non-derivative terms when transitioning from Eq. (51) to (52) ($+ m_c^2 i_{v\infty}\hat{i}_v(t) + m_c m_d i_{v\infty}\hat{i}_v(t-T_{SW})$) and from Eq. (67) to (68) ($+ m_d(m_c + m_d)i_{v\infty}\hat{i}_v(t)$). Equation (55) and Equation (70) self-corrected during factoring, so all final RHPZ and LHPZ expressions (Eqs. 55, 63, 70, 79, 80–86) are **exact**. Simply delete the extra $i_{v\infty}$ from Eqs. (52)–(54) and (68)–(69).
* **Limit Note on $i_{v\infty}$:** Clarify explicitly in Eqs. (53)/(55) and (59)–(60) that as $T_{SW} 	o 0$, the inductor ripple $\Delta I_L 	o 0$, so $i_{v\infty} = I_L - rac{\Delta I_L}{2} 	o I_L$ (the midpoint inductor current).

### Section V-E: Discrete-to-Continuous Reconstruction — **CRITICAL REVISION FOR VNA ACCURACY**
* **Errors in Original Equations (87)–(88):**
  1. Missing $s$ in exponent of Eq. (87): $e^{-t_c}$ should be $e^{-st_c}$.
  2. Wrong upper integration limit in Eq. (88): $\int_{t_c}^{T_{SW}+t_d}$ should be $\int_{t_c}^{T_{SW}}$, and the integrand $(i_{v\infty} + m_d t_d - m_d t)$ was not time-shifted by $(t - t_c)$.
  3. **Conceptual Error:** Equations (87)–(88) compute the Laplace transform of the *full steady-state waveform* rather than the *small-signal perturbation pulse*, and omit normalization by the cycle-averaged current.

---

## 3. Closed-Form Small-Signal VNA Reconstruction Kernels & ZOH Equivalence

To reproduce exact VNA gain, phase droop, and switching-frequency nulls without taking $T_{SW} 	o 0$, keep the discrete cascade intact ($z = e^{sT_{SW}}$) and apply the Laplace transform of the **small-signal differential current pulse** normalized by the discrete FIR output:

$$H_{VNA}(s) = H_v(e^{sT_{SW}}) \cdot H_{IZOH}(s) \cdot H_{FIR}(e^{sT_{SW}}) \cdot H_{rec}(s)$$

### A. Small-Signal Perturbation Geometry
When valley currents perturb by $\hat{i}_v[n-1]$ and $\hat{i}_v[n]$, the turn-off edge $t_c = D T_{SW}$ modulates by:
$$\hat{t}_c = rac{\hat{i}_v[n] - \hat{i}_v[n-1]}{m_c + m_d}, \qquad i_{pk} = i_{v\infty} + m_c t_c = i_{v\infty} + m_d t_d$$

### B. Charging Reconstruction Kernel $H_{rec,cg}(s)$
Consists of a vertical height shift $\hat{i}_v[n-1]$ over $[0, t_c]$ plus a width-modulation sliver of area $i_{pk}\hat{t}_c$ at $t = t_c$:
$$H_{rec,cg}(s) = rac{\left(rac{i_{pk}}{m_c + m_d}
ight)e^{-st_c}\left(1 - e^{-sT_{SW}}
ight) + \left(rac{1 - e^{-st_c}}{s}
ight)e^{-sT_{SW}}}{k_{0cg} + k_{1cg}e^{-sT_{SW}}}$$

### C. Discharging Reconstruction Kernel $H_{rec,dg}(s)$
Consists of a vertical height shift $\hat{i}_v[n]$ over $[t_c, T_{SW}]$ minus a width-modulation sliver of area $i_{pk}\hat{t}_c$ at $t = t_c$:
$$H_{rec,dg}(s) = rac{\left(rac{e^{-st_c} - e^{-sT_{SW}}}{s}
ight) - \left(rac{i_{pk}}{m_c + m_d}
ight)e^{-st_c}\left(1 - e^{-sT_{SW}}
ight)}{k_{0dg} + k_{1dg}e^{-sT_{SW}}}$$

* **Buck Cancellation Check:** Summing the numerators for Buck ($i_{cg} + i_{dg}$) cancels the $\pm \left(rac{i_{pk}}{m_c+m_d}
ight)e^{-st_c}$ terms identically, leaving a pure ZOH shifted by $t_c$: $\left(rac{1 - e^{-sT_{SW}}}{s}
ight)e^{-st_c}$.
* **ZOH Approximation Equivalence (Link to Ridley/Basso CPM Models):**
  * Convolving the deconvolved controller $H_v(e^{sT_{SW}}) \cdot H_{IZOH}(s)$ with a standard ZOH $\left(rac{1 - e^{-sT_{SW}}}{s}
ight)$ cancels $H_{IZOH}(s)$ and reproduces the classic Ridley/Basso continuous-time current-mode transfer function $rac{lpha}{1 - (1-lpha)e^{-sT_{SW}}} \cdot rac{1 - e^{-sT_{SW}}}{sT_{SW}}$ (up to a one-cycle sampling alignment shift).
  * This proves that **a standard ZOH is literally the implicit reconstruction approximation used in Basso/Ridley models**: it is exact for total Buck inductor current (omitting only the intra-cycle $e^{-st_c}$ delay), whereas for Flyback/Boost converters it smears the $t_d$-wide discharge pulse across the full period $T_{SW}$. Replacing the ZOH with $H_{rec,dg}(s)$ recovers the exact high-frequency phase lag and VNA nulls.

---

## 4. Intrinsic Converter Output Impedance ($Z_{out,conv}(s)$) & DCM Extension

### A. Source- and Load-Independent Norton Impedance (Full CCM Model)
To capture small-signal feedback from terminal voltage perturbations ($\hat{m}_c = \hat{v}_{cg}/L_m$, $\hat{m}_d = \hat{v}_{dg}/L_m$) without hardcoding external loads or sources:
* **Perturbed Valley Recurrence:**
  $$\hat{i}_v[n] = lpha \hat{i}_c[n-1] + (1-lpha)\hat{i}_v[n-1] + eta_c \hat{m}_c[n-1] - eta_d \hat{m}_d[n-1]$$
  where $eta_c = D T_{SW}(1 - lpha)$ and $eta_d = T_{SW}(D' + lpha D)$.
* **Norton Equivalent Circuit (Fig. 1):** Place an intrinsic output admittance $Y_{out,conv}(s) = rac{1}{Z_{out,conv}(s)} = -\left.rac{\partial \hat{I}_{dg}(s)}{\partial \hat{V}_{dg}(s)}
ight|_{\hat{I}_c=0, \hat{V}_{cg}=0}$ in parallel with the behavioral discharge source $i_{dg}$:
  $$\hat{I}_{dg}(s) = G_{di}(s)\hat{I}_c(s) - rac{1}{Z_{out,conv}(s)}\hat{V}_{dg}(s)$$
  For any arbitrary load impedance $Z_L(s)$, the control-to-output response is simply $rac{\hat{V}_{out}(s)}{\hat{I}_c(s)} = G_{di}(s)\left(Z_{out,conv}(s) \parallel Z_L(s)
ight)$, fulfilling the assertion on Page 12 of the draft.

### B. Extension to Discontinuous Conduction Mode (DCM)
* In DCM, the inductor current resets to zero every cycle ($i_v[n] = 0$), so the IIR valley filter collapses ($lpha = 0$ memory, no subharmonic oscillation).
* Charging and discharging waveforms become pure triangles ($t_c = rac{i_c[n-1]}{m_c + m_{cmp}}$, $t_d = rac{m_c}{m_d}t_c$, $i_{v\infty} = 0$), reducing the FIR stage to a single memoryless tap ($k_1 = 0$) and simplifying $H_{rec,cg}(s)$ and $H_{rec,dg}(s)$ to triangular pulse-width modulation kernels.

---

## 5. Literature Positioning & Draft Related Work Paragraph

### Comparison Matrix
* **Ridley (1991) / Tan & Middlebrook (1995) / Basso:** Sampled-data + continuous Padé approximation ($H_e(s)$) inside an averaged-switch circuit. Intuitive, but relies on 3-terminal switch re-orientation, approximates reconstruction as a ZOH, and loses phase/null accuracy near $rac{1}{2}F_{SW}$.
* **Brown & Middlebrook (1981) / Verghese et al. (1986):** Exact sampled-data state-transition matrices. Exact up to Nyquist, but mathematically opaque for new engineers.
* **Jian Li & Fred C. Lee (2009):** Multifrequency describing functions. Captures high-frequency phase and variable-frequency control, but requires complex Fourier/Bessel sideband math.
* **This Work:** Combines the **high-frequency Nyquist accuracy** of exact sampled-data/describing-function models with the **modular circuit intuition** of behavioral current sources—offering a progressive learning curve from a feedback-free "simple" geometric model to a full Norton-compensated model.

### Draft Literature Review Paragraph (Ready for Section I / II)
> *"Existing small-signal modeling frameworks for current-mode converters generally impose a trade-off between mathematical rigor and practical intuition. Classical circuit-averaging and PWM switch models [Erickson, Vorpérian] offer strong circuit-level intuition, yet they require engineers to mentally re-orient a three-terminal switch element across different converter topologies and inherently blur intra-cycle timing, failing to predict high-frequency phase droop above one-quarter of the switching frequency. To address sampling artifacts, Ridley [1991] and Tan and Middlebrook [1995] augmented averaged-switch models with continuous-time rational approximations ($H_e(s)$) of the current-loop sampler; however, these hybrid models implicitly approximate output current reconstruction as a full-period zero-order hold (ZOH), which misrepresents pulse-width-modulated discharge waveforms and degrades phase accuracy near the Nyquist rate. Conversely, exact sampled-data state-space methods [Verghese et al., 1986] and multifrequency describing-function frameworks [Li and Lee, 2009] accurately capture high-frequency phase and sideband behavior, but rely on state-transition matrix exponentials or Bessel-series expansions that obscure physical intuition for practicing engineers. This paper bridges that gap by prioritizing understandability grounded directly in inductor pulse geometry and elementary discrete-time filtering. By decomposing the switched inductor into separate charging ($i_{cg}$) and discharging ($i_{dg}$) behavioral current sources, the proposed approach establishes a unified, topology-agnostic representation that applies identical closed-form expressions across buck, boost, buck-boost, flyback, and forward converters. Omitting slope-feedback terms yields a transparent, feedback-free 'simple' model that enables new engineers to build intuition directly from waveform geometry, while incorporating slope feedback as an intrinsic parallel Norton impedance ($Z_{out,conv}$) recovers full parity with established small-signal models and accurately predicts measured VNA gain and phase nulls up to the Nyquist frequency."*

---

## 6. Finalized Document Architecture (Theory Paper + Companion Appendices/App Note)

To keep the main paper crisp, persuasive, and pedagogically focused while giving practicing engineers complete "plug-and-chug" usability, structure the work as follows (either as **Main Body + Appendices A–C** for a standalone journal/whitepaper, or **Main Body + Companion Application Note** if targeting a page-limited conference):

* **Main Body (Core Intuition, Theory & Benchmark Validation):**
  1. **Section I: Introduction & Motivation** — Frame the pedagogical goal, the accuracy vs. intuitiveness trade-off, and the literature review paragraph above.
  2. **Section II: Unified Behavioral Current-Source Topology** — Present Fig. 1 showing how $i_{cg}$, $i_{dg}$, and parallel $Z_{out,conv}(s)$ apply identically across all common topologies without 3-terminal switch re-orientation.
  3. **Section III: The "Simple" CCM Model (Core Discrete-to-Continuous Cascade)** — Derive the feedback-free cascade ($H_v(z)$ via superposition $
ightarrow$ $H_{IZOH}(s)$ $
ightarrow$ 2-tap geometric FIR $
ightarrow$ ZOH approximation vs. exact $H_{rec}(s)$ pulse-shaping kernels).
  4. **Section IV: Geometric Link to Classical Theory ($T_{SW} 	o 0$ Limit)** — Demonstrate how the 2-tap FIR filters expose the geometric origin of the RHPZ, LHPZ, and Buck zero cancellation.
  5. **Section V: The "Full" CCM Model & Experimental VNA Validation** — Introduce the source/load-independent Norton impedance $Z_{out,conv}(s)$ and present the **summary Bode plot comparison** (Simple Model vs. Full Model vs. Basso/Ridley vs. Measured Fixed-Frequency Flyback VNA data).
  6. **Section VI: Conclusion** — Replace placeholder text with a concise wrap-up of pedagogical and practical takeaways.

* **Appendices (or Companion Application Note):**
  * **Appendix A: "Meal Ready to Eat" (MRE) Model Summary** — Compact, copy-pasteable lookup tables of closed-form equations (CCM Simple, CCM Full with $Z_{out,conv}$, and DCM) ready to drop into Python, MATLAB, or Mathcad.
  * **Appendix B: Extension to Discontinuous Conduction Mode (DCM)** — Show how $i_v[n] = 0$ collapses the IIR/FIR stages into memoryless triangular pulse kernels.
  * **Appendix C: Experimental Flyback VNA Testbench & Worked Example** — Document the exact hardware parameters, current-sense resistor $R_s$, transformer turns ratio $N$, error amplifier, optocoupler/compensation network gains, and step-by-step calculation walkthrough.

---

## 7. Next Action Items for Future Sessions
1. **Derive Closed-Form DCM Equations & Build Appendix A (MRE Summary Table):** Write out the exact triangular DCM formulas and format the copy-pasteable equation tables for CCM Simple, CCM Full, and DCM.
2. **Draft Section I & Section VI:** Finalize the Introduction (integrating the literature review paragraph) and write a complete Conclusion replacing the draft placeholders.
3. **Compile Experimental Flyback Parameters (Appendix C / Section V):** Plug actual hardware values ($F_{SW}, L_m, N, V_{in}, V_{out}, R_{load}, R_s, m_{cmp}$, compensation network) into Python/MATLAB to generate the overlay plots comparing Simple Model, Full Model, Basso/Ridley, and VNA measurements.
