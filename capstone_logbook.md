---
title: "Weekly Logbook – Capstone Project in ML/AI: Black-Box Optimization"
author: "Manuel González Arvelo"
date: "2025-10-05"
---

# Weekly Logbook – Capstone Project in ML/AI: Black-Box Optimization

**Author:** Manuel González Arvelo  
**Duration:** 10 Weeks  
**Program:** Professional Formation in Machine Learning and Artificial Intelligence  
**Date:** 2025-10-05  

---

## Project Overview
This logbook documents weekly progress in the Capstone Project on **black-box optimization**, where the goal is to find the maxima of unknown functions using limited evaluations.  
Each week includes planning, decision-making rationale, and reflection on exploration versus exploitation.

---

# WEEK 1 — Example Entry

## 1. Previous Context
Initial dataset: 10 (x, y) pairs per function provided.  
Objective: maximize the output of 8 unknown functions (F1–F8).

---

## 2. Strategy Used This Week

| Function | Model Type | Method / Acquisition | Goal (Exploration / Exploitation) | Key Parameters |
|-----------|-------------|----------------------|----------------------------------|----------------|
| F1 | Gaussian Process (Matern 5/2) | UCB | Exploration | κ = 2.0 |
| F2 | Random Forest | Expected Improvement (EI) | Balanced | ξ = 0.01 |
| F3 | GP | EI | Exploitation | — |
| F4 | Extra Trees | UCB | Exploration | κ = 1.8 |

**Justification:**  
This week, the focus was on exploration since the initial dataset is small. Higher κ values were used in UCB to broaden search regions and learn the global structure of each function.

---

## 3. Input Submitted

| Function | Dimensionality (d) | Input (x) | Rationale for Selection |
|-----------|--------------------|------------|--------------------------|
| F1 | 2 | 0.345123 - 0.789654 | High uncertainty, promising mean |
| F2 | 4 | 0.102334 - 0.221110 - 0.555000 - 0.888333 | Large predicted variance |
| F3 | 3 | 0.710000 - 0.540000 - 0.230000 | Local exploitation near current best |

---

## 4. Results Received

| Function | Observed y | Model Prediction μ(x) | Surprise | Outcome |
|-----------|-------------|----------------------|-----------|----------|
| F1 | 0.672 | 0.620 | 0.052 | Slightly better than expected |
| F2 | 0.411 | 0.490 | 0.079 | Lower than expected |
| F3 | 0.733 | 0.710 | 0.023 | Confirmed local improvement |

**Interpretation:**  
The GP model performed well in lower dimensions (F1, F3) but struggled in higher dimensions (F2). Exploration will continue next week with new Sobol samples to diversify search regions.

---

## 5. Lessons Learned
- GP predictions align well with smooth 2D–3D functions.  
- For 4D+ functions, the model uncertainty may be underestimated.  
- The trade-off parameter (κ) in UCB strongly influences exploration intensity.

---

## 6. Next Week’s Plan
- Increase exploration in F2 and F4 using larger Sobol candidate sets (20k samples).  
- Switch to EI for F5 and F6 as data becomes denser.  
- Visualize GP mean and variance contours for F1 to guide intuition.

---

## 7. Progress Summary
This week focused on establishing a baseline. The workflow for submission, data logging, and reflection is validated. Next steps will emphasize improving acquisition optimization and uncertainty modeling.

---

# WEEK [2–10] TEMPLATE (Copy for Each Week)

## 1. Summary of Previous Week
- Functions updated: [List]  
- Key observations: [Summary]  
- Data points total: [Number]  

---

## 2. Strategy Used This Week

| Function | Model Type | Acquisition / Method | Goal | Parameters |
|-----------|-------------|----------------------|------|-------------|
| [F#] | [Model] | [Method] | [Explore / Exploit] | [κ / ξ / other] |

**Justification:**  
[Explain why this strategy was chosen.]

---

## 3. New Input Submitted

| Function | Dimensionality | Input (x) | Rationale |
|-----------|----------------|------------|------------|
| [F#] | [d] | [0.xxx - 0.xxx ...] | [Reason] |

---

## 4. Results Received

| Function | Observed y | Model Prediction μ(x) | Error | Outcome |
|-----------|-------------|----------------------|--------|----------|
| [F#] | [ ] | [ ] | [ ] | [Better / Worse / Neutral] |

**Interpretation:**  
[Discuss what you learned and how the model behaved.]

---

## 5. Reflection
- What worked well:  
- What didn’t work:  
- Insights gained:  
- Adjustments for next week:  

---

## 6. Metrics Tracking (Optional)

| Function | Best y | Iteration of Best | Total Queries | Avg. Variance σ² | Mode |
|-----------|---------|-------------------|----------------|------------------|------|
| F1 | [ ] | [ ] | [ ] | [ ] | [Explore / Exploit] |

---

## 7. Weekly Executive Summary
> Summarize in 2–3 sentences your main reasoning and what you plan to adjust next week.

---

## 8. Visualization Space (Optional)
_Add plots, convergence curves, or variance maps here._

---

## Appendix (Optional)
Include notes, code snippets, or screenshots used for analysis.