
import numpy as np
from scipy.stats import qmc

def lhs(lb, ub, n, seed):
    d = lb.size
    U = qmc.LatinHypercube(d=d, seed=seed).random(n)
    return lb + U*(ub - lb)

def mask_edges(C, edge_eps=1e-3):
    return np.all((C > edge_eps) & (C < 1 - edge_eps), axis=1)

def too_close_Linf(c, X, tol=0.02):
    return np.any(np.max(np.abs(X - c), axis=1) < tol)
