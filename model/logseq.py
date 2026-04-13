class Datom:
    def __init__(self, num, keyword, value, id):
        self.num = num
        self.keyword = keyword
        self.value = value
        self.id = id

class Block:
    uuid: str = None
    last_modified_at: int = None
    name: str = None
    metadata: dict = {}
    content: str = None

    def __init__(self, id, num):
        self.id = id
        self.num = num
    
    def url(self):
        return f"logseq://graph/notes?block-id={self.uuid}"
