from rest_framework import generics, viewsets
from datetime import datetime, time, timedelta
from django.db.models import Q
from .models import Actions, Photos
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import IdleControlSerializers


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Actions.objects.all().order_by("-id")
    serializer_class = IdleControlSerializers
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")


class ActionsWithPhotos(APIView):

    def post(self, request):
        camera = request.data.get('camera')
        start_tracking = request.data.get('start_tracking')
        stop_tracking = request.data.get('stop_tracking')
        photos = request.data.get('photos')
        action = Actions.objects.create(camera=camera, start_tracking=start_tracking, stop_tracking=stop_tracking)
        for photo in photos:
            image = photo.get('image')
            photo = Photos.objects.create(image=image, idle_id=action)
        return Response({"message": "Data created successfully"}, status=status.HTTP_201_CREATED)


class IdleActionListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        start_of_day = datetime.combine(date_obj, time.min)
        end_of_day = datetime.combine(date_obj, time.max)

        queryset = Actions.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by('date_created').order_by("-id")

        serializer = IdleControlSerializers(queryset, many=True)
        return Response(serializer.data)
