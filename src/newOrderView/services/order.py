from typing import List, Any, Tuple, Dict, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import logging

from src.newOrderView.repositories import OrderRepository
from src.newOrderView.utils import calculate_duration

logger = logging.getLogger(__name__)


class OrderServices:
    @staticmethod
    def get_order(
        from_date: str, to_date: str, operation_type_ids: List[int]
    ) -> List[Dict[str, Any]]:
        order_repo: OrderRepository = OrderRepository()

        from_date_dt: datetime = datetime.strptime(from_date, "%Y-%m-%d") + timedelta(microseconds=1)
        to_date_dt: datetime = datetime.strptime(to_date, "%Y-%m-%d") + timedelta(days=1) - timedelta(microseconds=1)


        order_data: List[Tuple[Any]] = order_repo.get_orders_by_operation(
            from_date=from_date_dt,
            to_date=to_date_dt,
            operation_type_ids=operation_type_ids,
        )

        result_dict: Dict[str, int] = defaultdict(int)

        for order_row in order_data:
            order_id: str = order_row[1].strip()
            startTime: datetime = order_row[2]
            endTime: Optional[datetime] = order_row[3]

            if endTime is not None:
                if endTime.date() > startTime.date():
                    endTime: datetime = startTime + timedelta(hours=1)
                else:
                    endTime: datetime = endTime or startTime + timedelta(hours=1)

            else:
                endTime: datetime = startTime + timedelta(hours=1)

            duration: int = calculate_duration(startTime, endTime)

            result_dict[order_id] += duration

        result_list: List[Dict[str, Any]] = [
            {"orId": order_id, "duration": duration}
            for order_id, duration in result_dict.items()
        ]

        return result_list
