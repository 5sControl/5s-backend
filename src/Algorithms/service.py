import requests

from rest_framework.exceptions import NotFound

from src.Algorithms.models import Algorithm, CameraAlgorithm
from src.StaffControl.Locations.models import Camera
from src.StaffControl.Locations.service import link_generator


class AlgorithmsService:
    def get_algorithms_status(self):
        algorithms = Algorithm.objects.all()
        algorithm_data = {
            algorithm.name: algorithm.is_available for algorithm in algorithms
        }
        return algorithm_data

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

            cameras = self.get_cameras_by_ids(camera_ips)
            if not cameras:
                self.errors.append(
                    f"Cameras with ids {', '.join(camera_ips)} do not exist"
                )
                continue

            new_records = self.create_new_records(algorithm, cameras)
            self.created_records.extend(new_records)

        self.log_created_records()

        if self.errors:
            return {"errors": self.errors}
        else:
            return {"message": "Camera Algorithm records created successfully"}

    def get_algorithm_by_name(self, name):
        return Algorithm.objects.filter(name=name).first()

    def get_cameras_by_ids(self, ids):
        return Camera.objects.filter(id__in=ids)

    def create_new_records(self, algorithm, cameras):
        existing_records = self.get_existing_records(algorithm, cameras)
        new_records = []

        for camera in cameras:
            if existing_records.filter(camera_id=camera.id).exists():
                continue

            result = self.start_yolo_processing(camera, algorithm)

            if "errors" not in result:
                print(result)
                new_record = CameraAlgorithm(
                    algorithm=algorithm, camera_id=camera, process_id=result["pid"]
                )
                new_record.save()
                new_records.append(new_record)

        return new_records

    def start_yolo_processing(self, camera, algorithm):
        rtsp_camera_url = link_generator.get_camera_rtsp_link_by_camera(camera)
        response = {"camera_url": rtsp_camera_url, "algorithm": algorithm.name}
        try:
            response = requests.post(
                url="http://detection_runner:3020/run",  # Send process data to YOLOv7 server
                json=response,
            )
            response_json = response.json()
        except requests.exceptions.RequestException as e:
            self.errors.append(f"Error sending request: {e}")
            return {"errors": [f"Error sending request: {e}"]}
        except ValueError as e:
            self.errors.append(f"Error decoding response: {e}")
            return {"errors": [f"Error decoding response: {e}"]}

        if response_json.get("status").lower() != "success":
            self.errors.append(f"Received non-success response: {response_json}")
            return {"errors": [f"Received non-success response: {response_json}"]}
        elif "pid" not in response_json:
            self.errors.append(f"Missing PID in response: {response_json}")
            return {"errors": [f"Missing PID in response: {response_json}"]}
        else:
            return response_json

    def get_existing_records(self, algorithm, cameras):
        return CameraAlgorithm.objects.filter(
            algorithm=algorithm, camera_id__in=cameras.values_list("id", flat=True)
        )

    def log_created_records(self):
        for record in self.created_records:
            print(
                f"Created record for algorithm '{record.algorithm.name}' and camera '{record.camera_id}'"
            )


algorithms_services = AlgorithmsService()
