from rest_framework import serializers

from students.models import Student, Group, Exam


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'middle_name',
                  'birthday', 'photo', 'ticket', 'notes', 'student_group')


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'title', 'leader', 'notes')


class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = ('id', 'subject', 'teacher', 'date', 'group', 'notes')
