from rest_framework.exceptions import NotFound
from src.Cameras.models import Camera

from src.CompanyLicense.decorators import check_active_algorithms
from src.Algorithms.models import Algorithm, CameraAlgorithm
from src.Inventory.models import Items
from src.Core.logger import logger

from src.Algorithms.utils import yolo_proccesing
from src.Algorithms.services.logs_algorithms import logs_service
from src.Core.const import SERVER_URL


class AlgorithmsService:
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
            logs_service.delete_log(
                algorithm_name=camera_algorithm.algorithm.name,
                camera_ip=camera_algorithm.camera.id,
            )
            camera_algorithm.delete()
        else:
            return {"status": False, "message": "Cannot find camera algorithm"}
        return {"status": True, "message": "Camera algorithm was stoped successfully"}

    @check_active_algorithms
    def create_camera_algorithm(self, data):
        self.errors = []
        self.created_records = []
        server_url = data.pop("server_url")

        for algorithm_name, camera_ips in data.items():
            if not algorithm_name:
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

            cameras = Camera.objects.filter(id__in=camera_ips)
            if not cameras:
                self.errors.append(
                    f"Cameras with ids {', '.join(camera_ips)} do not exist"
                )
                continue

            new_records = self.create_new_records(algorithm, cameras, server_url)
            if new_records:
                for camera in cameras:
                    logs_service.create_log(algorithm.name, camera.id)
                self.created_records.extend(new_records)
            else:
                for camera in cameras:
                    self.errors.append(
                        f"YOLO cant start process with next data: {algorithm}, {camera.id}, {server_url}"
                    )

        if self.errors:
            return {"status": False, "message": self.errors}
        else:
            for record in self.created_records:
                logger.info(f"record -> {record} was created")
            return {
                "status": True,
                "message": "Camera Algorithm records created successfully",
            }

    def create_new_records(self, algorithm, cameras):
        existing_records = self.get_existing_records(algorithm, cameras)
        new_records = []

        for camera in cameras:
            if existing_records.filter(camera=camera.id).exists():
                continue

            if CameraAlgorithm.objects.filter(
                algorithm=algorithm, camera=camera, is_active=True
            ).exists():
                self.errors.append(
                    f"Record with algorithm {algorithm.name}, camera {camera.id}, and server url {SERVER_URL} already exists"
                )
                continue
            if algorithm.name == "min_max_control":
                data = []
                algorithm_items = Items.objects.filter(camera=camera.id)
                print("algo items", algorithm_items.values())
                for item in algorithm_items:
                    data.append({"itemId": item.id, "coords": item.coords, "itemName": item.name})
                    print(f"coords: {item.coords}\nid {item.id}")
                print(f"camera id: {camera.id}")
            else:
                data = None
            result = yolo_proccesing.start_yolo_processing(
                camera=camera, algorithm=algorithm, data=data
            )
            if not result["success"] or "pid" not in result:
                return False

            new_record = CameraAlgorithm(
                algorithm=algorithm,
                camera=camera,
                process_id=result["pid"],
            )
            new_record.save()
            new_records.append(new_record)

        return new_records


edit_algorithms = AlgorithmsService()
