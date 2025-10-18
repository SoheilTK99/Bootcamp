from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from accounts.permissions import IsSupport, SupportHasScopes
from .serializers import SupportUserSerializer

User = get_user_model()

class SupportPingView(APIView):
    permission_classes = [permissions.IsAuthenticated, IsSupport]
    def get(self, request):
        prof = getattr(request.user, "support_profile", None)
        return Response({"ok": True, "user": request.user.username, "scopes": prof.scopes if prof else []})

class SupportUserViewSet(viewsets.ModelViewSet):
    serializer_class = SupportUserSerializer
    queryset = User.objects.filter(role="END_USER")
    http_method_names = ["get", "patch", "delete", "head", "options"]  # محدود

    permission_classes = [permissions.IsAuthenticated, IsSupport, SupportHasScopes]
    required_scopes = []  #  پیش‌فرض

    def get_required_scopes(self):
        if self.action in ("list", "retrieve"):
            return ["users.read"]
        elif self.action in ("partial_update", "update"):
            return ["users.write"]
        elif self.action == "destroy":
            return ["users.delete"]
        return []

    def get_permissions(self):
        # به SupportHasScopes بگو چه scopeهایی لازم است
        for p in self.permission_classes:
            pass
        self.required_scopes = self.get_required_scopes()
        return [perm() for perm in self.permission_classes]
