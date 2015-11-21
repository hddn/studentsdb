"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from students.views.students import StudentUpdateView, StudentDeleteView, StudentAddView, students_list
from students.views.groups import GroupUpdateView, GroupDeleteView, GroupAddView, groups_list
from students.views.exams import exams_list
from students.views.journal import JournalView
from students.views.contact_admin import ContactView

from .settings import MEDIA_ROOT, DEBUG


js_info_dict = {
    'packages': ('students',),
}

urlpatterns = patterns('',
    url(r'^$', students_list, name='home'),
    url(r'^students/add/$', login_required(StudentAddView.as_view()), 
        name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$',
        login_required(StudentUpdateView.as_view()), 
        name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$',
        login_required(StudentDeleteView.as_view()), 
        name='students_delete'),

    url(r'^groups/$', login_required(groups_list), name='groups'),
    url(r'^groups/add/$', login_required(GroupAddView.as_view()), 
        name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$',
        login_required(GroupUpdateView.as_view()), 
        name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', 
        login_required(GroupDeleteView.as_view()), 
        name='groups_delete'),

    url(r'^journal/(?P<pk>\d+)?/?$', 
        login_required(JournalView.as_view()), name='journal'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^exams/$', login_required(exams_list), name='exams'),

    url(r'^contact-admin/$', login_required(ContactView.as_view()), 
        name='contact_admin'),

    url(r'^jsi18n\.js$', 'django.views.i18n.javascript_catalog', js_info_dict),

    url(r'^users/profile/$', login_required(TemplateView.as_view(
        template_name='registration/profile.html')), name='profile'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'},
        name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'),
        name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', 
        namespace='users')),

    url('^social/', include('social.apps.django_app.urls',
        namespace='social')),   
    )

if DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': MEDIA_ROOT}))