
import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel as C
from sklearn.preprocessing import StandardScaler

def build_gp(dims, nu, ls_init, ls_bounds, noise_level, noise_bounds, restarts=12, seed=0):
    kernel = C(1.0, (1e-3, 1e3)) * Matern(length_scale=np.ones(dims)*ls_init,
                                           nu=nu, length_scale_bounds=ls_bounds) \
             + WhiteKernel(noise_level=noise_level, noise_level_bounds=noise_bounds)
    return GaussianProcessRegressor(kernel=kernel, normalize_y=True,
                                    n_restarts_optimizer=restarts, random_state=seed)

def fit_gp(X, y, gp, scale_X=True):
    scaler = None
    X_in = X
    if scale_X:
        scaler = StandardScaler().fit(X)
        X_in = scaler.transform(X)
    gp.fit(X_in, y)
    return gp, scaler
