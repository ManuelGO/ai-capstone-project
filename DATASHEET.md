# Datasheet: Black-Box Optimization (BBO) Capstone Dataset

## 1. Motivation

### Purpose
This dataset was created to support the **Black-Box Optimization (BBO) Capstone Project** at Imperial College Business School. The task is to maximize eight unknown ("black-box") functions using sequential Bayesian Optimization with limited query budgets.

### Task Supported
- **Primary task:** Sequential black-box function optimization under query constraints
- **Secondary tasks:** Surrogate model training (Gaussian Processes), acquisition function evaluation, exploration-exploitation trade-off analysis

### Gap Addressed
This dataset fills a gap in educational optimization benchmarks by providing:
- Real-world simulation of expensive function evaluations (1 query/week constraint)
- Functions with varying dimensionality (2D to 8D) and characteristics (unimodal, multimodal, plateaus)
- A sequential decision-making framework that mirrors industrial applications (hyperparameter tuning, chemical yield optimization, experimental design)

### Creators and Funding
- **Creator:** Manuel Gonzalez Arvelo
- **Institution:** Imperial College London, Business School
- **Programme:** Professional Certificate in Machine Learning and Artificial Intelligence
- **Funding:** Self-funded educational project

---

## 2. Composition

### Data Types
The dataset contains input-output pairs from black-box function evaluations:

| Component | Format | Description |
|-----------|--------|-------------|
| **Inputs (X)** | NumPy arrays (`.npy`) | Vectors in [0,1]^d where d varies by function |
| **Outputs (y)** | NumPy arrays (`.npy`) | Scalar values to be maximized |
| **Weekly submissions** | Embedded in notebooks | Query points selected each week |

### Dataset Size

| Function | Dimensions | Initial Points | Weekly Queries | Total Points (W9) |
|----------|------------|----------------|----------------|-------------------|
| F1 | 2D | 10 | 9 | 19 |
| F2 | 2D | 10 | 9 | 19 |
| F3 | 3D | 15 | 9 | 24 |
| F4 | 4D | 20 | 9 | 29 |
| F5 | 4D | 20 | 9 | 29 |
| F6 | 5D | 25 | 9 | 34 |
| F7 | 6D | 30 | 9 | 39 |
| F8 | 8D | 40 | 9 | 49 |
| **Total** | — | **170** | **72** | **242** |

### Data Format
- **Input format:** `x1 - x2 - ... - xd` (six decimal places)
- **Output format:** Scalar float (precision varies by function)
- **Storage:** NumPy binary format (`.npy`) for initial data; Python lists in Jupyter notebooks for weekly data

### Completeness
- **Initial data:** Complete for all 8 functions
- **Weekly data:** Complete through Week 9 (72 queries total)
- **Missing data:** None; all submitted queries received valid outputs

### Labels and Annotations
- No explicit labels; this is a regression/optimization task
- Implicit "high/low" performance categories can be derived from output values

### Relationships Between Instances
- Sequential dependency: Each week's query is informed by all previous observations
- No explicit links between functions (treated independently)

### Recommended Splits
Not applicable for standard ML splits. The dataset follows a sequential protocol:
- **Initial data:** Cold-start observations (provided)
- **Weekly queries:** Sequential acquisitions (1 per week)

### Sensitive Information
- **Privacy:** No personal data; all inputs are synthetic function coordinates
- **Offensive content:** None
- **Confidentiality:** Function formulas are proprietary to the course but outputs are shareable

### Subpopulations
Functions can be grouped by:
- **Dimensionality:** Low-D (F1-F2: 2D), Medium-D (F3-F5: 3-4D), High-D (F6-F8: 5-8D)
- **Landscape type:** Unimodal (F5), Multimodal (F7), Plateau (F8), Constrained (F6)

---

## 3. Collection Process

### Data Acquisition Method
1. **Initial data:** Provided by course instructors (Latin Hypercube Sampling assumed)
2. **Weekly queries:** Generated via Bayesian Optimization pipeline:
   - Fit Gaussian Process surrogate model
   - Generate candidates (Trust Region + Global sampling)
   - Score with Expected Improvement (EI) acquisition function
   - Apply filters (edge, duplicate, constraint masks)
   - Submit top candidate; receive output from hidden oracle

### Sampling Strategy
- **Initial sampling:** Deterministic (provided by course)
- **Query generation:** Adaptive/sequential based on GP posterior
- **Candidate sampling:** Latin Hypercube Sampling (LHS) with typical splits:
  - 70-90% Trust Region (local exploitation)
  - 10-30% Global (exploration)
  - Optional focused sampling around best-known points

### Time Frame
- **Duration:** 10 weeks (Week 1 through Week 10)
- **Frequency:** 1 query per function per week
- **Start date:** Course-dependent (academic term)

### Ethical Review
- No IRB approval required (no human subjects)
- Data is synthetic/simulated

### Consent
- Not applicable (no human participants)

### Impact on Data Subjects
- Not applicable (synthetic data)

---

## 4. Preprocessing/Cleaning/Labelling

### Preprocessing Steps Applied

| Technique | Functions | Purpose |
|-----------|-----------|---------|
| **StandardScaler** | F6, F7, F8 | Normalize inputs for GP numerical stability |
| **log1p transform** | F5 | Stabilize variance for large-scale outputs (y ~ 4000) |
| **Edge filtering** | All | Remove candidates near [0,1] boundaries |
| **Duplicate filtering** | All | L∞ distance check (tol = 0.02-0.03) |

### Constraint Masks Applied

| Function | Constraint | Rationale |
|----------|------------|-----------|
| F4 | x₂ ∈ [0.34, 0.40] | Prevent drift from optimal safe zone |
| F5 | x₃ ≥ 0.98, x₄ ≥ 0.98 | Chemical concentration threshold |
| F6 | x₄ ≥ 0.90 | Butter proportion constraint (recipe optimization) |
| F7 | Anisotropic per-dimension | Based on kernel length_scales |

### Raw Data Preservation
- **Initial data:** Preserved in `initial_data/function_*/` directories
- **Weekly data:** Stored in notebook `week_data` lists with original precision
- **Transformations:** Applied at inference time; raw values always recoverable

---

## 5. Uses

### Intended Uses
- **Educational:** Learning Bayesian Optimization, GP modelling, sequential decision-making
- **Benchmarking:** Comparing acquisition functions (EI, UCB, Thompson Sampling)
- **Research:** Studying exploration-exploitation trade-offs in limited-budget optimization

### Potential Risks and Biases
- **Selection bias:** Query strategies influence which regions are sampled
- **Confirmation bias:** Exploitation-heavy strategies may miss global optima
- **Overfitting:** GP may overfit with limited data in high dimensions (F7, F8)

### Inappropriate Uses
- **Production deployment:** Dataset is educational; real applications require domain-specific validation
- **Function reverse-engineering:** Attempting to recover exact formulas violates course integrity
- **Extrapolation:** Results should not be generalized beyond [0,1]^d input space

### Usage Restrictions
- Academic use only within Imperial College BBO Capstone programme
- Sharing of function formulas is prohibited
- Derived insights may be published with appropriate attribution

---

## 6. Distribution

### Availability
- **Repository:** [GitHub - ai-capstone-project](https://github.com/ManuelGO/ai-capstone-project)
- **Access:** Public repository (read access)
- **Format:** NumPy arrays (`.npy`), Jupyter notebooks (`.ipynb`)

### Distribution Method
- Git clone or direct download from GitHub
- No API access required

### Release Date
- Initial release: Course Week 1
- Updates: Weekly (after each submission round)
- Final version: After Week 10

### Licensing
- **Dataset:** Educational use license (Imperial College)
- **Code:** MIT License (notebooks and utilities)
- **Documentation:** CC BY 4.0

### Fees
- No fees; freely available for educational purposes

---

## 7. Maintenance

### Maintainer
- **Primary:** Manuel Gonzalez Arvelo
- **Contact:** Via GitHub issues or Imperial College email

### Update Schedule
- Weekly updates during active optimization (Weeks 1-10)
- Post-course: Archive status (no further updates)

### Version Control
- Git-based versioning
- Tagged releases for each week's submissions
- Commit history documents all changes

### Archival Plan
- Repository will remain public after course completion
- No planned deletion; serves as portfolio piece

### Error Reporting
- Issues can be reported via GitHub Issues
- Corrections will be documented in commit messages

---

## 8. Additional Notes

### Lessons Learned
Through 9 weeks of optimization, key insights emerged:
1. **Constraint discovery is crucial:** Hard constraints (F5: chemical thresholds, F6: butter proportion) dramatically affect performance
2. **Dimensionality matters:** High-D functions (F7, F8) require different strategies than low-D
3. **Plateaus are real:** F8 demonstrated that not all "stuck" optimizations have hidden peaks
4. **Anisotropic awareness:** Kernel length_scales reveal which dimensions matter most

### Function Characteristics Summary

| Function | Best y (W9) | Landscape | Key Insight |
|----------|-------------|-----------|-------------|
| F1 | ~0.30 | Smooth | x₂ constraint critical |
| F2 | ~0.64 | Smooth | Standard BO works well |
| F3 | ~TBD | Moderate | 3D transition function |
| F4 | ~0.30 | Constrained | x₂ safe zone [0.34, 0.40] |
| F5 | 4368 | Unimodal | x₃,x₄ ≥ 0.98 mandatory |
| F6 | -1.13 (W9 disaster) | Constrained | x₄ ≥ 0.90 (butter) critical |
| F7 | 1.952 | Multimodal | Anisotropic constraints essential |
| F8 | 9.957 | Plateau | Accept plateau, exploit locally |

---

*Last updated: Week 10 preparation*
*Author: Manuel Gonzalez Arvelo*
*Imperial College London, Business School*
