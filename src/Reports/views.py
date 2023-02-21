from rest_framework import viewsets
from datetime import datetime, time
from django.db.models import Q
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
        algorithm = Algorithm.objects.get(name=request.data.get("algorithm"))
        try:
            camera = Camera.objects.get(id=request.data.get("camera"))
            start_tracking = request.data.get("start_tracking")
            stop_tracking = request.data.get("stop_tracking")
            photos = request.data.get("photos")
            violation_found = request.data.get("violation_found")
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

    def get(self, request, date):
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        start_of_day = datetime.combine(date_obj, time.min)
        end_of_day = datetime.combine(date_obj, time.max)

        queryset = (
            Report.objects.filter(
                Q(date_created__gte=start_of_day) & Q(date_created__lte=end_of_day)
            )
            .order_by("date_created")
            .order_by("-id")
        )

        serializer = ReportSerializers(queryset, many=True)
        return Response(serializer.data)


class ReportListAPIView(APIView):
    """Sort from start of date to end of date"""

    permission_classes = [IsAuthenticated]

    def get(self, request, start_date, end_date):
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        queryset = Report.objects.filter(
            date_created__gte=start_date, date_created__lte=end_date
        ).order_by("date_created")
        serializer = ReportSerializers(queryset, many=True)
        return Response(serializer.data)
