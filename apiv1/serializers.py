from django.contrib.auth.models import User
from rest_framework import serializers

from students.models import Student, Group, Exam, MonthJournal


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


class JournalSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthJournal
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')
        extra_kwargs = {'password': {'write_only': True,
                                     'required': False}}

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        password = validated_data.get('password')
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    password2 = serializers.CharField(label='Confirm password', max_length=16, required=True, write_only=True)

    def validate_email(self, email):
        existing = User.objects.filter(email=email)
        if email and existing:
            raise serializers.ValidationError('This email is already registered')
        return email

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError("The two password fields didn't match.")
        return attrs

    def create(self, validated_data):
        username = validated_data.get('username')
        email = validated_data.get('email')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        password = validated_data.get('password')
        return self.Meta.model.objects.create_user(username=username, email=email, first_name=first_name,
                                                   last_name=last_name, password=password)
