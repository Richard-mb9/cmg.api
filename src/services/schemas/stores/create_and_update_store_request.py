from typing import TypedDict


class CreateAndUpdateStoreRequest(TypedDict):
    name: str
    cnpj: str
    corporate_name: str