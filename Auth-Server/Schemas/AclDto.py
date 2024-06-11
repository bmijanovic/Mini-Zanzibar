from pydantic import BaseModel


class ACLRequest(BaseModel):
    object: str
    relation: str
    user: str

