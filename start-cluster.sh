# Run this script from the head node of the cluster
ray start --head --redis-port=6379 --num-cpus=8
# Start each worker node. This command pipes each command in `init_worker.sh` through the
# parallel-ssh command to all nodes in the cluster.
cat ./mldb/scripts/init_worker.sh | parallel-ssh --askpass --inline --send-input --hosts sshhosts
