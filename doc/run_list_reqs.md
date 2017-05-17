# run list

A list of all the users previous runs. Each run is shown as a card with relavent data about the run including:

1. The run name and run id
2. Run status, elapsed time, total time
3. Job types in the run, the status of each job.
4. These cards can be clicked to open the run information view

### API calls needed

Get user runs, returns a list of the users runs 

```
get_user_runs = (user) => 
    return [{
        run_name: (str),
        run_id: (int),
        status: (RunStatus),
        jobs: [{
            JobType: (RunStatus)
        }],
        run_time: (Datetime),
    }]
```


### Websocket requests

New run item, adds the new item to the run_list
```
server -> client
new_run_item = (new_run_info) =>
    run_list.appen(new_run_info)
```

Run status change, a run status has changed, which needs to be updated for the user
```
server -> client
run_status_change = (run, status) => 
    index = run_list.find(fun)
    run_list[index].status = status
```