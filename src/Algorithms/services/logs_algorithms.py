from datetime import timezone

from src.Algorithms.models import CameraAlgorithmLog


class CameraAlgorithmLogsService:
    def get_logs(self):
        return CameraAlgorithmLog.objects.all()

    def create_log(self, algorithm_name, camera_ip):
        CameraAlgorithmLog.objects.create(
            algorithm_name=algorithm_name, camera_ip=camera_ip
        )

    def delete_log(self, algorithm_name, camera_ip):
        try:
            logs = CameraAlgorithmLog.objects.filter(
                algorithm_name=algorithm_name, camera_ip=camera_ip
            )
        except CameraAlgorithmLog.DoesNotExist:
            pass
        else:
            for log in logs:
                log.stoped_at = timezone.now()
                log.save()


logs_service = CameraAlgorithmLogsService()
