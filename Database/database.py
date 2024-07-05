from pymongo import MongoClient
from config import DB_URI, OWNER_ID

client = MongoClient(DB_URI)
db = client['farm_game']

class Database:
    def __init__(self):
        self.users = db['users']

    async def add_nyx_coin(self, user_id: int, amount: int):
        user = mycol.find_one({'_id': user_id})
        if user:
            current_nyx_coin = int(user.get('nyx_coin', 0))
            new_nyx_coin = current_nyx_coin + amount
            mycol.update_one({'_id': user_id}, {'$set': {'nyx_coin': new_nyx_coin}})
            

    def initialize_user(self, user_id, username):
        if not self.users.find_one({"_id": user_id}):
            user_data = {
                "_id": user_id,
                "username": username,
                "money": 9999999999999 if user_id == OWNER_ID else 50000,
                "animals": {},
                "products": {},
                "is_banned": False
            }
            self.users.insert_one(user_data)

    def get_user(self, user_id):
        return self.users.find_one({"_id": user_id})

    def update_user(self, user_id, update_data):
        self.users.update_one({"_id": user_id}, {"$set": update_data})

    def get_all_users(self):
        return list(self.users.find())

    def ban_user(self, user_id):
        self.update_user(user_id, {"is_banned": True})

    def unban_user(self, user_id):
        self.update_user(user_id, {"is_banned": False})
