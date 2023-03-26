from typing import TypedDict, List


class UpdateProductRequest(TypedDict):
    image_url: str
    name: str
    price: float
    available_store: bool
    available_delivery: bool
    categories_ids: List[int]