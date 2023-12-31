import logging

from django.conf import settings
from django.views.generic import TemplateView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

logger = logging.getLogger(__name__)


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


class SignInView(TemplateView):
    template_name = "supabase_signin.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["supabase_url"] = settings.SUPABASE_URL
        context["supabase_key"] = settings.SUPABASE_API_KEY
        return context
