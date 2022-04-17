#!/usr/bin/env bash

# Sorry guys, I'm too lazy to write actual tests,
# but I want to make sure the code actually runs.

scripts=(
#    "./Chapter 7/find_files_sequential.py"
    "./Chapter 7/task_decomposition.py"
    "./Chapter 7/count_votes.py"
#    "./Chapter 7/find_files_concurrent.py"
#    "./Chapter 7/pipeline.py"
    "./Chapter 8/race_condition_fixed.py"
#    "./Chapter 8/deadlock.py"
    "./Chapter 8/semaphore.py"
#    "./Chapter 8/starvation.py"
    "./Chapter 8/race_condition.py"
    "./Chapter 8/deadlock_arbitrator.py"
    "./Chapter 8/deadlock_hierarchy.py"
#    "./Chapter 6/game_threads.py"
    "./Chapter 6/stopwatch.py"
#    "./Chapter 6/game_multitasking.py"
    "./Chapter 4/process_lifecycle.py"
    "./Chapter 4/child_processes.py"
    "./Chapter 4/multithreading.py"
    "./Chapter 5/shared_ipc.py"
    "./Chapter 5/password_cracking_parallel.py"
    "./Chapter 5/message_queue.py"
    "./Chapter 5/pipe.py"
    "./Chapter 5/sockets.py"
    "./Chapter 5/thread_pool.py"
#    "./Chapter 2/password_cracking_sequential.py"
)


# running scripts concurrently
for script in "${scripts[@]}"
do
	(python3 "$script") &
done
wait