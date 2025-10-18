from rest_framework.permissions import BasePermission

class IsSupport(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and getattr(request.user, "role", None) == "SUPPORT"
        )
    

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.is_superuser)


class SupportHasScopes(BasePermission):
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated and getattr(request.user, "role", None) == "SUPPORT"):
            return False
        prof = getattr(request.user, "support_profile", None)
        required = getattr(view, "required_scopes", [])
        if prof is None:
            return False
        return all(scope in (prof.scopes or []) for scope in required)