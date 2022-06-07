#!/usr/bin/env bash

# Sorry guys, I'm too lazy to write actual tests,
# but I want to make sure some code actually runs.

scripts=(
    "./Chapter 7/count_votes/count_votes_concurrent.py"
    "./Chapter 7/count_votes/count_votes_sequential.py"
    "./Chapter 8/semaphore.py"
    "./Chapter 8/race_condition/race_condition.py"
    "./Chapter 8/deadlock/deadlock_arbitrator.py"
    "./Chapter 8/deadlock/deadlock_hierarchy.py"
    "./Chapter 6/stopwatch.py"
    "./Chapter 4/process_lifecycle.py"
    "./Chapter 4/child_processes.py"
    "./Chapter 4/multithreading.py"
    "./Chapter 5/shared_ipc.py"
    "./Chapter 5/message_queue.py"
    "./Chapter 5/pipe.py"
    "./Chapter 5/sockets.py"
    "./Chapter 5/thread_pool.py"
)


# running all the scripts concurrently!
# Such wow
# Much awesome
# Many cool
for script in "${scripts[@]}"
do
	(python3 "$script") &
done
wait