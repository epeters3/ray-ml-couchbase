# Tell the head node to stop
ray stop
# Stop the database
docker stop db
# Tell the worker nodes to stop
parallel-ssh --askpass --inline --hosts sshhosts /users/grads/epeter92/.local/bin/ray stop
