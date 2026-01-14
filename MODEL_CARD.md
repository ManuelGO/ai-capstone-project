# Model Card: Adaptive Bayesian Optimization for Black-Box Functions

## 1. Model Overview

| Field | Value |
|-------|-------|
| **Model name** | Adaptive GP-BO (Gaussian Process Bayesian Optimization) |
| **Version** | 1.0 (Week 10) |
| **Developer(s)** | Manuel Gonzalez Arvelo |
| **Contact** | GitHub: [ManuelGO/ai-capstone-project](https://github.com/ManuelGO/ai-capstone-project) |
| **Licence** | MIT (code), CC BY 4.0 (documentation) |

### Description
This optimization approach uses **Gaussian Process surrogate models** with **Expected Improvement (EI) acquisition** to sequentially optimize eight black-box functions. The strategy adapts per-function based on observed landscape characteristics, incorporating trust regions, constraint masks, and fallback acquisition functions.

---

## 2. Intended Use

| Field | Description |
|-------|-------------|
| **Primary task** | Sequential black-box optimization with limited query budgets |
| **Target users** | ML practitioners, researchers, students learning Bayesian Optimization |
| **Recommended use cases** | Hyperparameter tuning, experimental design, simulation optimization, chemical/industrial process optimization |
| **Not recommended for** | Real-time optimization (GP fitting is O(n³)), functions with >10D without modifications, adversarial/non-stationary environments |

### Suitable Scenarios
- Expensive function evaluations (minutes to hours per query)
- Smooth or moderately noisy objective functions
- Continuous input spaces in [0,1]^d
- Budget constraints (10-100 evaluations)

### Unsuitable Scenarios
- Discrete/categorical inputs (requires kernel modifications)
- Highly non-stationary functions
- Massively parallel evaluation settings
- Functions with hard discontinuities

---

## 3. Training Data

| Field | Description |
|-------|-------------|
| **Data sources** | Imperial College BBO Capstone: 8 synthetic black-box functions |
| **Size of dataset** | 170 initial points + 72 weekly queries = 242 total observations |
| **Languages/modalities** | Numerical vectors (X ∈ [0,1]^d) → scalar outputs (y ∈ ℝ) |
| **Preprocessing steps** | StandardScaler (X), log1p (y for F5), edge/duplicate filtering |

### Data Characteristics by Function

| Function | Dimensions | Initial Points | Characteristics |
|----------|------------|----------------|-----------------|
| F1-F2 | 2D | 10 each | Low-dimensional, smooth |
| F3 | 3D | 15 | Transition complexity |
| F4-F5 | 4D | 20 each | F5: Unimodal, large-scale outputs |
| F6 | 5D | 25 | Constrained (recipe optimization) |
| F7 | 6D | 30 | Multimodal, anisotropic |
| F8 | 8D | 40 | Plateau landscape |

---

## 4. Evaluation Metrics

| Field | Description |
|-------|-------------|
| **Metrics used** | Best observed y, improvement over baseline, GP prediction accuracy (μ vs actual) |
| **Performance results** | See summary table below |
| **Fairness/bias checks** | N/A (optimization task, no protected groups) |

### Performance Summary (Week 9)

| Function | Initial Best | Final Best (W9) | Improvement | Status |
|----------|--------------|-----------------|-------------|--------|
| F1 | ~0.25 | 0.298 | +19% | Suboptimal (constraint drift) |
| F2 | ~0.58 | ~0.64 | +10% | Stable |
| F3 | — | — | — | In progress |
| F4 | ~0.25 | 0.298 | +19% | Suboptimal (constraint drift) |
| F5 | 2625 | **4368** | **+66%** | **3 consecutive improvements** |
| F6 | -0.54 | -1.13 | -109% | **Disaster (W9)** - Fix applied |
| F7 | 1.43 | **1.952** | **+36%** | **New global best** |
| F8 | 9.06 | 9.957 | +10% | 2nd best (plateau) |

### GP Prediction Accuracy

| Function | Predicted μ | Actual y | Error |
|----------|-------------|----------|-------|
| F5 (W9) | 4402 | 4368 | 0.8% |
| F7 (W9) | ~1.95 | 1.952 | <1% |
| F8 (W9) | 9.974 | 9.957 | 0.2% |

---

## 5. Strategy Evolution (Weeks 1-10)

### Phase 1: Exploration (Weeks 1-3)
- **Objective:** Map landscape structure, identify promising regions
- **Settings:** Wide trust regions (L = 0.35-0.45), high exploration (ξ = 0.05-0.10)
- **Sampling:** 60-70% TR / 30-40% global
- **Key learnings:** Identified unimodal (F5), multimodal (F7), plateau (F8) structures

### Phase 2: Exploitation (Weeks 4-6)
- **Objective:** Refine around discovered optima
- **Settings:** Narrower TR (L = 0.20-0.30), lower exploration (ξ = 0.01-0.03)
- **Sampling:** 75-85% TR / 15-25% global
- **Key learnings:** F5 breakthrough (W4: 4289), F7 breakthrough (W6: 1.939)

### Phase 3: Constraint Discovery (Weeks 7-8)
- **Objective:** Understand hard constraints from failures
- **Discoveries:**
  - F5: x₃, x₄ ≥ 0.98 mandatory for high yield
  - F6: x₄ ≥ 0.90 (butter proportion) critical
  - F7: Anisotropic constraints based on kernel length_scales
- **Implementation:** Hard constraint masks in acquisition phase

### Phase 4: Ultra-Precision (Weeks 9-10)
- **Objective:** Final refinement with validated constraints
- **Settings:** Ultra-tight TR (L = 0.10-0.15), minimal exploration (ξ = 0.002-0.005)
- **Sampling:** 90-95% TR / 5-10% global + focused sampling (±0.3-0.5%)
- **Results:** F5 and F7 achieved new global bests; F8 validated plateau acceptance

### Technique Summary

| Technique | Purpose | Functions Applied |
|-----------|---------|-------------------|
| **Trust Region (TR)** | Local exploitation | All |
| **LHS Sampling** | Space-filling candidate generation | All |
| **EI Acquisition** | Balance exploration-exploitation | All (primary) |
| **UCB Fallback** | Handle EI degeneracy | All (fallback) |
| **MaxVar Fallback** | Uncertainty-driven exploration | All (fallback) |
| **log1p Transform** | Stabilize large-scale outputs | F5 |
| **StandardScaler** | Numerical stability | F6, F7, F8 |
| **Constraint Masks** | Enforce hard constraints | F4, F5, F6, F7 |
| **Anisotropic Bounds** | Dimension-specific constraints | F7 |
| **Focused Sampling** | Ultra-precise perturbations | F5, F7, F8 |
| **Plateau Acceptance** | Strategic consolidation | F8 |

---

## 6. Assumptions and Limitations

### Underlying Assumptions
1. **Smoothness:** Functions have continuous, differentiable structure (Matern kernel appropriate)
2. **Stationarity:** Function characteristics don't change over time
3. **Noise level:** Low to moderate noise (WhiteKernel handles observation noise)
4. **Unimodal prior:** EI assumes exploitation around global optimum is beneficial

### Known Limitations

| Limitation | Impact | Mitigation |
|------------|--------|------------|
| **Cubic scaling** | GP fitting is O(n³) | Limit to <500 observations per function |
| **High-D curse** | Performance degrades beyond 8D | Increase global sampling ratio |
| **Constraint discovery** | Hard constraints not known a priori | Empirical analysis of failures |
| **Local optima risk** | EI may exploit local, not global, optimum | UCB fallback, periodic exploration |
| **Plateau confusion** | GP struggles with flat regions | Plateau acceptance strategy (F8) |

### Failure Modes Observed

| Function | Week | Failure | Root Cause | Fix |
|----------|------|---------|------------|-----|
| F5 | W7 | y = 886 (-79%) | x₃, x₄ dropped below 0.98 | Hard constraint mask |
| F6 | W9 | y = -1.13 (worst) | x₄ = 0.35 (should be ≥0.90) | x₄ ≥ 0.90 constraint |
| F7 | W7 | y = 1.27 (-34%) | Moved too far from W6 optimum | Anisotropic constraints |
| F7 | W8 | y = 1.68 (-13%) | x₄ dropped 24% (uniform constraints) | Per-dimension bounds |

---

## 7. Ethical Considerations

| Field | Description |
|-------|-------------|
| **Potential biases** | Selection bias in query strategy; exploitation may miss global optima |
| **Mitigation strategies** | Maintain 10-30% global sampling; periodic exploration bursts |
| **Privacy concerns** | None (synthetic data, no PII) |

### Transparency and Reproducibility

This model card supports reproducibility through:
1. **Complete documentation:** All strategy decisions recorded in notebook reflections
2. **Version control:** Git history tracks weekly evolution
3. **Parameter logging:** TR width (L), exploration (ξ), sampling ratios documented
4. **Failure analysis:** Disasters analyzed and fixes documented (e.g., F6 W9)

### Real-World Adaptation Considerations

When adapting this approach to real-world problems:
- **Validate constraints:** Domain experts should verify discovered constraints (e.g., F5's chemical thresholds)
- **Budget allocation:** Real costs may justify different exploration-exploitation balance
- **Safety margins:** Industrial applications may require conservative constraint buffers
- **Human oversight:** Critical decisions should involve domain expert review

---

## 8. Model Life Cycle

| Field | Description |
|-------|-------------|
| **Date of last update** | Week 10 (January 2026) |
| **Version control** | GitHub: [ManuelGO/ai-capstone-project](https://github.com/ManuelGO/ai-capstone-project) |
| **Monitoring plan** | Weekly performance tracking; post-mortem analysis for failures |

### Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | W1-W3 | Initial exploration phase |
| 0.5 | W4-W6 | Exploitation refinement; F5/F7 breakthroughs |
| 0.8 | W7-W8 | Constraint discovery; failure analysis |
| 1.0 | W9-W10 | Ultra-precision; validated constraints |

### Future Improvements
- Automated constraint detection from failure patterns
- Multi-fidelity optimization for faster exploration
- Ensemble acquisition functions
- Transfer learning between similar functions

---

## 9. Additional Documentation

### Why This Structure is Sufficient

This model card provides comprehensive coverage because:

1. **Task-specific metrics:** Optimization improvement (%) is more meaningful than generic ML metrics
2. **Strategy evolution:** Week-by-week progression shows adaptive decision-making
3. **Failure documentation:** Honest reporting of disasters (F6 W9, F7 W7) enables learning
4. **Constraint discovery:** Domain-specific insights (chemical thresholds, recipe constraints) are captured
5. **Reproducibility:** All parameters and decisions are logged for replication

### Related Documents
- [DATASHEET.md](./DATASHEET.md) — Dataset documentation
- [README.md](./README.md) — Project overview
- `exploration_notebooks/` — Detailed per-function analysis and reflections

---

*Last updated: Week 10 preparation*
*Author: Manuel Gonzalez Arvelo*
*Imperial College London, Business School*
