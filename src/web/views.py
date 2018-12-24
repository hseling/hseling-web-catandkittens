from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django import forms

import requests


HSE_API_ROOT = "http://hse-api-web/"

# Create your views here.
def web_index(request):
    return render(request, 'index.html',
                  context={})


def web_main(request):
    # content = requests.get(HSE_API_ROOT)
    return render(request, 'main.html',
                  context={"status": request.GET.get('status')})


def web_status(request):
    task_id = request.GET.get('task_id')
    if task_id:
        url = HSE_API_ROOT + "status/" + task_id
        content = requests.get(url)
        result = content.json()
        if result.get('status') == 'SUCCESS':
            content = requests.get(HSE_API_ROOT + 'files/' + result.get('result', [""])[0])
            result['raw'] = content.content.decode('utf-8')
        return JsonResponse(result)
    return JsonResponse({"error": "No task id"})


def handle_uploaded_file(f):
    files = {'file': f}
    url = HSE_API_ROOT + "upload"
    content = requests.post(url, files=files)
    file_id = content.json().get("file_id")

    if file_id:
        file_id = file_id[7:]
        url = HSE_API_ROOT + "process/" + file_id
        content = requests.get(url)

    else:
        raise Exception(content.json())

    return content.json().get('task_id')


class UploadFileForm(forms.Form):
    file = forms.FileField()


def web_upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            task_id = handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('main?task_id=' + task_id)
    else:
        form = UploadFileForm()
    return render(request, 'main.html', {'form': form})

def web_check(request):
    return render(request, 'cat_check.html',
                  context={})

def web_collocations(request):
    return render(request, 'cat_collocations.html',
                  context={})