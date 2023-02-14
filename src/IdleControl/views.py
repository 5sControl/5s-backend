from rest_framework import generics, viewsets
from .models import Actions, Photos
from rest_framework import status
from rest_framework.response import Response
from .serializers import IdleControlSerializers, PhotoSerializers


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Actions.objects.all()
    serializer_class = IdleControlSerializers

    def create(self, request, *args, **kwargs):
        camera = request.data.get('camera')
        start_tracking = request.data.get('start_tracking')
        stop_tracking = request.data.get('stop_tracking')
        photos_data = request.data.get('photos')

        action = Actions.objects.create(
            camera=camera,
            start_tracking=start_tracking,
            stop_tracking=stop_tracking
        )
        if photos_data:
            for photo_data in photos_data:
                Photos.objects.create(
                    image=photo_data.get('image'),
                    idle_id=action
                )

        return Response(status=status.HTTP_201_CREATED)


class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photos.objects.all()
    serializer_class = PhotoSerializers
