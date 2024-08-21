from dataclasses import dataclass
import json
from typing import Optional


@dataclass
class User:
    username: Optional[str]
    email: str
    password: str

    def commit(self):
        users_db = json.load(open("./databases/users.json"))
        if self.email in users_db:
            return {"error": "email already exists"}, 409
        users_db[self.email] = self.__dict__
        dump_str = json.dumps(users_db, indent=4)
        with open("./databases/users.json", "w") as f:
            f.write(dump_str)
        return self.__dict__, 201

    def authenticate(self):
        users_db = json.load(open("./databases/users.json"))
        if self.email not in users_db:
            return {"error": "user does not exist"}, 404
        username = users_db[self.email]["username"]
        self.username = username
        if users_db[self.email]["password"] != self.password:
            return {"error": "password is incorrect"}, 401
        return self.__dict__, 200


@dataclass
class Chat:
    message: str
