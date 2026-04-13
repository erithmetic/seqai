import os
from pathlib import Path
from transit.reader import Reader
from transit.transit_types import Keyword

from model.logseq import Block, Datom

LogseqDB = dict[str, Block]

class LogseqDBAdapter:
    db: LogseqDB = {}
    node_db: dict[str, Block] = {}

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

    def read_all(self) -> dict:
        """
        Read all logseq records

        Args:
            file_path (str): Path to the transit file. Can include ~ for home directory.

        Returns:
            Dict: a dictionary representation of the logseq graph

        Raises:
            FileNotFoundError: If the file does not exist.
            IOError: If there's an error reading the file.
            ValueError: If there's an error parsing the transit data.
        """
        if not self.db_path.exists():
            raise FileNotFoundError(f"Transit file not found: {self.db_path}")
        
        if not self.db_path.is_file():
            raise ValueError(f"Path is not a file: {self.db_path}")
        
        with open(self.db_path, 'rb') as f:
            reader = Reader("json")
            db = reader.read(f)
            datoms = db.rep[self.kw("datoms")] 

            for item in datoms:
                rep = item.rep
                datom = Datom(rep[0], rep[1], rep[2], rep[3])
                self.read_datom(datom)
        
        for _, block in self.node_db.items():
            self.db[block.uuid] = block
                
    def read_datom(self, datom: Datom):
        print(f"{datom.num} {datom.id} {datom.keyword} {datom.value}")

        if datom.num not in self.node_db:
            self.node_db[datom.num] = Block(datom.id, datom.num)

        if datom.keyword == self.kw("block/uuid"):
            self.node_db[datom.num].uuid = str(datom.value)
        elif datom.keyword == self.kw("block/content"):
            self.node_db[datom.num].content = str(datom.value)

    def kw(self, key: str):
        return Keyword(key)


# def has_method(o, name):
#     return callable(getattr(o, name, None))