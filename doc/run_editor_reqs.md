# run editor

An editor to create new runs. The editor will consist of:

1. A list of supported run types (amwg diagnostic, ncclimo, time series, acme diags, ect).
2. For each run type, a sub component allowing for configuration of the run
3. Each run consists of a list of jobs, a run isn't one instance of one job but can be a set of jobs that are executed in sequence.
4. The option to save the run once the user is happy with it
5. The option to start a run once its been saved

### API calls needed

Get supported job types
```
get_job_types = () =>
    return [job.type for job in Jobs.all()]
```

Get a jobs configuration component
```
get_job_config = (job_type) =>
    job = Jobs.find(job_type)
    return job.requirements
```

Save the run config
```
save_run = (new_run) =>
    run = Runs.create(new_run)
    run.save()
```