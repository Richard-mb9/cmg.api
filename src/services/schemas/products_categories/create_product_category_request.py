from typing import TypedDict


class CreateProductCategoryRequest(TypedDict):
    name: str
    store_id: int