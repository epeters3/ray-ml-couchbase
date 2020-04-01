"""
Initializes a node in the cluster to have everything it needs to begin working.
"""
from socket import gethostname

import openml

from mldb.model_running import get_task_ids
from mldb.utils import logger

if __name__ == "__main__":
    # Make sure this node has all the required datasets so it
    # can train ML models on them.
    for task_id in get_task_ids():
        logger.info(
            f"Checking task {task_id} for '{gethostname()}' "
            "node (downloading if not present)"
        )
        openml.tasks.get_task(task_id, download_data=True)