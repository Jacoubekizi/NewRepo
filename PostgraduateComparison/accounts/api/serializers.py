from rest_framework import serializers
from accounts.models import CustomUser, Student
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError, smart_bytes
from rest_framework.exceptions import AuthenticationFailed
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from accounts.utils import Utlil
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email']



class StudentSignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type":"password"}, write_only=True)
    
    class Meta:
        model=CustomUser
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password':{'write_only':True,}
        }

    def validate(self, attrs):
        eamil = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum:
            raise serializers.ValidationError('The username should only contain alphanumeric characters')
        return attrs

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)

    def save(self, **kwargs):
        user = CustomUser(
            username=self.validated_data['username'],
            email = self.validated_data['email']
        )
        password = self.validated_data['password']
        user.set_password(password)
        user.is_student = True
        user.save()
        Student.objects.create(user=user)
        return user

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
    
class UserLoginSerilizer(serializers.Serializer):

    email = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self, data):

        email = data.get('email', )
        password = data.get('password', )

        if email is None:
            raise serializers.ValidationError({'message_error':'An email address is required to log in.'})
        
        if password is None:
            raise serializers.ValidationError({'message_error':'A password is required to log in.'})
        
        user = authenticate(username= email, password= password)

        if user is None:
            raise serializers.ValidationError({'message_error':'A user with this email and password was not found.'})
        
        if not user.is_active:
            raise serializers.ValidationError({'message_error':'Thid user is not currently actinated.'})
        
        return user
    


class StudentSerializer(serializers.ModelSerializer):
    student = serializers.CharField(source='user.username')
    class Meta:
        model = Student
        fields = ['id', 'student']


class ChangePassword(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, required=True)
    password1 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:

        model = CustomUser
        fields = ['old_password', 'password', 'password1']


    def validate(self, attrs):

        password = attrs['password']
        password1 = attrs['password1']
        if password and password1 and password != password1:
            raise serializers.ValidationError({'password': "password fields didn't match."})
        
        return attrs


    def validate_old_password(self, value):

        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"Old Password": "old password is not correct"})
        
        return value
    

    def update(self, instance, validated_data):

        instance.set_password(validated_data['password'])
        instance.save()

        return instance
    
class UpdateUserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username','first_name', 'last_name']
# .filter(email=value).exists()
    def validat_email(self, value):
        user = self.context['request'].user
        users = CustomUser.objects.exclude(pk=user.pk)
        if users :
            for user_one in users:
                if user_one.email == value is not None:
                    raise serializers.ValidationError({"email":"this email is already in user."})
        return value
    

    def update(self, instance, validated_data):
        
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']

        instance.save()

        return instance

class EmailVerifecatonSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token', ]

class ResetPasswordEmail(serializers.Serializer):
    email = serializers.EmailField(min_length=20)

    class Meta:
        fields = ['email',]

    def validate(self, attrs):
        # try:
            email = attrs.get('email', '')
            if CustomUser.objects.filter(email=email).exists:
                user = CustomUser.objects.get(email=email)
                uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(request=self.context['request']).domain
                relativelink = reverse('reset-password', kwargs={'uidb64':uidb64, 'token':token})
                absurl = 'http://'+current_site+relativelink
                email_body = 'Hi '+user.username+' Use the link below to reset your password \n'+ absurl
                data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Reset your password'}
                Utlil.send_eamil(data)
        #     return attrs
        # except Exception as identifier:
        #     pass
            return super().validate(attrs)
    

class SetNewPasswordSerializer(serializers.Serializer):
    
    password = serializers.CharField(min_length=6, max_length=16, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password', '')
            token = attrs.get('token', '')
            uidb64 = attrs.get('uidb64', '')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)