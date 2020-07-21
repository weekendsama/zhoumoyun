from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def testview(quests):
    return HttpResponse('<p>hello world</p>')
