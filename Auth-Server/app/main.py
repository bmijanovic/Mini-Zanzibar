from fastapi import FastAPI, Query
from app.schemas.AclDto import ACLRequest
import uvicorn

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



@app.post("/acl")
async def make_acl(acl_dto: ACLRequest):
    object: str = acl_dto.object
    relation: str = acl_dto.relation
    user: str = acl_dto.user
    return {"object": object, "relation": relation, "user": user}

@app.get("/acl/check")
async def check_acl(object: str = Query(...), relation: str = Query(...), user: str = Query(...)):
    return {"authorized": True}

@app.post("/namespace")
async def create_namespace(namespace: str):
    return {"namespace": namespace}

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

