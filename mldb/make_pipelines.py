from collections import defaultdict

from skplumber import Pipeline
from skplumber.primitives import transformers, classifiers

def _make_base_pipeline():
    # A random imputation of missing values step and one hot encoding of
    # non-numeric features step are automatically added.
    pipeline = Pipeline()
    # Preprocess the inputs
    pipeline.add_step(transformers["StandardScalerPrimitive"])
    return pipeline

_clf_blacklist = {"GaussianMixturePrimitive", "NuSVCPrimitive", "GaussianProcessClassifierPrimitive"}

def make_pipelines() -> dict:
    pipelines = {}
    for est_name, est in classifiers.items():
        if est_name not in _clf_blacklist:
            pipeline = _make_base_pipeline()
            pipeline.add_step(est)
            pipelines[est_name] = pipeline
    
    return pipelines