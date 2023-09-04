import django
from django.contrib import admin

from django.contrib.auth.models import Group, Permission
from django.core.handlers.wsgi import WSGIRequest
from .models import *
from import_export.admin import ImportExportMixin, ExportMixin
from .resource import  *
from django_object_actions import DjangoObjectActions, action
from .views import sorting
from imagekit.admin import AdminThumbnail
# Register your models here.



class MyAdminSite(admin.AdminSite):
    site_header = "Welcome Site Adminstration"  #login
    
    site_title = "Welcome Site Adminstration"
    index_title = "Welcome Site Adminstration"

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.is_active and request.user.is_staff and request.user.is_superuser

admin.site = MyAdminSite(name='blog-admin')


class PostAdminSite(admin.AdminSite):
    site_header = "Welcome To Admin Site"
    site_title = "Blog Admin"
    index_title = "Welcome To Admin Site"

    def has_permission(self, request: WSGIRequest) -> bool:
        return request.user.is_active and request.user.is_staff and request.user.is_admin

post_admin_site = PostAdminSite(name='post-admin')


class InformationAdmin(DjangoObjectActions, ExportMixin, admin.ModelAdmin):
    resource_classes = [InformationResource,]

    @action(label="Sorting", description="Submit this article")
    def make_published(self, request, obj):
       sorting()

    changelist_actions=('make_published',)


    fieldsets = (
        ('Section1',{'fields':['user', 'desires', 'photo', 'master_entrance_photo', 'nonworking_document_photo', 'payment_receipt_photo']}),
    )

    list_display = ['user', 'student', 'user_name', 'final_average', 'student_desires', 'photo_one', 'photo_two', 'photo_three', 'photo_four']
    photo_one = AdminThumbnail(image_field='image')
    photo_two = AdminThumbnail(image_field='image_one')
    photo_three = AdminThumbnail(image_field='image_two')
    photo_four = AdminThumbnail(image_field='image_three')

    list_per_page = 2

class StudentAdmin(ImportExportMixin, admin.ModelAdmin ):
    resource_class = StudentResource
    list_display = ['username','id' , 'Id_Number', 'average', 'exam']
    
    list_per_page = 5


class UniversityAdmin(admin.ModelAdmin):

    fieldsets = (
        ('Add Name University', {'fields':['university',]}),
    )

    list_display = ['id', 'university']
    search_fields = ['university',]


class DesiresAdmin(ImportExportMixin,admin.ModelAdmin):

    resource_class = DseiresResource

    list_display = ['desire', 'id','type_reg', 'number_of_student', 'university']
    fieldsets = (

        ('Add Name Desire', {
            
            'fields':['desire'],
            'classes':['wide']}
        ),

        ('Informaion Desire', {

            'fields':['type_reg', 'number_of_student', 'university'],
            'classes':['wide'],
            'description':'All about the details of the desire'}
        ),
    )

    search_fields = ['desire',]

class AdmissionAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = AdmissionsResource

    list_display = ['user', 'desire']

admin.site.register(InformationStudent, InformationAdmin)
admin.site.register(University, UniversityAdmin)
admin.site.register(Dseires, DesiresAdmin)
admin.site.register(Admissions, AdmissionAdmin)
admin.site.register(Students_University, StudentAdmin)
admin.site.register(Group)

post_admin_site.register(InformationStudent, InformationAdmin)
post_admin_site.register(University, UniversityAdmin)
post_admin_site.register(Dseires, DesiresAdmin)
post_admin_site.register(Admissions, AdmissionAdmin)
post_admin_site.register(Students_University, StudentAdmin)


# models = django.apps.apps.get_models()

# for model in models:
#     try:
#         blog_admin.register(model)
#     except admin.sites.AlreadyRegistered:
#         pass
