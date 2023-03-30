from rest_framework import views, viewsets, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import HistorySerializer
from .models import History


class HistoryViewSet(viewsets.ModelViewSet):
    """List of all history"""

    queryset = History.objects.all()

    serializer_class = HistorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "action",
        "location__name",
        "camera__id",
        "people__first_name",
        "people__last_name",
        "entry_date",
    ]

    def get_permissions(self):
        if self.request.method != "POST":
            return [IsAuthenticated()]
        return []


class FilteredHistoryModelViewSet(views.APIView):
    """Filtered History View"""

    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        # check required keys
        try:
            if request.data.get("type") is not None:
                type = request.data.get("type")
            else:
                raise AttributeError
            if request.data.get("from_date") is not None:
                from_date = request.data.get("from_date")
            else:
                raise AttributeError
            if request.data.get("to_date") is not None:
                to_date = request.data.get("to_date")
            else:
                raise AttributeError
        except AttributeError:
            return Response({"message": "The required keys do not exist"})
        else:
            if type == "between":
                serializer = HistorySerializer(
                    History.objects.filter(
                        entry_date__gte=from_date, entry_date__lte=to_date
                    ),
                    many=True,
                )
                return Response(serializer.data)
            elif type == "before":
                serializer = HistorySerializer(
                    History.objects.filter(entry_date__lte=from_date), many=True
                )
                return Response(serializer.data)
            elif type == "after":
                serializer = HistorySerializer(
                    History.objects.filter(entry_date__gte=from_date), many=True
                )
                return Response(serializer.data)
            else:
                return Response({"message": "Invalid type"})
