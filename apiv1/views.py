from django.contrib.auth.models import User
from rest_framework import permissions, viewsets
from rest_framework.generics import CreateAPIView

from apiv1 import serializers
from students.models import Student, Group, Exam, MonthJournal


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = serializers.StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = serializers.ExamSerializer
    permission_classes = (permissions.IsAuthenticated,)


class JournalViewSet(viewsets.ModelViewSet):
    queryset = MonthJournal.objects.all()
    serializer_class = serializers.JournalSerializer
    permission_classes = (permissions.IsAuthenticated,)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class RegisterUserView(CreateAPIView):
    serializer_class = serializers.RegisterUserSerializer
    permission_classes = (permissions.AllowAny,)
