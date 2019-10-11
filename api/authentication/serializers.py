from django.contrib.auth.password_validation import validate_password 

from rest_framework import serializers
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from django.contrib.auth import (
        get_user_model, 
        authenticate,)
from django.db.models import Q

from rest_framework.response import Response

from .models import StdUser,Student, Teacher, Faculty, Profession, Mail

User = get_user_model()

class FacultySerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Faculty
        fields = ('name',)

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = Profession
        fields = ('name',)


class CreateUserSerializer(serializers.ModelSerializer):
    read_only_fields = ('date_joined',)

    class Meta(object):
        model = User
        fields = (
            'email',
            'password',
        )

    def create(self, validated_data):

        validate_password(password=validated_data.get('password',), user=validated_data.get('email'), password_validators=None)
        
        email = validated_data.get('email')
        user = User.objects.create_user(**validated_data) 
        user.send_mail(email=email)
        return user

class RecoverySerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)
    
    class Meta(object):
        model = User
        fields = ('email',)
        
    def post(self,data):
        email = data.get('email', None)
                
        user = User.objects.filter(Q(email=email)).distinct()
                                 
        if user.exists() and user.count() == 1:
            user_obj = user.first()                                
            user_obj.send_recovery_password(email=email)
        else:
            raise serializers.ValidationError("This email is not valid")
        
        if user_obj:
            if not user_obj.is_active:
                raise serializers.ValidationError("User not active")
        return data

class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User
        fields = ('code',)

class VerifyUserPassSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=64)

    class Meta(object):
        model = User
        fields = ('code',
                'password',)
    
    def post(self, data, code):
        user = User.objects.get(code=code)

class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = User

        fields = ('email',
                'password',)

        extra_kwargs = {'password': {'write_only' : True}}

    def delete(self, request, pk=None, **kwargs):
        request.user.is_active = False
        request.user.save()
        
        return Response(status = 204)

class TeacherSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False)

    class Meta(object):
        model = Teacher
        fields = (
            'faculty',
        )

class StudentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer(many=False)
    profession = ProfessionSerializer(many=False)

    class Meta(object):
        model = Student
        fields = ( 
            'faculty',
            'profession',
        )

class SendMailSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=64)
    subject = serializers.CharField(max_length=256)
    body = serializers.CharField(max_length=2048)
    
    class Meta(object):
        model = Mail

        fields = '__all__'

    def send(self, data):
        email = data.get('email')
        #user = User.objects.get(email=email).first()
        subject = data.get('subject')
        body = data.get('body')
        return Mail.send_mail(email=email,subject=subject,body=body)

class FindUserSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=20)

    class Meta(object):
        model = User
        
        fields = (
                'email',
                )

    def post(self, data):
         email = data.get('email')                                                          
         user = User.objects.get(email=email).first()
         return UserSerializer(user)    

class UserSerializer(serializers.ModelSerializer):
    date_joined = serializers.ReadOnlyField() 
    student = StudentSerializer(many=False, read_only=True)
    teacher = TeacherSerializer(many=False, read_only=True)

    class Meta(object):
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'patronymic',
            'bio',
            'avatar',
            'date_of_birth',
            
            'date_joined',
            'last_update',
            
            'news_subscription',
            'is_staff',
            'is_active',
            'is_superuser',
            'user_permissions',

            'is_student',
            'is_teacher',
            'student',
            'teacher',

            'password',
        )

        extra_kwargs = {'password': {'write_only': True}}


class UpdateUserSerializer(serializers.ModelSerializer):
   
    class Meta(object):
        model = User
        exclude = (
                'email',
                'password',
                'is_staff', 
                'is_active', 
                'is_superuser', 
                'is_student', 
                'is_teacher',
                'username',
                'last_login',
                'groups',
                'code',
                'user_permissions')

class BulkUpdateSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        exclude = (
                'email',
                'password',
                'is_staff',
                'is_active',
                'is_superuser',
                'is_student',
                'is_teacher',
                'username',
                'last_login',
                'groups',
                'code',
                'user_permissions')
 
class DeleteAllSerializer(serializers.ModelSerializer):
    
    class Meta(object):
        model = User
        fields = ('email',
                  'password')
    
    def delete(self, request, **kwargs):
        request.user.is_active = False
        request.user.save()
        
        return Response(status = 200)
    
