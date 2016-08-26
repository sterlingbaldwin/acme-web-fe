# {   u'content': u'hello world!',
#     u'destination': u'init',
#     u'target_app': u'run_manager'}
# from poller.views import update as poller_update
from util.utilities import print_message
from channels import Group
import json


# An empty dict subclass, to allow me to call poller views directly
# without needing to make an http request
class mydict(dict):
    pass


def dispatch(message, data, user):
    destination = data.get('destination')
    if destination == 'init':
        return init(message, data, user)
        # group_job_update(9999, 'testest', 'rockin it')
    elif destination == 'status_update':
        return status_update(message, data, user)
    elif destination == 'send_to_group':
        return send_to_group(data, user)
    else:
        print_message('unrecognized destination function {}'.format(destination))
        return -1


def init(message, data, user):
    message.reply_channel.send({'text': 'connection initialized to run manager'})
    return 0


def status_update(message, data, user):
    return -1


def send_to_group(data, group):
    Group(group).send(data)
    return 0


def group_job_update(job_id, user, status):
    message = {
        'text': json.dumps({
            'destination': 'set_run_status',
            'job_id': job_id,
            'user': user,
            'status': status
        })
    }
    Group('active').send(message)