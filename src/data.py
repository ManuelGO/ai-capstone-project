
from pathlib import Path
import numpy as np

def load_initial(data_dir: Path):
    X = np.load(data_dir / "initial_inputs.npy", allow_pickle=True)
    y = np.load(data_dir / "initial_outputs.npy", allow_pickle=True)
    return np.asarray(X, float), np.asarray(y, float).ravel()

def append_weeks(X, y, week_data):
    for x_new, y_new in week_data:
        X = np.vstack([X, x_new])
        y = np.append(y, y_new)
    return X, y
