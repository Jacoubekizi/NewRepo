from accounts.api.serializers import *
from .models import *
from .serializer import *
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions
from accounts.api.permission import IsStudent
from .validations import *
import json
from rest_framework.views import Http404
# from django.views.decorators.cache import cache_page
# from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view
# # Create your views here.

# Registration for the comparison

class Update_Information_Student(APIView):
    def get_object(self, user_id):
        try:
            return InformationStudent.objects.get(id=user_id)
        except InformationStudent.DoesNotExist:
            raise Http404
        
    def get(self, request, user_id=None):
        information_student = self.get_object(user_id)
        serializer = InfoStudentSerializer(information_student)
        return Response(serializer.data)

    def put(self, request, user_id=None):
        information_student = self.get_object(user_id)
        serializer = InfoStudentSerializer(information_student, data=request.data)
        if serializer.is_valid():
            serializer.save()
            information_student.is_update = True
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class Register(APIView):

    permission_classes = [permissions.IsAuthenticated, IsStudent]

    def post(self, request):
        data = request.data
        user_q = request.user
        # print(type(user))
        user_one = Student.objects.get(user__email=user_q.email)
        des = json.loads(data['desires'])
        # des = data['desires']
        list_desire = validate_desires(des)
        final_average = finale_average(data)
        user = student(data)
        serializer = InfoStudentSerializer(data={
                                            'user':user_one.id,
                                            'student':user,
                                            'id_number':data['idnumber'],
                                            'user_name':data['username'],
                                            'final_average':final_average,
                                            'photo':data['photo'],
                                            'master_entrance_photo':data['photo_one'],
                                            'nonworking_document_photo':data['photo_two'],
                                            'payment_receipt_photo':data['photo_three'],
                                            'desires':list_desire}, many=False, context={'request': request})
        if serializer.is_valid():
            serializer.save()   
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
def sorting():
    
    for student in InformationStudent.objects.all().order_by('-final_average'):
        for d in student.desires.all():
                adminassion = Admissions.objects.filter(desire=d).count()
                if d.number_of_student>adminassion:
                    serializer = AdmissionSerializer(data=
                                                        {
                                                        'user':student.user.id,
                                                        'desire':d.desire
                                                        })
                    if serializer.is_valid():
                        serializer.save()
                    break

# @method_decorator( cache_page(60*5), name='dispatch')
class GetDesires(APIView):
    def get(self, request):
        desires = Dseires.objects.all()
        serializer = StuDesSerializer(desires, many=True)
        data = serializer.data
        return Response(data)


# add universiyt and list all universitys

# class AddUniversity(APIView):

#     permission_classes = (permissions.IsAuthenticated,)
#     def post(self, request):
#             serializer = UniversitySerializer(data=request.data)
#             if serializer.is_valid():
#                 serializer.save()
#             # data = serializer.data
#             return Response(serializer.data)
                
#     def get(self, request):
        # one = University.objects.all()
#         serializer = UniversitySerializer(one, many=True)
#         # data = serializer.data
        # return Response({"universitys":serializer.data})


# # add desires belonging to a particular university
# class University_Desires(APIView):

#     permission_classes = (permissions.IsAuthenticated,)

#     def get(self, request, univer_id):

#         university = get_object_or_404(University, pk=univer_id)
#         univer = university.university_name.all()
#         serializer = StuDesSerializer(univer, many=True)
#         return Response(serializer.data)
    
#     def post(self, request, univer_id):
#         university = get_object_or_404(University, id=univer_id)
#         serializer = StuDesSerializer(data={
#             'desire':request.data['desire'],
#             'type_reg':request.data['type_reg'],
#             'number_of_student':request.data['number'],
#             'university':univer_id      
#         })
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)

