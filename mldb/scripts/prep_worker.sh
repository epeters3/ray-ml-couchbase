python3 -m pip install openml ray
python3
import openml
from socket import gethostname
for task_id in openml.study.get_suite("OpenML-CC18").tasks:
    print(
        f"Checking task {task_id} for '{gethostname()}' "
        "node (downloading if not present)"
    )
    openml.tasks.get_task(task_id, download_data=True)

