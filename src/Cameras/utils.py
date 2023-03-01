from src.Reports.models import Report
from src.ImageReport.models import Image
from src.Algorithms.service import algorithms_services

from datetime import datetime
import zipfile
import os


class MakeZip:
    def __init__(self):
        self.image_report_path = []
        self.images_folder = "images/"
        
    def get_image_path(self, algorithm: str):
        algorithm_obj = algorithms_services.get_algorithm_by_name(algorithm)

        if not algorithm_obj:
            return {
                "status": False,
                "message": f"Cannot find algorithm {algorithm}" 
            }
        
        reports = Report.objects.filter(algorithm=algorithm_obj)
        for report in reports:
            image_report_objs = Image.objects.filter(report_id=report)
            for image_report_obj in image_report_objs:
                self.image_report_path.append(image_report_obj.image)

    def create_zip(self, algorithm: str):
        self.get_image_path(algorithm)
        zip_filename = f"{algorithm}_data_{datetime.now().date()}.zip"
        zip_path = os.path.join(self.images_folder, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zip_file:
            for image_path in self.image_report_path:
                zip_path = os.path.join("images", image_path)
                zip_file.write(image_path, zip_path)
        
        return {
            "status": True,
            "message": f"Zip file created at {zip_path}"
        }


zip_maker = MakeZip()