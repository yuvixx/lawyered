from dataclasses import dataclass
import json


@dataclass
class User:
    username: str
    email: str
    password: str

    def commit(self):
        users_db = json.load(open("./databases/users.json"))
        if self.username in users_db:
            return {"error": "username already exists"}, 400
        users_db[self.username] = self.__dict__
        dump_str = json.dumps(users_db, indent=4)
        with open("./databases/users.json", "w") as f:
            f.write(dump_str)
        return self.__dict__, 201
