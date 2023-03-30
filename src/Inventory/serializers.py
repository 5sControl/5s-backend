from rest_framework import serializers

from src.Algorithms.service import algorithms_services

from src.Inventory.models import Items
from src.Algorithms.models import CameraAlgorithm
from src.Cameras.models import Camera
from src.Algorithms.models import Algorithm

from django.db.models import Q

from src.Algorithms.utils import yolo_proccesing


class ItemsSerializer(serializers.ModelSerializer):
    """
    Items Serializer
    """

    class Meta:
        model = Items
        fields = ["id",
                  "name",
                  "status",
                  "current_stock_level",
                  "low_stock_level",
                  "email",
                  "camera",
                  "date_created",
                  "date_updated",
                  "coords"
                  ]

    def update(self, instance, validated_data):
        # update item
        instance = super().update(instance, validated_data)
        print(f"Updated item {instance}")

        # stopped process
        process_id = CameraAlgorithm.objects.filter(
            Q(camera_id=instance.camera) & Q(algorithm__name='min_max_control')
        ).values_list('process_id', flat=True).first()
        if process_id == None:
            return instance
        yolo_proccesing.stop_process(pid=process_id)

        # updated status process
        algorithms_services.update_status_of_algorithm_by_pid(pid=process_id)

        # started process
        camera = Camera.objects.filter(id=instance.camera)
        algorithm = Algorithm.objects.filter(name='min_max_control')
        algorithms_services.create_new_records(cameras=[camera], algorithm=algorithm)

        return instance
