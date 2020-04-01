from socket import gethostname
from pprint import pprint
from time import time

import ray
import openml
from skplumber import Pipeline
from sklearn.model_selection import train_test_split

from mldb.learning_utils import metrics
from mldb.utils import logger
from mldb.db import save_run

def get_task_ids() -> dict:
    return openml.study.get_suite("OpenML-CC18").tasks

@ray.remote
def do_run(pipe: Pipeline, task_id: int, clf_name: str) -> dict:
    """
    Runs given pipeline on given openml task, writing a dictionary
    containing data about the run to the database. If the task is not downloaded to
    the host machine, the task will be downloaded automatically.
    """
    status = "SUCCESS"
    hostname = gethostname()
    logger.info(f"training '{clf_name}' on task {task_id} on host: '{hostname}'...")
    task = openml.tasks.get_task(task_id) # downloads task if not on host already
    dataset = task.get_dataset()
    X, y = task.get_X_and_y("dataframe")

    start_time = time()

    try:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33)
        pipe.fit(X_train, y_train)
        y_pred = pipe.predict(X_test)

        scores = {}
        for metric_name, metric_fn in metrics.items():
            scores[metric_name] = metric_fn(y_test, y_pred)
    
    except Exception as e:
        status = "FAIL"
        logger.error(e)
        error_msg = str(e)
    
    fit_score_time = time() - start_time

    results = {
        "clf_name": clf_name,
        "task": {
            "id": task_id
        },
        "dataset": {
            "name": dataset.name,
            "id": dataset.dataset_id,
            "n_instances": len(X.index)
        },
        "status": status,
        "hostname": hostname,
        "time": fit_score_time
    }

    if status == "FAIL":
        results["error_msg"] = error_msg
    else:
        results.update(scores)
    
    return results
