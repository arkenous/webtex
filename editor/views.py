from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.conf import settings
from os import mkdir, listdir
from os.path import exists, isdir

storage = settings.BASE_DIR + '/storage/'


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
    if request.method == 'POST':
        content = request.POST['content']
        print('content: '+content)
        return JsonResponse({'result': 'OK'})
    else:
        raise JsonResponse({'result': 'Error'})
