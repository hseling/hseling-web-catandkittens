from django.db import models
from django.http import HttpResponseRedirect
from web.views import handle_uploaded_file

# Create your models here.
class Record(models.Model):
    text = models.CharField(max_length=140)
    timestamp = models.DateTimeField(auto_now_add=True)


class MetaFile(models.Model):
    """
    Метаданные корпуса (файлы *.txt)
    """
    meta = models.FileField()

    def save(self, request):
        task_id = handle_uploaded_file(request.FILES['meta'])
        return HttpResponseRedirect('main?task_id=' + task_id)


class WordFile(models.Model):
    """
    Корпус с разметкой (файлы *.conll)
    """
    words = models.FileField()

    def save(self, request):
        task_id = handle_uploaded_file(request.FILES['words'])
        return HttpResponseRedirect('main?task_id=' + task_id)


class CollocationFile(models.Model):
    """
    Cписки коллокаций (файлы *.xlsx)
    """
    collocations = models.FileField()

    def save(self, request):
        task_id = handle_uploaded_file(request.FILES['collocations'])
        return HttpResponseRedirect('main?task_id=' + task_id)

class Word2VecFile(models.Model):
    """
    Модель Word2Veс. 3 файла: модель, syn1neg.npy, vectors.npy
    """
    model = models.FileField()
    syn1neg = models.FileField()
    vectors = models.FileField()

    def save(self, request):
        for file in request.FILES.values():
            handle_uploaded_file(file)

class UDPipeFile(models.Model):
    """
    Модель UDPipe (*.udpipe)
    """
    model = models.FileField()
    def save(self, request):
        task_id = handle_uploaded_file(request.FILES['model'])
        return HttpResponseRedirect('main?task_id=' + task_id)
