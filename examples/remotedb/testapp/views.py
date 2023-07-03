import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@login_required
def login_required_view(request):
    return HttpResponse(f"{request.user.pk}")


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
