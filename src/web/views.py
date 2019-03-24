import os

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django import forms
import json
from collections import defaultdict
import requests

HSE_API_ROOT = os.environ.get("HSELING_API_ROOT", "http://hse-api-web/")


# Create your views here.
def web_index(request):
    return render(request, 'index.html',
                  context={})


def web_main(request):
    return render(request, 'corpus_main.html',
                  context={})


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


class TextForm(forms.Form):
    paste_text = forms.CharField()


def web_upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            task_id = handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('main?task_id=' + task_id)
    else:
        form = UploadFileForm()
    return render(request, 'main.html', {'form': form})


def handle_text_to_check(t):
    url = HSE_API_ROOT + "input_text"
    text = {"text": t}
    content = requests.post(url, json=json.dumps(text), headers={'content-type': 'application/json'})
    content_json = content.json()
    return content_json.get('input_text') # task id


def handle_file_to_check(f):
    files = {'file': f}
    url = HSE_API_ROOT + "input_file"
    content = requests.post(url, files=files)
    return content.json().get('task_id')


def handle_text_to_search(postdata, url):
    if isinstance(postdata,dict):
        if postdata.get('search_collocations'):
            text = {"text": postdata['search_collocations'], "count": postdata.get("n"),
                    "domain": postdata.get('search-domain')}
        elif postdata.get('search'):
            text = {"text": postdata['search']}
        elif postdata.get('lemma1'):
            text = {'text': postdata}
    else:
        text = {'text':postdata}
    content = requests.post(url, json=json.dumps(text), headers={'content-type': 'application/json'})
    return content.json()['found']


def web_intext(request):
    if request.method == 'POST':
        task_id = handle_text_to_check(request.POST['paste_text'])
        if task_id:
            return HttpResponseRedirect('check?task_id=' + task_id)

        else:
            return JsonResponse({"error": "No task id"})
    else:
        return web_check(request)

def web_check(request):
    return render(request, 'cat_check.html',
                  context={})


def web_collocations(request):
    return render(request, 'collocations_info.html',
                  context={})


def make_sents(text):
    texts = dict()
    for found in text:
        if not texts.get(found['id_text']):
            texts[found['id_text']] = defaultdict(str)
        texts[found['id_text']][found['abs_sent_id']] += (' ' + (found['word']))
    out = []
    for k, v in texts.items():
        metadata = handle_text_to_search(k, HSE_API_ROOT + 'search_metadata')
        to_append = {"sents": []}
        to_append.update(metadata[0])
        for key, val in v.items():
            to_append['sents'].append(val.strip())
        out.append(to_append)
    return out


def lex_gram_search(request):
    out, searched = [], ''
    if request.POST['lemma1'].isalnum():  # на поиске пустых строк и пробелов подвисает, не надо их
        searched = request.POST['lemma1']
        if request.POST.get('lemma2'):
            searched += ', {0}'.format(request.POST['lemma2'])
        text = handle_text_to_search(request.POST, HSE_API_ROOT + 'search_text')
        out = make_sents(text)

    return out, searched


def web_search(request):
    if request.method == 'POST':
        if request.POST.get('search'):
            searched = request.POST
            if searched['search'].isalnum():  # на поиске пустых строк и пробелов подвисает, не надо их
                text = handle_text_to_search(searched, HSE_API_ROOT + 'search_text')

                return render(request, 'search_results.html', context={"corpus_search": make_sents(text),
                                                                       "outtext": "По запросу {0} нашлись следующие примеры:".format(
                                                                           request.POST['search'])})
            else:
                return render(request, 'search_results.html', context={"corpus_search": [],
                                                                       "outtext": "Пустой или некорректный запрос"})
        elif request.POST.get('lemma1'):
            out, searched = lex_gram_search(request)
            if out:
                return render(request, 'search_results.html', context={"corpus_search": out,
                                                                       "outtext": "По запросу {0} нашлись следующие примеры:".format(
                                                                           searched)})
            else:
                return render(request, 'search_results.html', context={"corpus_search": [],
                                                                       "outtext": "Пустой или некорректный запрос"})

        else:
            return render(request, 'search.html',
                          context={})
    return render(request, 'search.html',
                  context={})


def web_search_collocations(request):
    if request.method == 'POST':
        searched = request.POST
        if searched['search_collocations'].isalnum():  # на поиске пустых строк и пробелов подвисает, не надо их
            text = handle_text_to_search(searched, HSE_API_ROOT + 'search_collocations')
            return render(request, 'cat_collocations.html',
                          context={"items": text, "searched": searched['search_collocations'],
                                   "out": "По запросу {0} нашлись следующие коллокации:".format(
                                       searched['search_collocations'])})
        else:
            return render(request, 'cat_collocations.html',
                          context={"items": [], "out": "Пустой или некорректный запрос"})
    return render(request, 'cat_collocations.html',
                  context={})


def web_search_morph(request):
    return render(request, 'search_morph.html', context={})
