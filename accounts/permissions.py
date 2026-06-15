from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsManager(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_manager() or request.user.is_superuser())
    message = "You do not have permission to perform this action."

class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (request.user.is_customer() or request.user.is_superuser())
    message = "You do not have permission to perform this action."

class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated and (request.user.is_manager() or request.user.is_superuser())
    message = "You do not have permission to perform this action." 