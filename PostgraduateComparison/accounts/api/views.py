from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import *
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .validation import custom_validation
from application.group import editors
from rest_framework.views import APIView
from accounts.utils import Utlil
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
import random
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
User = get_user_model()
from django.contrib.auth.tokens import PasswordResetTokenGenerator



class StudentSignupView(generics.GenericAPIView):

    """
    An endpoint for the client to create a new Student.
    """
    permission_classes = [permissions.AllowAny]
    serializer_class = StudentSignupSerializer

    def post(self, request, *args, **kwargs):
        clean_data = custom_validation(request.data)
        serializer = self.get_serializer(data=clean_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = CustomUser.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user)
        current_site = get_current_site(request).domain
        relativelink = reverse('email-verify')
        absurl = 'http://'+current_site+relativelink+'?token='+str(token.access_token)
        rand_num = random.randint(1,10000)
        email_body = 'Hi '+user.username+' Use the link below to verify your email \n'+ absurl
        data = {'email_body':email_body, 'to_email':user.email, 'email_subject':'Verify your email'}
        Utlil.send_eamil(data)
        data_user = serializer.data
        data_user['tokens'] = {"refresh" : str(token), "access":str(token.access_token)}
        return Response(
            {
                "user": data_user,
                "message":"account created successfully"
            })


class VerifyEamil(APIView):

    serializer_class = EmailVerifecatonSerializer

    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload =jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            user = CustomUser.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.save()
                # reverse('auth-login-token')
                return Response({'email':'Successfylly activated'}, status=status.HTTP_200_OK)
            
        except jwt.ExpiredSignatureError as identifier:
                return Response({'error':'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
                return Response({'error':'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

class UserLoginApiView(generics.GenericAPIView):
    """
    An endpoint to authenticate existing users their email and passowrd.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerilizer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {'refresh':str(token), 'access':str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):

    """An endpoint to logout Users"""

    permission_classes = [permissions.IsAuthenticated,]
    def post(self, request):
       try:
           refresh_token = request.data['refresh']
           token = RefreshToken(refresh_token)
           token.blacklist()
           return Response({"message":"Goode by"},status=status.HTTP_205_RESET_CONTENT)
       except Exception as e:
           return Response( status=status.HTTP_400_BAD_REQUEST)
    

class Change_Password(APIView):

    # queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, user_pk):

        data = request.data
        user_one = CustomUser.objects.get(id=request.user.id)
        serializer = ChangePassword(user_one ,data=data, many=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                
                {
                    "success":"The Changed Password has been successfully"
                },
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class UpdateUser(APIView):

    permission_classes=[permissions.IsAuthenticated]


    def put(self, requset, user_pk):

        user_pk = requset.user.pk
        user = CustomUser.objects.get(pk=user_pk)
        serializer = UpdateUserSerializer(user, data=requset.data, many=False, context={'request':requset})
        if serializer.is_valid():
            serializer.save()
            return Response(

                {'success':"The changed information has been successfully."},
                status=status.HTTP_200_OK
            )
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmail

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        return Response({'success':'we have sent you a link to reset your password'},
                        status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success':True, 'message':'Credentials valid', 'uidb54':uidb64, "token":token}, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({'error':'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

class SetNewPassword(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message':'Password reset success'}, status=status.HTTP_200_OK)