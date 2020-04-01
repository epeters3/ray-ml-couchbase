import math

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score
from skplumber import Pipeline


def f1_macro(y_true, y_pred) -> float:
    return f1_score(y_true, y_pred, average="macro")

metrics = {"accuracy": accuracy_score, "f1_macro": f1_macro}
