import os
from pathlib import Path
from transit.reader import Reader
from transit.transit_types import Keyword

from model.logseq import Block, Datom, Node, NodeType

LogseqDB = dict[str, Node]

class LogseqDBAdapter:
    db: LogseqDB = {}
    node_db: dict[str, Node] = {}

    @staticmethod
    def from_journal_path(journal_path: str) -> 'LogseqDBAdapter':
        """
        Factory method to create a LogseqDBAdapter instance from a journal path.

        Args:
            journal_path (str): Path to the user's journal directory (e.g., '/Users/erica/notes')
        """
        db_file_path = LogseqDBAdapter.db_file_path_from_journal_path(journal_path)
        return LogseqDBAdapter(db_file_path)

    @staticmethod
    def db_file_path_from_journal_path(journal_path: str) -> str:
        """
        Convert a user's journal path to logseq transit file path
        Replaces path separators with '++' signs.

        Args:
            journal_path (str): Path to the user's journal directory (e.g., '/Users/erica/notes').

        Returns:
            str: Full path to logseq db (e.g., '/Users/erica/.logseq/graphs/logseq_local_++Users++erica++notes.transit').
        """
        # Expand user path
        expanded_path = os.path.expanduser(journal_path)
        
        # Normalize path separators to forward slashes
        normalized_path = expanded_path.replace(os.sep, '/')

        graphs_dir = os.path.expanduser("~/.logseq/graphs")
        
        # Replace forward slashes with '++' signs and prepend 'logseq_local_'
        formatted = normalized_path.replace('/', '++')
        return os.path.join(graphs_dir, f"logseq_local_{formatted}.transit")


    def __init__(self, db_path):
        self.db_path = Path(db_path)

    def read_all(self):
        """
        Read all logseq records into an in-memory database stored in the `db` attribute.

        Args:
            file_path (str): Path to the transit file. Can include ~ for home directory.
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"Transit file not found: {self.db_path}")
        
        if not self.db_path.is_file():
            raise ValueError(f"Path is not a file: {self.db_path}")
        
        with open(self.db_path, 'rb') as f:
            reader = Reader("json")
            transit_data = reader.read(f)
            datoms = transit_data.rep[self.kw("datoms")] 

            for item in datoms:
                rep = item.rep
                datom = Datom(rep[0], rep[1], rep[2], rep[3])
                self.read_datom(datom)
        
        for _, node in self.node_db.items():
            if len(str(node.uuid)) > 0:
                self.db[node.uuid] = node
    
    def read_node_type(self, keyword: Keyword) -> NodeType:
        kw_str = str(keyword)
        if kw_str.startswith("block/"):
            return NodeType.BLOCK
        elif kw_str.startswith("ast/"):
            return NodeType.AST
        elif kw_str.startswith("db/"):
            return NodeType.DB
        elif kw_str.startswith("page/"):
            return NodeType.PAGE
        elif kw_str.startswith("file/"):
            return NodeType.FILE
        elif kw_str.startswith("schema/"):
            return NodeType.SCHEMA
        else:
            raise ValueError(f"Unknown node type for keyword: {keyword}")
    
    def parse_node(self, datom: Datom) -> Node:
        node_type = self.read_node_type(datom.keyword)

        if node_type == NodeType.BLOCK:
            return Block(id=datom.id, num=datom.num)

        return Node(type=node_type, id=datom.id, num=datom.num)
                
    def read_datom(self, datom: Datom):
        # print(f"{datom.num} {datom.id} {datom.keyword} {datom.value}")

        if datom.num not in self.node_db:
            self.node_db[datom.num] = self.parse_node(datom)

        if self.node_db[datom.num].type != NodeType.BLOCK:
            return

        if datom.keyword == self.kw("block/uuid"):
            self.node_db[datom.num].uuid = str(datom.value)
        elif datom.keyword == self.kw("block/content"):
            self.node_db[datom.num].content = str(datom.value)

    def kw(self, key: str):
        return Keyword(key)
    
    def all_blocks(self) -> list[Block]:
        return [node for node in self.db.values() if node.type == NodeType.BLOCK]


# def has_method(o, name):
#     return callable(getattr(o, name, None))