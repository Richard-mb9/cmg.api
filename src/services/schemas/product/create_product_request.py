from typing import TypedDict, List


class CreateProductRequest(TypedDict):
    store_id: int
    image_url: str
    name: str
    description: str
    available_store: bool
    available_delivery: bool
    price: float
    categories_ids: List[int]
