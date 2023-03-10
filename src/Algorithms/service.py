from rest_framework.exceptions import NotFound

from django.utils import timezone

from src.Algorithms.models import Algorithm, CameraAlgorithm, CameraAlgorithmLog
from src.Cameras.service import camera_service

from .utils import yolo_proccesing

from typing import Tuple, Union, List

from ..core.logger import logger
from src.StaffControl.Locations.models import Camera


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

    def update_status_of_algorithm_by_pid(self, pid: int):
        camera_algorithm = CameraAlgorithm.objects.filter(process_id=pid).first()
        if camera_algorithm:
            camera_algorithm_logs_service.delete_log(
                algorithm_name=camera_algorithm.algorithm.name,
                camera_ip=camera_algorithm.camera.id,
            )

            # camera_algorithm.is_active = False
            # camera_algorithm.save()
            camera_algorithm.delete()  # FIXME: Remove
        else:
            return {"status": False, "message": "Cannot find camera algorithm"}
        return {"status": True, "message": "Camera algorithm was stoped successfully"}

    def create_camera_algorithm(
        self, data: dict
    ) -> Tuple[List[CameraAlgorithm], List[str]]:
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
            if new_records:
                for camera in cameras:
                    camera_algorithm_logs_service.create_log(algorithm.name, camera.id)
                self.created_records.extend(new_records)
            else:
                for camera in cameras:
                    self.errors.append(
                        f"YOLO cant start process with next data: {algorithm}, {camera.id}, {server_url}"
                    )

        if self.errors:
            return {"message": self.errors}
        else:
            for record in self.created_records:
                logger.info(f"record -> {record} was created")
            return {"message": "Camera Algorithm records created successfully"}

    def get_algorithm_by_name(self, name: str):
        algorithm = Algorithm.objects.filter(name=name).first()
        if algorithm:
            return algorithm
        else:
            return False

    def create_new_records(
        self, algorithm: Algorithm, cameras: List[Camera], server_url: str
    ) -> Union[List[CameraAlgorithm], bool]:
        existing_records = self.get_existing_records(algorithm, cameras)
        new_records = []

        for camera in cameras:
            if existing_records.filter(camera=camera.id).exists():
                continue

            result = yolo_proccesing.start_yolo_processing(
                camera, algorithm, server_url
            )
            if not result["success"] or "pid" not in result:
                return False

            new_record = CameraAlgorithm(
                algorithm=algorithm,
                camera=camera,
                process_id=result["pid"],
                yolo_url=result["server_url"],
            )
            new_record.save()
            new_records.append(new_record)

        return new_records

    def get_existing_records(self, algorithm, cameras):
        return CameraAlgorithm.objects.filter(
            algorithm=algorithm, camera__in=cameras.values_list("id", flat=True)
        )


class CameraAlgorithmLogsService:
    def get_logs(self):
        return CameraAlgorithmLog.objects.all()

    def create_log(self, algorithm_name, camera_ip):
        CameraAlgorithmLog.objects.create(algorithm_name, camera_ip)

    def delete_log(self, algorithm_name, camera_ip):
        try:
            log = CameraAlgorithmLog.objects.get(
                algorithm_name=algorithm_name, camera_ip=camera_ip
            )
        except CameraAlgorithmLog.DoesNotExist:
            pass
        else:
            log.stoped_at = timezone.now()
            log.save()


camera_algorithm_logs_service = CameraAlgorithmLogsService()
algorithms_services = AlgorithmsService()
