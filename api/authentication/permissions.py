from rest_framework.permissions import BasePermission

class AllowAny(BasePermission):
    """
    Allow any access.
    This isn't strictly required, since you could use an empty
    permission_classes list, but it's useful because it makes the intention
    more explicit.
    """

    def has_permission(self, request, view):
        return True

class IsAuthenticated(BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)

class IsModeratorUser(BasePermission):
    """
    Allows access only to moderator users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


