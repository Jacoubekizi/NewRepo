from rest_framework.permissions import BasePermission

class IsStudent(BasePermission):
    def has_permission(self, request, view):

        return bool(request.user and request.user.is_student)
    

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        
        return bool(request.user and request.user.is_employee)
    