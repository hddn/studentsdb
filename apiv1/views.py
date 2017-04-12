from rest_framework import permissions
from rest_framework import viewsets

from apiv1.serializers import StudentSerializer, GroupSerializer, ExamSerializer, JournalSerializer
from students.models import Student, Group, Exam, MonthJournal


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticated,)


class ExamViewSet(viewsets.ModelViewSet):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = (permissions.IsAuthenticated,)


class JournalViewSet(viewsets.ModelViewSet):
    queryset = MonthJournal.objects.all()
    serializer_class = JournalSerializer
    permission_classes = (permissions.IsAuthenticated,)
