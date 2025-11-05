
import numpy as np

def make_tr_box(anchor, lb, ub, L):
    lb_tr = np.clip(anchor - 0.5 * L * (ub - lb), 0, 1)
    ub_tr = np.clip(anchor + 0.5 * L * (ub - lb), 0, 1)
    return lb_tr, ub_tr
