# 📚 References & Technical Foundations  
**Black-Box Optimisation (BBO) — Capstone Project**  
*Manuel González Arvelo*

This document lists all academic, technical and practical resources that informed the optimisation strategy used in this project.  
It complements the README and the weekly notebooks by providing a clear bibliography for surrogate modelling, Bayesian optimisation and candidate selection.

---

## 1. Core Bayesian Optimisation Literature

### Foundational Papers
- **Jones, D. R., Schonlau, M., Welch, W. J. (1998).**  
  *Efficient Global Optimization of Expensive Black-Box Functions.*  
  *Journal of Global Optimization.*  
  → Introduces **Expected Improvement (EI)** and forms the basis of modern BO.

- **Mockus, J. (1975–1989).**  
  *Bayesian Approach to Global Optimization.*  
  → Fundamental ideas behind Bayesian optimisation and utility-based search.

- **Brochu, E., Cora, V., de Freitas, N. (2010).**  
  *A Tutorial on Bayesian Optimization of Expensive Cost Functions.*  
  → Accessible explanation of EI, GPs, and sequential decision making.

- **Snoek, J., Larochelle, H., Adams, R. (2012).**  
  *Practical Bayesian Optimization of Machine Learning Algorithms.*  
  → Establishes BO as a practical tool for ML hyperparameter search.

---

## 2. Gaussian Processes (GPs)

- **Rasmussen, C. E., Williams, C. K. I. (2006).**  
  *Gaussian Processes for Machine Learning (GPML).*  
  → Definitive reference on GP regression, Matern kernels, noise handling, ARD, and predictive distributions.

---

## 3. Acquisition Functions: Exploration–Exploitation

- **Srinivas, N., Krause, A., Kakade, S., Seeger, M. (2010).**  
  *Gaussian Process Optimization in the Bandit Setting: No Regret Algorithms.*  
  → Introduces **GP-UCB**, used as a fallback when EI becomes flat.

- **Kushner, H. J. (1964).**  
  *A New Method of Locating the Maximum Point of an Arbitrary Multipeak Curve in the Presence of Noise.*  
  → Early formulation of improvement-based strategies.

---

## 4. Trust Regions & Local BO

- **Eriksson, D., et al. (2019).**  
  *Scalable Global Optimization via Local Bayesian Optimization.*  
  → Motivates **trust-region BO**, anchoring candidate regions near the current best.

- **Regis, R. (2014).**  
  *Latin Hypercube Sampling Strategies.*  
  → Basis for using **LHS** to generate diverse candidate sets.

---

## 5. Software & Framework Documentation

### scikit-learn  
Used for GP regression, kernels, scaling:  
https://scikit-learn.org/stable/modules/gaussian_process.html

### SciPy  
Used for EI computation (`scipy.stats.norm`).  
https://docs.scipy.org/

### NumPy  
Vectorisation, random sampling, array manipulation.  
https://numpy.org/doc/

---

## 6. Educational Resources

### StatQuest (YouTube)  
Clear and practical explanations that guided GP kernel intuition, noise modelling, and acquisition behaviour:  
https://www.youtube.com/@statquest

Relevant playlists:
- Gaussian Processes  
- Kernels (RBF, Matern)  
- Bayesian Optimisation fundamentals  
- Maximum Likelihood, Regularisation  

### PyTorch & TensorFlow (contextual learning, not directly used)
- PyTorch Docs: https://pytorch.org/docs/  
- TensorFlow Guide: https://www.tensorflow.org/guide  

---

## 7. Future Sources to Explore

Potential future work may include:
- **BOHB** (Falkner et al., 2018) – hybrid BO + HyperBand.  
- **Optuna** (Akiba et al., 2019) – advanced HPO library.  
- **TuRBO** (Wang et al., 2020) – scalable trust-region BO for high-dimensional settings.

---

## 8. How These References Shape the Project

These materials directly influenced the project:

- **GP surrogate modelling** → GPML + scikit-learn.  
- **EI acquisition function** → EGO (Jones et al., 1998).  
- **UCB fallback** → GP-UCB (Srinivas et al., 2010).  
- **Trust regions around best points** → Local BO (Eriksson et al., 2019).  
- **LHS candidate sampling** → Regis (2014).  
- **Noise modelling & kernel selection** → GPML + StatQuest.

Together, these sources provide a rigorous foundation for all modelling and optimisation decisions implemented in the capstone.

