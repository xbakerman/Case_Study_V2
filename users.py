from serializable import Serializable
from database_inheritance import DatabaseConnector
from tinydb import Query

class User(Serializable):
    
    def __init__(self, name, email) -> None:
        super().__init__(email)
        self.name = name
        self.email = email

    @classmethod
    def get_db_connector(cls):
        return DatabaseConnector().get_users_table()

    def store(self):
        print("Storing user...")
        super().store()

    @classmethod
    def load_by_id(cls, id):
        print("Loading user...")
        data = super().load_by_id(id)
        if data:
            return cls(data['name'], data['email'])
        else:
            return None
        
    def delete(self):
        super().delete()
        print("User deleted.")

    def __str__(self):
        return F"User: {self.name} ({self.email})"

    def __repr__(self):
        return self.__str__()

if __name__ == "__main__":
    # Create a device
    user1 = User("User One", "one@mci.edu")
    user2 = User("User Two", "two@mci.edu") 
    user3 = User("User Three", "three@mci.edu") 
    user1.store()
    user2.store()
    user3.store()
    user4 = User("User Four", "four@mci.edu") 
    user4.store()

    loaded_user = User.load_by_id("four@mci.edu")
    if loaded_user:
        print(f"Loaded: {loaded_user}")
    else:
        print("User not found.")

    all_users = User.find_all()
    for user in all_users:
        print(user)