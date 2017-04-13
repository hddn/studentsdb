from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from apiv1.views import StudentViewSet, GroupViewSet, ExamViewSet, JournalViewSet, UserViewSet


router = DefaultRouter()
router.register(r'students', StudentViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'exams', ExamViewSet)
router.register(r'journal', JournalViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls'))
]
