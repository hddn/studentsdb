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
         'image': 'img/ah.jpg'},
         {'id': 2,
         'first_name': u'Скарлетт',
         'last_name': u'Йоханссон',
         'ticket': 11,
         'image': 'img/sy.jpg'},
         {'id': 3,
         'first_name': u'Майкл',
         'last_name': u'Джордан',
         'ticket': 23,
         'image': 'img/mj.jpg'},
         )
    return render(request, 'students/students_list.html', {'students': students})


def students_add(request):
    return HttpResponse('<h2>Add student</h2>')


def students_edit(request, sid):
    return HttpResponse('<h2>Edit student %s</h2>' % sid)


def students_delete(request, sid):
    return HttpResponse('<h2>Delete student %s</h2>' % sid)



def groups_list(request):
    return HttpResponse('<h2>Groups List</h2>')


def groups_add(request):
    return HttpResponse('<h2>Add group</h2>')


def groups_edit(request, gid):
    return HttpResponse('<h2>Edit group %s</h2>' % gid)


def groups_delete(request, gid):
    return HttpResponse('<h2>Delete group %s</h2>' % gid)

