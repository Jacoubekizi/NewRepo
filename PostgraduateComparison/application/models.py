from django.db import models
from accounts.models import  Student
from imagekit.models.fields import ImageSpecField
from imagekit.processors import ResizeToFill


# Create your models here.

# Model for Infromations Universitys
class University(models.Model):
    university = models.CharField(max_length=100)

    def __str__(self):
        return self.university


# Model for Desires Informations
class Dseires(models.Model):

    choice = (
        ('عام' , 'عام'),
        ('موازي', 'موازي')
    )

    desire = models.CharField(max_length=255)
    type_reg = models.CharField(max_length=20, choices=choice)
    number_of_student = models.IntegerField()
    university = models.ForeignKey(University, related_name="university_name", on_delete=models.CASCADE)
    

    def __str__(self):
        return self.desire


# Model for Information Students get from university
class Students_University(models.Model):
    Id_Number = models.BigIntegerField(unique=True)
    username = models.CharField(verbose_name='Username', max_length=255)
    average = models.DecimalField(verbose_name='Average', max_digits=5, decimal_places=3)
    exam = models.DecimalField(verbose_name="National examination score", max_digits=4, decimal_places=2, null=True, blank=True)

    def __str__(self) -> str:
        return self.username


# Model for Information Students
class InformationStudent(models.Model):
 
    user = models.OneToOneField(Student, related_name="informationstudent", on_delete=models.CASCADE)
    student =models.OneToOneField(Students_University, related_name='stu', on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, help_text="أدخل الاسم الثلاثي")
    id_number = models.BigIntegerField(unique=True)
    is_update = models.BooleanField(default=False)
    final_average = models.DecimalField(verbose_name="Final Average", max_digits=5, decimal_places=3, default=0.0)
    desires = models.ManyToManyField(Dseires, related_name="student_desire")
    photo = models.ImageField(blank=True, help_text='أدخل صورة مصدقة عن وثيقة التخرج', null=True, upload_to='images')
    image = ImageSpecField(source='photo', processors=[ResizeToFill(300,200)], format='PNG', options={'quality':60})
    master_entrance_photo =models.ImageField(blank=True, help_text='أدخل صورة مصدقة عن امتحان قيد الماجستير', null=True, upload_to='images')
    image_one = ImageSpecField(source='master_entrance_photo', processors=[ResizeToFill(300,200)], format='PNG', options={'quality':60})
    nonworking_document_photo = models.ImageField(blank=True, help_text='صورة عن وثيقة غير عامل أو موافقة الجهة التي يعمل لديها الطالب', null=True, upload_to='images')
    image_two = ImageSpecField(source='nonworking_document_photo', processors=[ResizeToFill(300,200)], format='PNG', options={'quality':60})    
    payment_receipt_photo = models.ImageField(blank=True, help_text='صورة عن إيصال دفع خاص بطلاب الموازي', null=True, upload_to='images')
    image_three = ImageSpecField(source='payment_receipt_photo', processors=[ResizeToFill(300,200)], format='PNG', options={'quality':60})

    def __str__(self):
        return self.user.user.username

    def student_desires(self):
        return ",".join([str(p) for p in self.desires.all()])
    
    
    class Meta:
        ordering = ['-final_average']



class Admissions(models.Model):
    user = models.OneToOneField(Student, related_name="admissions", on_delete=models.CASCADE)
    desire = models.CharField(max_length=255)

    def __str__(self):
        return self.user.user.username
    