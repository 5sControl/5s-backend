import logging

import requests
from datetime import datetime

from django.db.models import Q

from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from src.CompanyLicense.decorators import validate_license
from src.Core.const import PRODUCTION, SERVER_URL
from src.Core.paginators import NoPagination
from src.ImageReport.models import Image
from src.CameraAlgorithms.models import Camera
from src.CameraAlgorithms.models import Algorithm
from src.Reports.models import Report, SkanyReport
from src.Reports.serializers import (
    ReportSerializers,
    OperationReportSerializer,
    ReportByIDSerializer,
)
from src.Inventory.service import process_item_status
from src.Reports.service import edit_extra, create_skanyreport

logger = logging.getLogger(__name__)


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
        data = request.data
        try:
            algorithm_name = data.get("algorithm")
            camera_ip = data.get("camera")

            algorithm = Algorithm.objects.get(name=algorithm_name)
            camera = Camera.objects.get(id=camera_ip)

            start_tracking = data.get("start_tracking")
            stop_tracking = data.get("stop_tracking")

            photos = data.get("photos")
            violation_found = data.get("violation_found")

            # FIXME: make easy this shit
            if algorithm_name == "min_max_control":
                extra = process_item_status(data.get("extra"))

            elif algorithm_name == "operation_control":
                if not PRODUCTION:
                    if "extra" in data:
                        for data in data["extra"]:
                            if "place" in data:
                                logger.warning(
                                    f"Operation control extra data is {data}"
                                )
                                requests.post(
                                    f"{SERVER_URL}:9876/skany/create/",
                                    json=data["extra"][0],
                                )
                                break
                        else:
                            logger.warning(f"Operation control extra data is {data}")
                            requests.post(
                                f"{SERVER_URL}:9876/operation-control/", json=data
                            )
                extra = edit_extra(data.get("extra"), camera)
            else:
                extra = data.get("extra")

        except KeyError as e:
            logger.critical(f"Error while parsing report: {e}")
            return {"status": False, "message": "The model response is not complete"}

        action = Report.objects.create(
            camera=camera,
            extra=extra,
            algorithm=algorithm,
            violation_found=violation_found,
            start_tracking=start_tracking,
            stop_tracking=stop_tracking,
        )

        if algorithm_name == "operation_control":
            create_skanyreport(
                action, extra, not violation_found, start_tracking, stop_tracking
            )

        if photos:
            for photo in photos:
                if photo.get("image"):
                    image = photo.get("image")
                    date = photo.get("date")
                    photo = Image.objects.create(
                        image=image, date=date, report_id=action
                    )
        else:
            logger.critical(f"Image in report {action} wasn't found")
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
            queryset = queryset.exclude(algorithm__name="min_max_control").filter(
                algorithm__name=algorithm_name
            )

        queryset = queryset.order_by("algorithm__name", "camera__id", "id")

        serializer = ReportSerializers(queryset, many=True)
        return Response(serializer.data)


class SearchReportListView(GenericAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = ReportSerializers

    @validate_license
    def get_queryset(self):
        date = self.request.query_params.get("date")
        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")
        camera_ids = self.request.query_params.getlist("camera__id")
        algorithm_names = self.request.query_params.getlist("algorithm")

        queryset = Report.objects.all().order_by("-id")

        if start_time:
            queryset = queryset.filter(date_created__gte=f"{date} {start_time}")
        if end_time:
            queryset = queryset.filter(date_created__lte=f"{date} {end_time}")
        if camera_ids:
            camera_filters = Q()
            for camera_id in camera_ids[0].split(","):
                camera_filters |= Q(camera__id=camera_id)
            queryset = queryset.filter(camera_filters)
        if algorithm_names:
            algorithm_filters = Q()
            for algorithm_name in algorithm_names[0].split(","):
                algorithm_filters |= Q(algorithm__name=algorithm_name)
            queryset = queryset.filter(algorithm_filters)

        queryset = queryset.exclude(algorithm__name="min_max_control")

        queryset = queryset.order_by("-id")

        return queryset

    def get(self, request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class GetOperationVideoInfo(ListAPIView):
    queryset = SkanyReport.objects.all()
    serializer_class = OperationReportSerializer
    pagination_class = NoPagination

    def get_queryset(self):
        return SkanyReport.objects.exclude(start_time__isnull=True)


class GetReportByID(RetrieveAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportByIDSerializer
