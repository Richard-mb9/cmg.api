from src.infra.repositories.base_repository import BaseRepository
from src.domain.invoices_items import InvoicesItems


class InvoicesItemsRepository(BaseRepository):
    def __init__(self):
        super().__init__(InvoicesItems)
