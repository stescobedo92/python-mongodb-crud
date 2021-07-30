from fastapi import APIRouter, Response
from config.db import connection
from schemas.user import userEntity, usersEntity
from models.user import User
from passlib.hash import sha256_crypt
from bson import ObjectId
from starlette.status import HTTP_204_NO_CONTENT

user = APIRouter()


@user.get('/users')
def find_all_users():
    return usersEntity(connection.local.user.find())


@user.post('/users')
def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]
    id = connection.local.user.insert_one(new_user).inserted_id
    userResult = connection.local.user.find_one({"_id": id})

    return userEntity(userResult)


@user.get('/users/{id}')
def find_userBy_id(id: str):
    return userEntity(connection.local.user.find_one({"_id": ObjectId(id)}))


@user.put('/users/{id}')
def update_user(id: str, user: User):
    connection.local.user.find_one_and_update({"_id": ObjectId(id)}, {"$set": dict(user)})
    return userEntity(connection.local.user.find_one({"_id": ObjectId(id)}))


@user.delete('/users/{id}')
def find_all_users(id: str):
    userEntity(connection.local.user.find_one_and_delete({"_id": ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)