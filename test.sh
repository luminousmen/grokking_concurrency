#!/usr/bin/env bash

# Sorry guys, I'm too lazy to write actual tests,
# but I want to make sure some code actually runs.
set -e
scripts=(
#    "./Chapter 7/pipeline.py"
    "./Chapter 7/count_votes/count_votes_concurrent.py"
    "./Chapter 7/count_votes/count_votes_sequential.py"
#    "./Chapter 9/reader_writer/reader_writer.py"
    "./Chapter 9/reader_writer/rwlock.py"
    "./Chapter 9/reader_writer/rwlock_fair.py"
    "./Chapter 9/starvation.py"
#    "./Chapter 9/deadlock/deadlock.py"
    "./Chapter 9/deadlock/deadlock_arbitrator.py"
    "./Chapter 9/deadlock/deadlock_hierarchy.py"
    "./Chapter 9/deadlock/lock_with_name.py"
    "./Chapter 9/producer_consumer.py"
    "./Chapter 8/semaphore.py"
    "./Chapter 8/race_condition/bank_account.py"
    "./Chapter 8/race_condition/race_condition.py"
    "./Chapter 8/race_condition/unsynced_bank_account.py"
    "./Chapter 8/race_condition/synced_bank_account.py"
    "./Chapter 6/pacman.py"
#    "./Chapter 6/arcade_machine_multitasking.py"
#    "./Chapter 6/arcade_machine.py"
#    "./Chapter 10/thread_cost.py"
#    "./Chapter 10/pizza_server.py"
#    "./Chapter 10/pizza_busy_wait.py"
#    "./Chapter 10/pizza_client.py"
#    "./Chapter 10/threaded_pizza_server.py"
#    "./Chapter 11/event_loop.py"
#    "./Chapter 11/pizza_reactor.py"
    "./Chapter 4/process_lifecycle.py"
    "./Chapter 4/child_processes.py"
    "./Chapter 4/multithreading.py"
    "./Chapter 5/library_thread_pool.py"
    "./Chapter 5/thread_pool.py"
    "./Chapter 5/message_queue.py"
    "./Chapter 5/shared_ipc.py"
    "./Chapter 5/password_cracking_parallel.py"
    "./Chapter 5/sockets.py"
    "./Chapter 5/pipe.py"
    "./Chapter 2/password_cracking_sequential.py"
#    "./Chapter 13/wordcount/worker.py"
#    "./Chapter 13/wordcount/server.py"
    "./Chapter 13/wordcount/protocol.py"
    "./Chapter 13/wordcount/wordcount_seq.py"
    "./Chapter 13/wordcount/scheduler.py"
    "./Chapter 13/matmul/time_matmuls.py"
    "./Chapter 13/matmul/matmul_sequential.py"
    "./Chapter 13/matmul/matmul_concurrent.py"
    "./Chapter 12/future_burger.py"
    "./Chapter 12/coroutine.py"
#    "./Chapter 12/asynchronous_pizza/asynchronous_pizza_joint.py"
    "./Chapter 12/asynchronous_pizza/async_socket.py"
#    "./Chapter 12/asynchronous_pizza/cooperative_pizza_server.py"
    "./Chapter 12/asynchronous_pizza/event_loop.py"
#    "./Chapter 12/asynchronous_pizza/aio.py"
    "./Chapter 12/asynchronous_pizza/future.py"
    "./Chapter 12/asynchronous_pizza/event_loop_with_pool.py"
)


# running all the scripts concurrently!
# Such wow
# Much awesome
# Many cool
for script in "${scripts[@]}"
do
	(python3.9 "$script") #&
done
wait