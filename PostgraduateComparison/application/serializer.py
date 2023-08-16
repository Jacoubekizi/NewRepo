from rest_framework import serializers
from .models import InformationStudent, Admissions, Dseires, University

class AdmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Admissions
        fields = ['user', 'desire']

class UniversitySerializer(serializers.ModelSerializer):

    class Meta :
        model = University
        fields = '__all__'


class StuDesSerializer(serializers.ModelSerializer):

    universitys = UniversitySerializer(many=True, read_only=True)
    class Meta:
        model = Dseires
        fields = '__all__'


class InfoStudentSerializer(serializers.ModelSerializer):
    desier =StuDesSerializer(many=True, read_only=True)
    username = serializers.CharField(source='user.user.name', read_only=True)

    class Meta:
        model = InformationStudent
        # fields = ['user', 'username','average', 'university_degree', 'exam', 'final_average', 'desires', 'photo', 'master_entrance_photo', 'nonworking_document_photo', 'payment_receipt_photo']
        fields = '__all__'
        

    


