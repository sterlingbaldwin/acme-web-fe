# run template editor

An editor to create new runs. The editor will consist of:

1. A list of supported run types (amwg diagnostic, ncclimo, time series, acme diags, ect).
2. For each run type, a sub component allowing for configuration of the run
3. Each run consists of a list of jobs, a run isn't one instance of one job but can be a set of jobs that are executed in sequence.
4. The option to save the template once the user is happy with it

### API calls needed

Get the template information
```
get_template = (template_id) => 
    template = Templates.find(template_id)
    return template.toJson()
```

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

Save the template. If the templates already exists, update it, if its a new template create a new record.
```
save_template = (new_template) =>
    if new_template.id:
        template = Templates.find(new_template.id)
        template.update(new_template)
    else:
        templates = Templates.create(new_template)
        template.save()
```