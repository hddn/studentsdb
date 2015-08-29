from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def students_list(request):
    return render(request, 'students/students_list.html', {})


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

