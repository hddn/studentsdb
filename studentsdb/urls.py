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
from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView, TemplateView
from django.views.i18n import JavaScriptCatalog

from students.views.students import StudentUpdateView, StudentDeleteView, StudentAddView, StudentsListView
from students.views.groups import GroupUpdateView, GroupDeleteView, GroupAddView, GroupsListView
from students.views.exams import exams_list
from students.views.journal import JournalView
from students.views.contact_admin import ContactView
from students.forms.login import LoginForm


urlpatterns = [
    url(r'^$', StudentsListView.as_view(), name='home'),
    url(r'^students/add/$', login_required(StudentAddView.as_view()), name='students_add'),
    url(r'^students/(?P<pk>\d+)/edit/$', login_required(StudentUpdateView.as_view()), name='students_edit'),
    url(r'^students/(?P<pk>\d+)/delete/$', login_required(StudentDeleteView.as_view()), name='students_delete'),

    url(r'^groups/$', login_required(GroupsListView.as_view()), name='groups'),
    url(r'^groups/add/$', login_required(GroupAddView.as_view()), name='groups_add'),
    url(r'^groups/(?P<pk>\d+)/edit/$', login_required(GroupUpdateView.as_view()), name='groups_edit'),
    url(r'^groups/(?P<pk>\d+)/delete/$', login_required(GroupDeleteView.as_view()), name='groups_delete'),

    url(r'^journal/(?P<pk>\d+)?/?$', login_required(JournalView.as_view()), name='journal'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^exams/$', login_required(exams_list), name='exams'),

    url(r'^contact-admin/$', login_required(ContactView.as_view()), name='contact_admin'),

    url(r'^jsi18n/$', JavaScriptCatalog.as_view(), name='javascript_catalog'),

    url(r'^users/profile/$', login_required(TemplateView.as_view(
        template_name='registration/profile.html')), name='profile'),
    url(r'^users/login/$', auth_views.login, kwargs={'authentication_form': LoginForm}, name='auth_login'),
    url(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    url(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    url(r'^users/', include('registration.backends.simple.urls', namespace='users')),

    url('^social/', include('social_django.urls', namespace='social')),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
