from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model

UserModel = get_user_model()

def custom_validation(data):
    email = data['email'].strip()
    username = data['username'].strip()
    password = data['password'].strip()
    password2 = data['password2'].strip()

    if not email:
        raise ValidationError({"error_message":"The email address is required for registration."})
    
    if not username:
        raise ValidationError({"error_message":"The username is required for registration."})
    
    if not password:
        raise ValidationError({"error_message":"The field passowrd is required."})
    
    if not password2 :
        raise ValidationError({"error_message":"The field passowrd2 is required."})
    
    if password != password2:
        raise ValidationError({"error_message":"password do not match."})
    
    return data