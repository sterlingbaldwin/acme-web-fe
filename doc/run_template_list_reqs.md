#### run template list

A list of all the run configurations the user has created in the past. This will allow them to create a run template that they can run multiple times with small changes. 

1. List of saved run templates.
2. A sharing option to give another user a copy of the template.
3. Each run template will consist of the name of the run, and a button to open it in the template editor.
4. Each run template will have a list of previous runs of this type.

### API calls

Get all the tempalates the user has access to.
```
get_templates = (user) =>
    return [for template in RunTemplates.all() if user in template.allowed_users]
```

Get the list of users so we know who we can share with
```
get_user_list = () =>
    return [user.toJson() for user in Users.all()]
```

Get the group list
```
get_group_list = () =>
    return [group.toJson() for group in Groups.all()]
```

Share the template with a user
```
share_template_user = (template_id, user) => 
    template = Templates.find(template_ie)
    template.allowed_users.append(user)
```

Share the tempaltes with a group
```
share_template_group = (template_id, group_id) =>
    template = Templates.find(template_id)
    group = Groups.find(group_id)
    users = group.users
    for user in users:
        template.allowed_users.append(user)
```

### Websocket requests

A template has been share with me, add it to the top of the templates list
```
server -> client
update_template_list = (template) =>
    template_list.prepend(template)
```
