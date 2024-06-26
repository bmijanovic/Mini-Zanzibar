from pydantic import BaseModel

class ACL(BaseModel):
    object: str
    relation: str
    user: str

    def to_key(self):
        return f"{self.object}#{self.relation}@{self.user}"