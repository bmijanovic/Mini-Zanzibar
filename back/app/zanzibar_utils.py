import os
import requests
from dotenv import load_dotenv

load_dotenv()
MINI_ZANZIBAR_URL = os.getenv("MINI_ZANZIBAR_URL")


def check_acl(object, relation, user):
    return requests.get(MINI_ZANZIBAR_URL + "/acl/check", params={
        "object": object,
        "relation": relation,
        "user": user
    })


def create_acl(object, relation, user):
    return requests.post(MINI_ZANZIBAR_URL + "/acl", json={
        "object": object,
        "relation": relation,
        "user": user
    })


def delete_acl(object, user):
    return requests.delete(MINI_ZANZIBAR_URL + "/acl", params={
        "object": object,
        "user": user
    })
