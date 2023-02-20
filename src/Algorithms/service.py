from rest_framework.exceptions import NotFound

from src.Algorithms.models import Algorithm, CameraAlgorithm
from src.StaffControl.Locations.service import camera_service

from .utils import yolo_proccesing

from ..core.logger import logger


class AlgorithmsService:
    def get_algorithms_status(self):
        algorithms = Algorithm.objects.all()
        algorithm_data = {
            algorithm.name: algorithm.is_available for algorithm in algorithms
        }
        return algorithm_data

    def get_camera_algorithms(self):
        process = CameraAlgorithm.objects.all()
        return process

    def update_status_of_algorithm(self, data):
        for algorithm_name, is_available in data.items():
            try:
                algorithm = Algorithm.objects.get(name=algorithm_name)
            except Algorithm.DoesNotExist:
                raise NotFound(
                    detail=f"Algorithm with name '{algorithm_name}' not found"
                )

            algorithm.is_available = is_available
            algorithm.save()

        return {"message": "Algorithm status updated"}

    def create_camera_algorithm(self, data):
        self.errors = []
        self.created_records = []
        server_url = data.pop("server_url")
        for algorithm_name, camera_ips in data.items():
            if algorithm_name == None:
                continue
            algorithm = self.get_algorithm_by_name(algorithm_name)
            if not algorithm:
                self.errors.append(
                    f"Algorithm with name {algorithm_name} does not exist"
                )
                continue

            if not algorithm.is_available:
                self.errors.append(
                    f"Algorithm with name {algorithm_name} is not available"
                )
                continue

            cameras = camera_service.get_cameras_by_ids(camera_ips)
            if not cameras:
                self.errors.append(
                    f"Cameras with ids {', '.join(camera_ips)} do not exist"
                )
                continue

            new_records = self.create_new_records(algorithm, cameras, server_url)
            self.created_records.extend(new_records)

        if self.errors:
            for error in self.errors:
                logger.critical(error)
            return {"message": self.errors}
        else:
            for record in self.created_records:
                logger.info(record)
            return {"message": "Camera Algorithm records created successfully"}

    def get_algorithm_by_name(self, name):
        return Algorithm.objects.filter(name=name).first()

    def create_new_records(self, algorithm, cameras, url):
        existing_records = self.get_existing_records(algorithm, cameras)
        new_records = []

        for camera in cameras:
            if existing_records.filter(camera_id=camera.id).exists():
                continue

            result = yolo_proccesing.start_yolo_processing(camera, algorithm, url)

            if "errors" not in result:
                new_record = CameraAlgorithm(
                    algorithm=algorithm, camera_id=camera, process_id=result["pid"]
                )
                new_record.save()
                new_records.append(new_record)

        return new_records

    def get_existing_records(self, algorithm, cameras):
        return CameraAlgorithm.objects.filter(
            algorithm=algorithm, camera_id__in=cameras.values_list("id", flat=True)
        )


algorithms_services = AlgorithmsService()
