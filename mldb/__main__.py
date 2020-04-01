import ray
from pprint import pprint
import json
import random

from mldb.model_running import get_task_ids, do_run
from mldb.make_pipelines import make_pipelines
from mldb.db import get_already_run_setups, has_setup_been_run, save_run

def main():
    ray.init(address='192.168.36.150:6379')

    # These datasets error out on every run, because the labels are unknown.
    task_black_list = {3918, 3917, 3902, 3903, 3904}
    task_ids = [tid for tid in get_task_ids() if tid not in task_black_list]

    remaining_run_ids = []
    pipeline_map = make_pipelines()
    experiment_setups = []

    already_run_setups = get_already_run_setups()

    # Create the setup for all the experiments and randomize them to 
    # distribute the load more evenly across workers and across time.
    for task_id in task_ids:
        for clf_name, pipeline in pipeline_map.items():
            experiment_setups.append((pipeline, task_id, clf_name))
    random.shuffle(experiment_setups)
    
    # Kick-off execution of every pipeline on every task, for the
    # ones that haven't been previously kicked off and stored in the database.
    for setup in experiment_setups:
        if not has_setup_been_run(setup[2], setup[1], already_run_setups):
            result_id = do_run.remote(*setup)
            remaining_run_ids.append(result_id)
    
    # Gather up the results of all the experiments.
    while remaining_run_ids:
        # Use ray.wait to get the object ID of the first task that completes.
        done_ids, remaining_run_ids = ray.wait(remaining_run_ids)
        result_id = done_ids[0]
        results = ray.get(result_id)
        save_run(results)
        print(f"{len(remaining_run_ids)} runs remaining")

if __name__ == "__main__":
    main()