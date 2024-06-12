import os
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Body
from app.schemas.AclDto import ACL
from app.services.consul_db_handler import ConsulDBHandler
from app.services.level_db_handler import LevelDBHandler

load_dotenv()
LEVELDB_PATH = os.getenv("ACL_LEVELDB_PATH")
CONSUL_DB_HOST = os.getenv("CONSUL_DB_HOST")
CONSUL_DB_PORT = os.getenv("CONSUL_DB_PORT")

app = FastAPI()
level_db_handler = LevelDBHandler(LEVELDB_PATH)
consul_db_handler = ConsulDBHandler(CONSUL_DB_HOST, CONSUL_DB_PORT)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/acl")
async def make_acl(acl_dto: ACL):
    object: str = acl_dto.object
    relation: str = acl_dto.relation
    user: str = acl_dto.user
    level_db_handler.put_acl(f"{object}#{relation}@{user}", f"{object}#{relation}@{user}")
    return {"object": object, "relation": relation, "user": user}


@app.get("/acl/check")
async def check_acl(object: str = Query(...), relation: str = Query(...), user: str = Query(...)):
    acl = level_db_handler.get_acl(f"{object}#{relation}@{user}")
    return {"authorized": acl is not None}


@app.post("/namespace")
async def create_namespace(namespace: str = Body(...)):
    consul_db_handler.store_config("namespace", namespace)
    return {"namespace": consul_db_handler.retrieve_config("namespace")}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)

