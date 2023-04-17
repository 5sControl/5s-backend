import math
from typing import Any, Dict

import requests

from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from src.Algorithms.utils import yolo_proccesing


class OrderViewPaginnator(PageNumberPagination):
    page_size = 50
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        count = self.page.paginator.count
        page_size = self.get_page_size(self.request)
        all_page_count = math.ceil(count / page_size)

        return Response(
            OrderedDict(
                [
                    ("count", count),
                    ("current_page", self.page.number),
                    ("records_on_page", page_size),
                    ("all_page_count", all_page_count),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )


# FIXME: camera ip should be dynamic
def get_skany_video_info(time, camera_ip="192.168.1.110") -> Dict[str, Any]:
    server_host = yolo_proccesing.get_algorithm_url()
    video_chacker_host = f"{server_host}:3456/is_video_available/"

    response = {
        "camera_ip": str(server_host)[7:],
        "time": time,
    }

    print(video_chacker_host)
    print(response)

    request = requests.post(
        url=f"{video_chacker_host}:3456/is_video_available/",
        json=response,
    )

    return request.json()
