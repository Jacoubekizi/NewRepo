from import_export import resources, widgets
from import_export.fields import Field
from import_export.widgets import ForeignKeyWidget
from .models import*


class InformationResource(resources.ModelResource):

    user = Field(
        column_name='username',
        attribute='user',
        widget=ForeignKeyWidget(InformationStudent, field='user')
    )

    desires_student = Field(
        column_name='desires',
        attribute='desires',
        widget=widgets.ManyToManyWidget(Dseires, field='desire', separator=',')
    )

    username = Field(
        column_name='student',
        attribute='student',
        widget=ForeignKeyWidget(Students_University, field='username')
    )
    class Meta:
        model = InformationStudent
        fields = ['id' ,'user' 'desires_student', 'final_average', 'username']




class AdmissionsResource(resources.ModelResource):

    user = Field(
        column_name='nameStudent',
        attribute='user',
        widget=ForeignKeyWidget(model=Student, field='user')
    )

    class Meta:
        model = Admissions
        fields = ['user', 'desire']





class DseiresResource(resources.ModelResource):

    university = Field(
        column_name='university',
        attribute='university',
        widget=ForeignKeyWidget(model=University, field='university')
    )
    class Meta:
        model = Dseires
        fields = ['id','desire', 'type_reg', 'number_of_student', 'university']






class StudentResource(resources.ModelResource):
    class Meta:
        model = Students_University
        fields = ['id' ,'Id_Number','username', 'average', 'exam']