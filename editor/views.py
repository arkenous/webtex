from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.conf import settings
from os import mkdir, listdir, chdir
from os.path import exists, isdir, join
from subprocess import check_output

storage = settings.BASE_DIR + '/editor/static/storage/'


@login_required
def index(request):
    return render_to_response(template_name='index.jinja', context={
        'user': request.user
    })


@login_required
def read_file_list(request):
    data = {}
    if request.method == 'POST':
        if not exists(storage) or not isdir(storage):
            mkdir(storage)

        user_storage = storage + request.user.username + '/'
        if exists(user_storage) and isdir(user_storage):
            data['list'] = listdir(user_storage)
        else:
            mkdir(user_storage)
            data['list'] = ''

        data['result'] = 'Success'
        return JsonResponse(data)
    else:
        return JsonResponse({'result': 'Error'})


@login_required
def compile_content(request):
    data = {}
    if request.method == 'POST':
        user_storage = storage + request.user.username + '/'
        if not exists(user_storage) or not isdir(user_storage):
            return JsonResponse({'result': 'Error', 'cause': 'user storage is not available'})

        data['result'] = 'Success'
        content = request.POST['content']
        chdir(user_storage)
        f = open('document.tex', 'w')
        f.write(content)
        f.close()

        data['latex'] = check_output(
            ['platex', '-halt-on-error', '-interaction=nonstopmode',
             '-file-line-error', '-no-shell-escape', 'document.tex']
        ).decode('utf-8').splitlines() + check_output(['dvipdfmx', 'document.dvi']).decode('utf-8').splitlines()

        if exists('document.pdf'):
            data['exist_pdf'] = 'True'
            data['user'] = request.user.username
            # TODO: Redpen添削機能を実装する
            data['redpen_out'] = ""
            data['redpen_err'] = ""
        else:
            data['exist_pdf'] = 'False'

        return JsonResponse(data)
    else:
        return JsonResponse({'result': 'Error'})


@login_required
def upload_file(request):
    if request.method == 'POST':
        user_storage = storage + request.user.username + '/'
        if not exists(user_storage) or not isdir(user_storage):
            return JsonResponse({'result': 'Error', 'cause': 'user storage is not available'})

        file = request.FILES['file']
        if file:
            dest = open(join(user_storage, file.name), 'wb+')
            for chunk in file.chunks():
                dest.write(chunk)
            dest.close()
            return JsonResponse({'result': 'Success'})
        else:
            return JsonResponse({'result': 'Error', 'cause': 'file is not valid'})
    else:
        return JsonResponse({'result': 'Error'})
