from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import StudentSignupSerializer, CustomUserSerializer, UserLoginSerilizer, StudentSerializer
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from .validation import custom_validation
from application.group import editors
User = get_user_model()


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
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data['tokens'] = {"refresh" : str(token), "access":str(token.access_token)}
        return Response(
            {
                "user": data,
                "message":"account created successfully"
            })


class UserLoginApiView(generics.GenericAPIView):
    """
    An endpoint to authenticate existing users their email and passowrd.
    """
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserLoginSerilizer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
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
    

    
