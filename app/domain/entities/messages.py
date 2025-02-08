from dataclasses import dataclass
from domain.values.message import Text

@dataclass
class Message:
    oid: str
    text: Text
