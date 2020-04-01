from couchbase.n1ql import N1QLQuery

from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator

cluster = Cluster('couchbase://localhost')
authenticator = PasswordAuthenticator('Administrator', 'password')
cluster.authenticate(authenticator)

# Open the machine learning runs bucket
runs_bucket = cluster.open_bucket('mlruns')

def get_already_run_setups() -> set:
    q = N1QLQuery("SELECT clf_name, task.id AS task_id FROM mlruns")
    return {(row["clf_name"], row["task_id"]) for row in runs_bucket.n1ql_query(q)}

def has_setup_been_run(clf_name: str, task_id: int, setups: set) -> bool:
    return (clf_name, task_id) in setups

def save_run(run: dict):
    runs_bucket.insert(f"{run['clf_name']}+{run['task']['id']}", run)