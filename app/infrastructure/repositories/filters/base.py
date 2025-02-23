from dataclasses import dataclass


@dataclass
class GetMessagesInfraFilter:
    limit: int = 10
    offset: int = 0
