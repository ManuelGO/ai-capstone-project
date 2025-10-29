# 🧠 Black-Box Optimization (BBO) — Capstone Project

## 1) Project Overview
The **BBO Capstone** is an iterative ML challenge to optimize **eight unknown (“black-box”) functions** with **one query per function per week**. You never see the equations—only inputs → output pairs.  
This mimics real-world tasks like **hyperparameter tuning**, **chemical yield optimization**, or **control**, where evaluations are expensive and uncertainty matters.

**Why it’s relevant:** it trains a repeatable workflow—plan, model, query, reflect—that generalizes to data-science problems with **limited information**.

**Career value:** shows proficiency in **Bayesian optimization**, **experimental design**, **documentation**, and **reproducibility**.

---

## 2) Inputs and Outputs
- **Inputs:** vectors **x ∈ [0,1]^d** (d varies by function).  
  - F1–F2: 2D, F3: 3D, F4–F5: 4D, F6: 5D, F7: 6D, F8: 8D.
  - **Submission format:** `x1 - x2 - … - xd` with six decimals (e.g., `0.123456 - 0.654321`).
- **Output:** a single scalar **y** (the performance signal).
- **Objective:** **maximize** y for all eight functions.

**Example**
Input (F2):  0.684763 - 0.992806  
Output:      0.6397916079538416
---

## 3) Challenge Objectives & Constraints
- **Goal:** find high-performing inputs with **few evaluations**.
- **Constraints:**  
  - 1 query/function/week; outputs returned later.  
  - Black-box (no gradients or closed form).  
  - Surfaces can be noisy, non-linear, multi-modal.  
- **Success criteria:** not only higher y, but **clear, data-driven reasoning** and iterative refinement.

---

## 4) Technical Approach (living section)
### Surrogate modelling
- **Primary:** **Gaussian Process (GP)** with **Matern(ν=2.5)** + **ConstantKernel** (amplitude) + **WhiteKernel** (noise).  
- **Preprocessing:** **StandardScaler** on X; log-transform on y when scale is extreme (e.g., F5).  
- **Uncertainty:** use GP predictive mean (μ) and std (σ) to guide acquisition.

### Acquisition & candidate generation
- **Expected Improvement (EI)** as default; **UCB** and **MaxVar** as fallbacks if EI is flat.  
- **Trust Regions (TR):** center on the **best observed point**; typical mix **70–80% TR / 20–30% global**.  
- **Sampling:** **Latin Hypercube Sampling (LHS)** to generate diverse candidates; anti-edge and anti-duplicate filters.

### Exploration ↔ Exploitation
- Early rounds: higher **ξ** (e.g., 0.05–0.10) + wider TR for **exploration**.  
- Current rounds: lower **ξ** (≈ 0.02) for **refinement**, still keeping 20–40% global sampling in higher-D (F7–F8).

### Function-specific notes (Week 3 snapshot)
- **Improved:** **F2, F3, F4, F7, F8** → stable upward trend; refinement with small ξ and TR.  
- **Challenging:** **F5, F6** → noisier/irregular; keep some global sampling, TR broader; log1p(y) in F5.  
- **F1:** re-balanced toward exploration after weak outcomes; larger ξ and relaxed TR.

### Optional classification view (SVMs)
- With more data, a **soft-margin / kernel SVM** could separate “high vs low y” regions for interpretability.  
  Useful as a complementary diagnostic; GPs remain primary for uncertainty-aware search.

---

## 5) Repository Structure

The repository is organised to keep data, notebooks, and results clearly separated for transparency and reproducibility:
```
📁 capstone-bbo/
┣ 📂 initial_data/              # Provided base datasets (F1–F8: initial_inputs.npy, initial_outputs.npy)
┣ 📂 notebooks/                 # One Jupyter notebook per function
│   ┣ function_1.ipynb
│   ┣ function_2.ipynb
│   ┣ …
│   ┗ function_8.ipynb
┣ 📂 suggestions/               # CSV files with suggested query points per week
┣ 📂 figures/                   # Optional: generated visualizations (e.g. EI maps, projections)
┣ 📜 reflections.md             # Weekly reflections and learning notes
┣ 📜 README.md                  # Main project documentation (this file)
┗ 📜 requirements.txt           # Dependencies for reproducibility
```
---

## 6) Reproducible Workflow (per week)
1. **Load** initial + weekly (x,y). Guardar `X_prev, y_prev`.  
2. **Fit** GP (scaled X; adjust noise/length scales).  
3. **Generate** candidates (LHS: TR + global).  
4. **Score** with EI (ξ adaptive). Fallback: UCB → MaxVar.  
5. **Filter** (anti-edge, anti-duplicate) and **select** top-1 for submission.  
6. **Log** rationale, plots y μ/σ maps or pair projections. Commit notebooks + CSV.

---

## 7) Current Progress (Week 3 — brief)
- **Submissions:**  
  - F2: `0.966811 - 0.862665`  
  - F3: `0.250686 - 0.415794 - 0.535793`  
  - F4: `0.399923 - 0.481496 - 0.417614 - 0.455103`  
  - F5: `0.487939 - 0.756981 - 0.713439 - 0.929657`  
  - F6: `0.519632 - 0.356784 - 0.660361 - 0.981270 - 0.172574`  
  - F7: `0.087739 - 0.209465 - 0.209361 - 0.156530 - 0.372774 - 0.896630`  
  - F8: `0.105756 - 0.116724 - 0.211116 - 0.162702 - 0.690885 - 0.574863 - 0.206488 - 0.351411`  
  - F1: `0.765363 - 0.899441`
- **Trend:** Up in **F2, F3, F4, F7, F8**; mixed in **F5, F6**; F1 under review (more exploration).

---

*Author: Manuel Gonzalez Arvelo*  
*Programme: BBO Capstone — Stage 2 (Weeks 1–3). This README will evolve as the project progresses.*
