# run list

A list of all the users previous runs. Each run is shown as a card with relavent data about the run including:

1. The run name and run id
2. Run status, elapsed time, total time
3. Job types in the run, the status of each job.
4. These cards can be clicked to open the run information view

### API calls needed

get_user_runs = (user) => 
    returns a list of the users runs 
    [{
        run_name: (str),
        run_id: (int),
        status: (RunStatus),
        jobs: [{
            JobType: (RunStatus)
        }],
        run_time: (Datetime),
    }]

