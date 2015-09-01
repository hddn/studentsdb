# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def students_list(request):
    students = (
        {'id': 1,
         'first_name': u'Ентоні',
         'last_name': u'Хопкінс',
         'ticket': 42,
         'group': 'ЗСІ-11',   
         'image': 'img/ah.jpg'},
         {'id': 2,
         'first_name': u'Скарлетт',
         'last_name': u'Йоханссон',
         'ticket': 11,
         'group': 'ЗСІ-12',
         'image': 'img/sy.jpg'},
         {'id': 3,
         'first_name': u'Майкл',
         'last_name': u'Джордан',
         'ticket': 23,
         'group': 'ЗСІ-13',
         'image': 'img/mj.jpg'},
         )
    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h2>Add student</h2>')


def students_edit(request, sid):
    return HttpResponse('<h2>Edit student %s</h2>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h2>Delete student %s</h2>' % sid)

