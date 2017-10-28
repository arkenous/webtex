from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render_to_response(template_name='index.jinja', context={
        'user': request.user
    })


@login_required
def compile_content(request):
    import json
    from django.http import HttpResponse,Http404

    if request.method == 'POST':
        content = request.POST['content']
        print('content: '+content)
        response = json.dumps({'result': 'OK'})
        return HttpResponse(response, content_type='text/javascript')
    else:
        raise Http404
