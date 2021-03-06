from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from util.utilities import print_message
from util.utilities import print_debug

import os
import vcs
import cdms2
import numpy
import json


@login_required
def get_provenance(request):
    user = str(request.user)
    try:
        data = json.loads(request.body)
    except Exception as e:
        raise

    file_name = data.get('file_name')
    run_name = data.get('run_name')
    run_id = data.get('run_id')
    variable = data.get('variable')
    if not file_name:
        print_message('No file name')
        return HttpResponse(status=400)
    if not run_name:
        print_message('No run_name')
        return HttpResponse(status=400)
    if not run_id:
        print_message('No run_id')
        return HttpResponse(status=400)
    if not variable:
        print_message('No variable')
        return HttpResponse(status=400)

    print_message('Looking up filepath for file={file}, user={user}, run_name={run_name}, id={id}'.format(
        file=file_name,
        user=user,
        run_name=run_name,
        id=run_id), 'ok')

    filepath = find_filepath(file_name, user, run_name, run_id)
    try:
        file = cdms2.open(filepath)
    except Exception as e:
        print_message('Error opening {file} with cdms2'.format(file=filepath))
        print_debug(e)
        return HttpResponse(status=500)

    try:
        provenance = file(variable).exportProvenance()
    except Exception as e:
        print_message('Error getting information from {file} with variable={var}'.format(file=filepath, var=variable))
        print_debug(e)
        return HttpResponse(status=500)
    return HttpResponse(json.dumps(provenance))


@login_required
def get_variables(request):
    user = str(request.user)
    try:
        data = json.loads(request.body)
    except Exception as e:
        raise

    file_name = data.get('file_name')
    run_name = data.get('run_name')
    run_id = data.get('run_id')
    if not file_name:
        print_message('No file name')
        return HttpResponse(status=400)
    if not run_name:
        print_message('No run_name')
        return HttpResponse(status=400)
    if not run_id:
        print_message('No run_id')
        return HttpResponse(status=400)

    print_message('Looking up filepath for file={file}, user={user}, run_name={run_name}, id={id}'.format(
        file=file_name,
        user=user,
        run_name=run_name,
        id=run_id), 'ok')
    filepath = find_filepath(file_name, user, run_name, run_id)
    print_message('filepath={filepath}'.format(filepath=filepath), 'ok')
    try:
        file = cdms2.open(filepath)
    except Exception as e:
        print_message('Error opening {file} with cdms2'.format(file=filepath))
        print_debug(e)
        return HttpResponse(status=500)

    variables = []
    bounds_arrays = [a.bounds for _, a in file.axes.items() if hasattr(a, "bounds")]
    for v in file.variables:
        if v in bounds_arrays:
            continue
        variables.append(v)
    return HttpResponse(json.dumps(variables))


# Utility function, should not ever be called via url
def find_filepath(file, user, run_name, run_id, run_type='diagnostic'):
    path = 'userdata/{user}/{run_type}_output/{run_name}_{id}/amwg/{file}'.format(
        user=user,
        run_type=run_type,
        run_name=run_name,
        id=run_id,
        file=file
    )
    filepath = os.path.abspath(path)
    return filepath
