from rest_framework import serializers
from accounts.models import CustomUser, Student
from django.contrib.auth import authenticate


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