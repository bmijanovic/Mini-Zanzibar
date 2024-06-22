import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Body

from app.models import ACL
from app.consul_db_handler import ConsulDBHandler
from app.level_db_handler import LevelDBHandler

load_dotenv()
LEVELDB_PATH = os.getenv("ACL_LEVELDB_PATH")
CONSUL_DB_HOST = os.getenv("CONSUL_DB_HOST")
CONSUL_DB_PORT = os.getenv("CONSUL_DB_PORT")

app = FastAPI()
level_db_handler = LevelDBHandler(LEVELDB_PATH)
consul_db_handler = ConsulDBHandler(CONSUL_DB_HOST, CONSUL_DB_PORT)


@app.post("/acl")
async def create_acl(acl_dto: ACL):
    object: str = acl_dto.object
    relation: str = acl_dto.relation
    user: str = acl_dto.user
    level_db_handler.put(f"{object}@{user}", f"{relation}")
    return {"object": object, "relation": relation, "user": user}


@app.get("/acl/check")
async def check_acl(object: str = Query(...), relation: str = Query(...), user: str = Query(...)):
    acl = level_db_handler.get(f"{object}@{user}")
    return {"authorized": acl is not None}


@app.post("/namespace")
async def create_namespace(namespace=Body(...)):
    await consul_db_handler.create_new_config(namespace)
    return await consul_db_handler.get_config()
