from rest_framework import generics, viewsets
from datetime import datetime, time, timedelta
from django.db.models import Q
from src.Image.models import Photos
from src.Cameras.models import Camera
from src.Algorithms.models import Algorithm
from src.Reports.models import Report
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from src.Reports.serializers import ReportSerializers


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by("-id")
    serializer_class = ReportSerializers
    # permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PUT")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")


class ActionsWithPhotos(APIView):

    def post(self, request):
        algorithm = Algorithm.objects.get(name=request.data.get('algorithm'))
        camera = Camera.objects.get(id=request.data.get('camera'))
        start_tracking = request.data.get('start_tracking')
        stop_tracking = request.data.get('stop_tracking')
        photos = request.data.get('photos')
        violation_found = request.data.get('violation_found')
        extra = (request.data.get('extra')['equipment'])
        action = Report.objects.create(camera=camera, extra=extra, algorithm=algorithm, violation_found=violation_found, start_tracking=start_tracking, stop_tracking=stop_tracking)
        for photo in photos:
            image = photo.get('image')
            date = photo.get('date')
            photo = Photos.objects.create(image=image, date=date, report_id=action)
        return Response({"message": "Data created successfully"}, status=status.HTTP_201_CREATED)


class IdleActionListView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d').date()
        start_of_day = datetime.combine(date_obj, time.min)
        end_of_day = datetime.combine(date_obj, time.max)

        queryset = Report.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by('date_created').order_by("-id")

        serializer = ReportSerializers(queryset, many=True)
        return Response(serializer.data)
