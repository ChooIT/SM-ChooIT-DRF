from rest_framework.permissions import BasePermission

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True
        elif request.user.is_authenticated:
            return str(obj.user_no) == str(request.user.email)
        else:
            return False


class MethodDependPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        elif request.method == 'POST':
            if request.user.is_authenticated:
                return True
            return False
