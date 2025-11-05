# 🧠 Black-Box Optimization (BBO) — Capstone Project

## 1️⃣ Project Overview
The **BBO Capstone** is an iterative ML challenge to optimize **eight unknown ("black-box") functions** with **one query per function per week**.  
You never see the equations—only inputs → output pairs.  

This mimics real-world tasks like **hyperparameter tuning**, **chemical yield optimization**, or **experimental control**, where evaluations are expensive and uncertainty matters.

**Relevance:** it trains a repeatable workflow — *plan → model → query → reflect* — that generalizes to data-science problems with **limited information**.

**Career value:** demonstrates mastery of **Bayesian Optimization**, **experimental design**, **documentation**, and **reproducibility**.

---

## 2) Inputs and Outputs
- **Inputs:** vectors **x ∈ [0,1]^d** (d varies per function).  
  - F1-F2: 2D, F3: 3D, F4-F5: 4D, F6: 5D, F7: 6D, F8: 8D.  
  - **Submission format:** `x1 - x2 - … - xd` (six decimals).  
- **Output:** a scalar **y**, to be **maximized**.  
- **Example:**
Input (F2):  0.684763 - 0.992806  
Output:      0.6397916079538416

---

## 3) Challenge Objectives & Constraints
- **Goal:** maximize y with *few evaluations*.  
- **Constraints:**
- 1 query/function/week.
- Black-box, no gradients or analytic form.
- Noisy, non-linear, possibly multi-modal landscapes.
- **Success =** improved y **and** clear, data-driven reasoning and iterative refinement.

---

## 4) Technical Approach
### Surrogate Modelling
- **Model:** Gaussian Process (GP)  
- **Kernel:** Matern (ν=2.5) × Constant + WhiteKernel (noise).  
- **Scaling:** StandardScaler on X; log1p(y) for large-scale responses (e.g., F5).  
- **Uncertainty:** use GP predictive mean (μ) and std (σ) to guide next queries.  

### Acquisition & Candidate Generation
- **Expected Improvement (EI)** as primary,  
**UCB** and **MaxVar** as fallbacks if EI plateaus.  
- **Trust Region (TR):** centered on current best point.  
Typical mix → 70-80 % TR / 20-30 % global.  
- **Sampling:** Latin Hypercube (LHS); anti-edge & anti-duplicate filtering.

### Exploration ↔ Exploitation
- **Early rounds:** higher ξ (0.05-0.10), wider TR → exploration.  
- **Current rounds:** ξ≈0.02, narrower TR → local refinement.  
- **Higher-D (F7-F8):** maintain 30-40 % global candidates.

### Function-specific remarks
| Function | Status / Strategy |
|-----------|------------------|
| F1 | Early convergence; widened TR for renewed exploration. |
| F2-F4 | Stable upward trend, refinement phase (low ξ). |
| F5 | Unimodal, high variance → `log1p(y)` stabilisation, small ξ=0.01. |
| F6 | Moderate noise → broader TR + ξ≈0.03. |
| F7 | Multimodal; increased exploration (ξ≈0.05, κ≈1.8). |
| F8 | 8D surface; balance 70 % TR / 30 % global, anti-edge filter active. |


### Optional classification view (SVMs)
- With more data, a **soft-margin / kernel SVM** could separate "high vs low y" regions for interpretability.  
  Useful as a complementary diagnostic; GPs remain primary for uncertainty-aware search.

---

## 5) Repository Structure

The repository is organised to keep data, notebooks, and results clearly separated for transparency and reproducibility:
```
📁 capstone-bbo/
├── README.md
├── requirements.txt
│
├── initial_data/
│   ├── function_1/initial_inputs.npy
│   ├── function_1/initial_outputs.npy
│   └── … (function_2-function_8)
│
├── exploration_notebooks/
│   ├── f01_exploration.ipynb
│   ├── f02_exploration.ipynb
│   └── … (f03-f08)
│
├── configs/                  # Per-function configuration (YAML)
│   ├── f01.yaml
│   ├── f02.yaml
│   ├── f03.yaml
│   └── … (f08.yaml)
│
├── src/                      # Planned modular codebase (in progress)
│   ├── init.py
│   ├── data.py               # Load inputs/outputs, append weeks
│   ├── gp.py                 # GP building & fitting utilities
│   ├── candidates.py         # LHS sampling & filtering
│   ├── acquisition.py        # EI, UCB, MaxVar functions
│   ├── trust_region.py       # Trust-region helpers
│   └── run_suggest.py        # CLI to run suggestions (under development)
│
├── suggestions/              # Saved candidate CSVs (by week)
└── figures/                  # Optional visualisations / plots
```
---

## 6) Modularisation Plan (work in progress)
We are progressively migrating recurring logic from the notebooks to reusable modules under `src/`.  
This transition will allow:
- Unified GP + acquisition handling across functions.
- Parameter tuning via `configs/*.yaml` instead of hard-coded notebook values.
- Consistent saving/logging behaviour (e.g., `suggestions/F5_w05.csv`).
- Easier experimentation (different kernels/acquisitions with a single config edit).

**Implementation strategy:**
- Maintain notebooks as the *authoritative reference* while testing module parity.
- Validate results function-by-function before fully automating.
- Ensure identical behaviour (same EI ranking, same candidates) before migration.

---

## 7) Reproducible Workflow (per function/week)
1. **Load data:** initial + weekly updates.  
2. **Fit GP:** scale X, set noise/length-scales.  
3. **Generate candidates:** LHS with TR + global sampling.  
4. **Score:** EI (ξ adaptive); fallback UCB → MaxVar.  
5. **Filter:** edge and duplicate removal.  
6. **Select:** best candidate → format → save as submission CSV.  
7. **Reflect:** summarise reasoning, trends, and next-week strategy.

---

## 8) Upcoming Additions
✅ `configs/` with YAML per function (parameterized strategy)  
✅ `requirements.txt` for reproducibility  
🔄 `src/` modular code scaffolding (to be filled progressively)  
🔜 `Makefile` or CLI wrapper for one-command weekly suggestions  
🔜 CI tests (Pytest or simple asserts) to validate numerical consistency  

## 9) Example Usage (future state)
```bash
# Once src/ modules are complete
python -m src.run_suggest --config configs/f05.yaml --week 5
```
**This command will automatically:**
-	Load data and configuration.
-	Fit the GP and evaluate EI/UCB.
-	Select the next query and write `suggestions/F5_w05.csv`.
---
## 10) Quick Setup Commands
To create the modular structure and placeholders:
```bash
# From project root
mkdir -p configs src suggestions figures

# Create empty placeholder files
touch src/__init__.py

# Example base configs
echo "# YAML config templates per function" > configs/README.txt
echo "# To be filled with per-function settings (xi, kappa, L, etc.)" >> configs/README.txt

# Requirements
cat > requirements.txt <<'EOF'
numpy>=1.24
scipy>=1.10
scikit-learn>=1.3
pandas>=2.0
matplotlib>=3.7
seaborn>=0.12
plotly>=5.15
pyyaml>=6.0
EOF

# Optional commit
git add .
git commit -m "Add modular structure (configs/, src/, suggestions/, figures/)"
```
---

## 11) Dependencies
**Main Python libraries (see `requirements.txt`):**
- `numpy`, `scipy`, `scikit-learn`
- `pandas`, `matplotlib`, `seaborn`, `plotly`
- `pyyaml` — for configuration management

## 12) Author:


*Author: Manuel Gonzalez Arvelo*  
*Imperial College London, Business School - Black-Box Optimization Capstone*
*Programme: BBO Capstone — Stage 2 (Weeks 1-5). This README will evolve as the project progresses.*
