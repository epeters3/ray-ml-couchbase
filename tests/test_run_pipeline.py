from unittest import TestCase

import openml
from skplumber import Pipeline
from skplumber.primitives import transformers, classifiers
from sklearn.model_selection import train_test_split


class TestRunPipeline(TestCase):
    def test_pipeline_can_run_on_task_6(self):
        pipe = Pipeline()
        pipe.add_step(transformers["StandardScalerPrimitive"])
        pipe.add_step(classifiers["ExtraTreeClassifierPrimitive"])

        X, y = openml.tasks.get_task(6).get_X_and_y("dataframe")
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)

        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)