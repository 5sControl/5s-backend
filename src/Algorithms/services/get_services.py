from src.Algorithms.models import Algorithm, CameraAlgorithm


class GetAlgorithmsData:
    def get_algorithm_by_name(self, name: str):
        algorithm = Algorithm.objects.filter(name=name).first()
        if algorithm:
            return algorithm
        else:
            return False

    def get_existing_records(self, algorithm, cameras):
        return CameraAlgorithm.objects.filter(
            algorithm=algorithm, camera__in=cameras.values_list("id", flat=True)
        )

    def get_algorithms_status(self):
        algorithms = Algorithm.objects.all()
        algorithm_data = {
            algorithm.name: algorithm.is_available for algorithm in algorithms
        }
        return algorithm_data

    def get_camera_algorithms(self):
        process = CameraAlgorithm.objects.all()
        return process


algorithms_detail = GetAlgorithmsData()
