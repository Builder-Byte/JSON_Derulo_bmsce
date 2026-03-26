class StateManager:

    def __init__(self):
        self.store = {}

    def get_history(self, user_id):
        return self.store.get(user_id, [])

    def update(self, user_id, data):
        if user_id not in self.store:
            self.store[user_id] = []

        self.store[user_id].append(data)

        return self.store[user_id]
    
    def get_userID(self, user_id):
        return self.store.get(user_id)