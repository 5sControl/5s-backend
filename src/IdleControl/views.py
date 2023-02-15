from rest_framework import generics, viewsets
from .models import Actions, Photos
from datetime import datetime
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import IdleControlSerializers, PhotoSerializers


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Actions.objects.all()
    serializer_class = IdleControlSerializers

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")

    def destroy(self, request, *args, **kwargs):
        raise MethodNotAllowed("DELETE")


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


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializers
