import requests
from rest_framework import viewsets
from datetime import datetime
from django.db.models import Q
from rest_framework.generics import GenericAPIView

from src.CompanyLicense.decorators import validate_license
from src.Core.const import PRODUCTION, SERVER_URL

from src.ImageReport.models import Image
from src.Cameras.models import Camera
from src.Algorithms.models import Algorithm
from src.Reports.models import Report

from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from src.Reports.serializers import ReportSerializers

from src.Inventory.service import process_item_status
from src.Reports.service import edit_extra, create_skanyreport


class ActionViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all().order_by("-id")
    serializer_class = ReportSerializers
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.status = request.data.get("status", instance.status)
        instance.date_updated = datetime.now()
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        raise MethodNotAllowed("POST")

    def partial_update(self, request, *args, **kwargs):
        raise MethodNotAllowed("PATCH")


class ActionsWithPhotos(APIView):
    def post(self, request):
        print(request.data)
        algorithm = Algorithm.objects.get(name=request.data.get("algorithm"))
        try:
            camera = Camera.objects.get(id=request.data.get("camera"))
            start_tracking = request.data.get("start_tracking")
            stop_tracking = request.data.get("stop_tracking")
            photos = request.data.get("photos")
            violation_found = request.data.get("violation_found")

            if request.data.get("algorithm") == "min_max_control":
                extra = process_item_status(request.data.get("extra"))

            elif request.data.get("algorithm") == "operation_control":
                print(request.data.get("algorithm"))
                if not PRODUCTION:
                    print("start creating skany")
                    if 'extra' in request.data:
                        for data in request.data['extra']:
                            if 'place' in data:
                                requests.post(f"{SERVER_URL}:9876/skany/create/", json=request.data['extra'][0])
                                break
                        else:
                            requests.post(f"{SERVER_URL}:9876/operation-control/", json=request.data)
                extra = edit_extra(request.data.get("extra"), camera)
            else:
                extra = request.data.get("extra")

        except KeyError:
            return {"status": False, "message": "The model response is not complete"}
        else:
            action = Report.objects.create(
                camera=camera,
                extra=extra,
                algorithm=algorithm,
                violation_found=violation_found,
                start_tracking=start_tracking,
                stop_tracking=stop_tracking,
            )

            if photos:
                for photo in photos:
                    image = photo.get("image")
                    date = photo.get("date")
                    photo = Image.objects.create(
                        image=image, date=date, report_id=action
                    )
                if request.data.get("algorithm") == "operation_control":
                    create_skanyreport(action, extra, not violation_found)
            else:
                action.delete()
                return Response(
                    {
                        "status": False,
                        "message": "The report was not saved due to an omission in the response from the YOLO",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"status": True, "message": "Data created successfully"},
            status=status.HTTP_201_CREATED,
        )


class ReportListView(APIView):
    permission_classes = [IsAuthenticated]

    @validate_license
    def get(self, request, algorithm_name, camera_ip, date, start_time, end_time):
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_time_obj = datetime.strptime(start_time, "%H:%M:%S").time()
        end_time_obj = datetime.strptime(end_time, "%H:%M:%S").time()

        start_of_day = datetime.combine(date_obj, start_time_obj)
        end_of_day = datetime.combine(date_obj, end_time_obj)

        queryset = Report.objects.filter(
            Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
        ).order_by("-date_created", "-id")

        if camera_ip:
            queryset = queryset.filter(camera__id=camera_ip)
        if algorithm_name:
            queryset = queryset.exclude(algorithm__name='min_max_control').filter(algorithm__name=algorithm_name)

        queryset = queryset.order_by("algorithm__name", "camera__id", "id")

        serializer = ReportSerializers(queryset, many=True)
        return Response(serializer.data)


class SearchReportListView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializers

    @validate_license
    def get_queryset(self):
        date = self.request.query_params.get("date")
        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")
        camera_id = self.request.query_params.get("camera__id")
        algorithm_name = self.request.query_params.get("algorithm")

        queryset = Report.objects.all().order_by("-id")
        queryset = queryset.exclude(algorithm__name='min_max_control')

        if start_time:
            queryset = queryset.filter(date_created__gte=f"{date} {start_time}")
        if end_time:
            queryset = queryset.filter(date_created__lte=f"{date} {end_time}")
        if camera_id:
            queryset = queryset.filter(camera__id=camera_id)
        if algorithm_name:
            queryset = queryset.filter(algorithm__name=algorithm_name)

        queryset = queryset.order_by("-id")

        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)
