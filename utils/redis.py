from .database import database

class Redis:
    def __init__(self) -> None:
        self.redis = dict()
    
    def record(self, special_id, userid, text) -> None:
        database.save_data(userid=userid, messageid=special_id, text=text)
        self.redis[userid] = {
            special_id: text
        }
    
    def get_special_id(self, userid):
        if userid in self.redis:
            return len(self.redis[userid]) + 1
        else:
            return 1
    
    async def get_cached(self, userid: int, special_id: int) -> str:
        if userid in self.redis:
            if special_id in self.redis[userid]:
                return await str(self.redis[userid][special_id]).replace('arroba', '@')

        else:
            data = database.get_data(userid=userid)
            if userid in data:
                return data
    

redis = Redis()