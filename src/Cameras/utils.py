from src.Reports.models import Report
from src.ImageReport.models import Image
from src.Algorithms.service import algorithms_services

import zipfile
import os


class MakeZip:
    def __init__(self):
        self.image_report_path = []

    def get_image_path(self, algorithm: str):
        algorithm_obj = algorithms_services.get_algorithm_by_name(algorithm)

        if not algorithm_obj:
            return {
                "status": False,
                "message": f"Cannot find algorithm {algorithm}" 
            }
        
        reports = Report.objects.filter(algorithm=algorithm_obj)
        for report in reports:
            try:
                image_report_objs = Image.objects.filter(report_id=report)
            except Image.DoesNotExist:
                continue
            else:
                for image_report_obj in image_report_objs:
                    self.image_report_path.append(image_report_obj.image)

    def create_zip(self, algorithm: str):
        self.get_image_path(algorithm)
        zip_filename = f"{algorithm}_data.zip"

        with zipfile.ZipFile(zip_filename, "w") as zip_file:
            for path in self.image_report_path:
                zip_path = os.path.join(algorithm, path)
                zip_file.write(path, zip_path)
    
        return {
            "status": True,
            "message": f"Data from {algorithm} was successfully compressed to {zip_filename}"
        }


zip_maker = MakeZip()