from dataclasses import dataclass
from datetime import datetime


@dataclass
class Ordini:
    customer_id:int
    order_date: datetime
    order_id: int
    order_status:int
    required_date:datetime
    shipped_date:datetime
    staff_id:int
    store_id:int


    def __hash__(self):
        return hash(self.order_id)

    def __str__(self):
        return self.order_id
