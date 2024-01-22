from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import SocialPost
from .serializers import SocialPostSerializer


class SocialPostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    pagination_class = None
    queryset = SocialPost.objects.all()
    serializer_class = SocialPostSerializer
