import logging

from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Profile

logger = logging.getLogger(__name__)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def login_with_jwt(request):
    """Exchange the Supabase access token for a Django session ID cookie.
    This endpoint expects a Supabase access token to be sent
    in the Authorization header.
    Upon successful authentication, it creates a Django session
    for the authenticated user.

    :param request: An HTTP request object containing the JWT token in the headers.
    :return: An empty response indicating the success of the authentication process.
    """
    auth_login(request, request.user)
    return Response()


@api_view(["GET"])
def anonymous_view(request):
    logger.info("anonymous_view user: %s", request.user.__dict__)
    token = getattr(request.user, "token", None)
    payload = token.payload if token else {}
    return Response(payload)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def authenticated_view(request):
    logger.info("authenticated_view user: %s", request.user.__dict__)
    user = request.user
    return Response({"id": user.id, "payload": request.user.token.payload})


class ProfileView(LoginRequiredMixin, UpdateView):
    """View to display and update the authenticated user profile."""

    template_name = "profile.html"
    model = Profile
    fields = ("preferred_username",)
    success_url = "."

    def get_object(self, queryset=None) -> Profile:
        """Retrieves the user's profile.
        Creates a new profile if no profile exists for the user.
        """
        obj, _ = self.model.objects.get_or_create(user=self.request.user)
        return obj
