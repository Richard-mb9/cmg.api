from typing import TypedDict


class BatchCreateTableRequest(TypedDict):
    store_id: int
    initial_range: int
    end_range: int
