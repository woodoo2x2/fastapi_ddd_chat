from pydantic import BaseModel

from infrastructure.repositories.filters.base import GetMessagesInfraFilter


class GetMessagesFiltersSchema(BaseModel):
    limit: int = 10
    offset: int = 0

    def to_infra(self) -> GetMessagesInfraFilter:
        return GetMessagesInfraFilter(limit=self.limit, offset=self.offset)
