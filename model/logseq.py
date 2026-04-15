from dataclasses import dataclass, field
from enum import Enum

class Datom:
    def __init__(self, num, keyword, value, id):
        self.num = num
        self.keyword = keyword
        self.value = value
        self.id = id

class NodeType(Enum):
    AST = "ast"
    DB = "db"
    PAGE = "page"
    BLOCK = "block"
    FILE = "file"
    SCHEMA = "schema"

@dataclass
class Node:
    id: int = None
    type: NodeType = None
    num: int = None
    uuid: str = None
    last_modified_at: int = None
    name: str = None
    content: str = None
    match_value: float = None

    def __init__(self, type: NodeType, **kwargs):
        self.type = type
        for key, value in kwargs.items():
            setattr(self, key, value)

@dataclass
class Block(Node):
    def __init__(self, **kwargs):
        super().__init__(NodeType.BLOCK, **kwargs)

    def url(self):
        return f"logseq://graph/notes?block-id={self.uuid}"
