#### run queue

A view of the global queue status. The run queue will show the user:

1. A global run queue showing the status of all queued/running jobs in the system.
2. Filter to show only my jobs
3. Each run will only show the run name, run id, and run status.
4. A user can cancel their runs.

### API calls

Get run queue, return a list of job_info objects
```
get_run_queue = () =>
    return sorted([job for job in JobQueue.all()], job_compare_newest_first)
```

Cancel a run, remove the job from the queue
```
cancel_run = (run_id) => 
    run = JobQueue.find(run_id)
    if user in run.admin_users:
        run.cancel()
        return True
    else:
        return False
```

### Websocket requests

Job status updates. Any time the status of one of the jobs in the list changes, update its status for the user
```
server -> client
job_queue_update = (job_id, status) => 
    job = job_queue.find(job_id)
    job.status = status
```

New job added to the queue. When another user adds a job to the queue, it should be updated for all the other users
```
server -> client
job_queue_push = (job) => 
    job_queue.prepend(job)
```



