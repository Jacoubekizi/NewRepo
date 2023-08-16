from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404
from .models import *

editors, created = Group.objects.get_or_create(name='Employee')


content_type_one = ContentType.objects.get_for_model(University)
post_permission = Permission.objects.filter(content_type=content_type_one)

content_type_two = ContentType.objects.get_for_model(Dseires)
post_permission_two = Permission.objects.filter(content_type=content_type_two)

content_type_three = ContentType.objects.get_for_model(InformationStudent)
permission = Permission.objects.filter(content_type=content_type_three)

content_type_four = ContentType.objects.get_for_model(Admissions)
permission_one = Permission.objects.filter(content_type = content_type_four)

content_type_five = ContentType.objects.get_for_model(Students_University)
permission_two = Permission.objects.filter(content_type = content_type_five)


for perm in post_permission:
    editors.permissions.add(perm)

for perm in post_permission_two:
    editors.permissions.add(perm)

for perm in permission:
    if perm.codename == "delete_informationstudent" or perm.codename == "view_informationstudent":
        editors.permissions.add(perm)

for perm in permission_one:
    if perm.codename == "view_admissions":
        editors.permissions.add(perm)

for perm in permission_two:
    if perm.codename == "view_students_university" or perm.codename == "add_students_university":
        editors.permissions.add(perm)