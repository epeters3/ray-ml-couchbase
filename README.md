## To Initialize The Ray Cluster

This should be done only once, and not every time the Ray cluster is started:

1.  Add an `sshhosts` file to project root, adding the name of each host in the cluster that will be ssh'd into, one name per line.
1.  ```
    ./prep-cluster.sh
    ```

## To Boot Up The Ray Cluster & Run the Experiments

1.  Start up the CouchBase database:
    ```
    sudo docker start db
    ```

1.  Start up the cluster from the host node:
    ```
    ./start-cluster.sh
    ```
1.  Run the experiments from the host node:
    ```
    python3 -m mldb
    ```

# To Bring Down The Ray Cluster

1.  Bring down the CouchBase database:
    ```
    sudo docker stop db
    ```

1.  Bring down the Ray cluster:
    ```
    ./stop-cluster.sh
    ```

## Troubleshooting

Ensure the Python `ray` package is installed on all cluster nodes, and that the python packages folder is on the `PATH` of each of those nodes, so the `ray` CLI can be accessed.

If any step fails, you may have to ssh into each machine and execute the step manually. 