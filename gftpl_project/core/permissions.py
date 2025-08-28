from rest_framework.permissions import BasePermission, SAFE_METHODS


# Create your permissions here.

# -------------------- Admin permissions --------------------
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_admin())

# -------------------- Manager or Admin permissions --------------------
class IsManagerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and (user.is_admin() or user.is_manager()))

# -------------------- Read Manager or Admin permissions --------------------
class ReadOnlyOrAdminManager(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return bool(request.user and request.user.is_authenticated)
        user = request.user
        return bool(user and user.is_authenticated and (user.is_admin() or user.is_manager()))