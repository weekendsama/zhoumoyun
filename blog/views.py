from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from . import models
# Create your views here.


def testview(quests):
    return HttpResponse('<p>hello world</p>')


