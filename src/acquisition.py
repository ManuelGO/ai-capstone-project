
import numpy as np
from scipy.stats import norm

def expected_improvement(mu, sigma, y_best, xi=0.01):
    sigma = np.maximum(sigma, 1e-12)
    imp = mu - y_best - xi
    Z = imp / sigma
    return imp * norm.cdf(Z) + sigma * norm.pdf(Z)

def ucb(mu, sigma, kappa=1.6):
    return mu + kappa * sigma

def max_variance(mu, sigma):
    return sigma
