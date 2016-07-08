from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
import json
import os
from constants import RUN_SCRIPT_PATH
from util.utilities import print_debug
from models import ModelRun
import shutil


#
# Creates a new model run configuration
# input: user, the user requesting a new run config folder
#        run_name, the name of the new run config
#        optional: template, the name of their predefined template
# @login_required
def create_run(request):
    path = os.path.abspath(os.path.dirname(__file__))
    user_directory = path + RUN_SCRIPT_PATH + str(request.user)

    # TODO: make this not hard coded
    template_directory = path + RUN_SCRIPT_PATH + 'resources/'
    if not os.path.exists(user_directory):
        print "[+] Creating directory {}".format(user_directory)
        os.makedirs(user_directory)


    new_run = request.GET.get('run_name')
    if not new_run:
        return HttpResponse(status=400)

    new_run_dir = os.path.join(user_directory, new_run)
    if os.path.exists(new_run_dir):
        return HttpResponse(status=409)

    try:
        os.makedirs(new_run_dir)
    except Exception as e:
        print_debug(e)
        return HttpResponse(status=500)

    try:
        run = ModelRun(user=request.user)
        run.save()
    except Exception as e:
        print "[-] Error saving run {} in database for user {}".format(new_run_dir, request.user)
        shutil.rmtree(new_run_dir, ignore_errors=True)
        print_debug(e)
        return JsonResponse({'error': 'error saving run in database'})

    template = request.POST.get('template')
    if not template:
        return JsonResponse({'new_run_dir': new_run_dir})
    else:
        found_template = False
        template_path = False
        template_search_dirs = [request.user, 'global']
        template_search_dirs = [os.path.join(template_directory,x) for x in template_search_dirs]
        for directory in template_search_dirs:
            if os.path.exists(x):
                if template in os.listdir(x):
                    found_template = True
                    template_path = os.path.join(x)

        if found_template:
            try:
                shutil.copyfile(template_path, new_run_dir)
            except Exception as e:
                print_debug(e)
                print "[-] Error saving template {} for user {}".format(template, request.user)
                return JsonResponse({'new_run_dir': new_run_dir, 'error': 'template not saved'})
        else:
            return JsonResponse({'new_run_dir': new_run_dir, 'template_dir': template_path})


@login_required
def delete_run(request):
    run_directory = request.DELETE.get('run_name')
    run_directory = user_directory = os.path.join(str(os.getcwd()), RUN_SCRIPT_PATH, run_directory)
    run_directory = '/Users/baldwin32/projects/acme-web-fe/run_manager/run_scripts/test/test_run'

    if not os.path.exists(run_directory):
        print "[-] Attempt to delete directory that doesnt exist"
        return HttpResponse(status=400)

    if request.user != run_directory.split('/')[-2]:
        print "[-] Attempt to delete someone elses run directory"
        return HttpResponse(status=403)

    shutil.rmtree(run_directory, ignore_errors=True)
    if os.path.exists(run_directory):
        print "[-] Failed to remove directory {}".format(run_directory)
        return HttpResponse(status=500)

    return HttpResponse()

def view_runs(request):
    return JsonResponse({})


def create_script(request):
    return JsonResponse({})


def update_script(request):
    return JsonResponse({})


def read_script(request):
    return JsonResponse({})


def delete_script(request):
    return JsonResponse({})