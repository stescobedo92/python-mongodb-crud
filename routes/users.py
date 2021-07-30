from fastapi import APIRouter
from config.db import connection
from schemas.user import userEntity, usersEntity
from models.user import User

user = APIRouter()


@user.get('/users')
def find_all_users():
    return usersEntity(connection.local.user.find())


@user.post('/users')
def create_user(user: User):
    new_user = dict(user)
    del new_user["id"]
    id = connection.local.user.insert_one(new_user).inserted_id
    userResult = connection.local.user.find_one({"_id": id})

    return userEntity(userResult)


@user.get('/users/{id}')
def find_userBy_id():
    return "hello world"


@user.put('/users/{id}')
def update_user():
    return "hello world"

@user.delete('/users/{id}')
def find_all_users():
    return "hello world"