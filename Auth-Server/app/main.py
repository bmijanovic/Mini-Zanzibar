import base64
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Query, Body
from starlette.middleware.cors import CORSMiddleware

from app.models import ACL
from app.consul_db_handler import ConsulDBHandler
from app.level_db_handler import LevelDBHandler
from app.role_parser import *

load_dotenv()
LEVELDB_PATH = os.getenv("ACL_LEVELDB_PATH")
CONSUL_DB_HOST = os.getenv("CONSUL_DB_HOST")
CONSUL_DB_PORT = os.getenv("CONSUL_DB_PORT")

app = FastAPI()
level_db_handler = LevelDBHandler(LEVELDB_PATH)
consul_db_handler = ConsulDBHandler(CONSUL_DB_HOST, CONSUL_DB_PORT)

origins = [
    "http://consul:8500/",
    "http://client_back:8001/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=[""],
    allow_headers=[""],
)


@app.post("/acl")
async def create_acl(acl_dto: ACL):
    object: str = acl_dto.object
    relation: str = acl_dto.relation
    user: str = acl_dto.user
    level_db_handler.put(f"{object}@{user}", f"{relation}")
    return {"object": object, "relation": relation, "user": user}


@app.delete("/acl")
async def delete_acl(object: str = Query(...), user: str = Query(...)):
    level_db_handler.delete(f"{object}@{user}")
    return {"object": object, "user": user}


@app.get("/acl/check")
async def check_acl(object: str = Query(...), relation: str = Query(...), user: str = Query(...)):
    role = level_db_handler.get(f"{object}@{user}")
    if role is None:
        return {"authorized": False}
    namespace = await consul_db_handler.get_config()
    privileges = get_privileges(relation, namespace['relations'])
    return {"authorized": role in privileges}


@app.post("/namespace")
async def create_namespace(namespace=Body(...)):
    await consul_db_handler.create_new_config(namespace)
    return "Success"


@app.post("/consul_watch_handler")
async def consul_watch_handler(body=Body(...)):
    decoded_version = base64.b64decode(body['Value']).decode('utf-8')
    await consul_db_handler.change_config_to_version(decoded_version.replace('"', ""))
    return "Success"


# testing
@app.get("/namespace")
async def get_namespace():
    return await consul_db_handler.get_config()
