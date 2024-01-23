import os
from tinydb import TinyDB, Query 
from serializer import serializer


class User:
    
    db_connector = TinyDB(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.json'), storage=serializer).table('users')

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.db = TinyDB('database.json')
        

    def __str__(self):
        return f"{self.name} ({self.id})"
    
    def to_dict(self):
        return {"id": self.id, "name": self.name}
    
    def store_data(self):
        print("Storing user data...")
        # Check if the user already exists in the database
        UserQuery = Query()
        result = self.db_connector.search(UserQuery.id == self.id)
        if result:
            # Update the existing record with the current instance's data
            result = self.db_connector.update(self.to_dict(), doc_ids=[result[0].doc_id])
            print("User data updated.")
        else:
            # If the user doesn't exist, insert a new record
            self.db_connector.insert(self.to_dict())
            print("User data inserted.")
            
    @classmethod
    def load_data_by_id(cls, user_id):
        # Lade Daten aus der Datenbank und erstelle eine Instanz der User-Klasse
        UserQuery = Query()
        result = cls.db_connector.get(UserQuery.id == user_id)

        if result:
            data = result
            return cls(data['id'], data['name'])
        else:
            return None
        
    @classmethod
    def load_data_by_name(cls, user_name):
        # Lade Daten aus der Datenbank und erstelle eine Instanz der User-Klasse
        UserQuery = Query()
        result = cls.db_connector.get(UserQuery.name == user_name)

        if result:
            data = result
            return cls(data['id'], data['name'])
        else:
            return None
        
    @classmethod
    def load_all_data(cls):
        # Lade alle Benutzer aus der Datenbank und erstelle eine Liste von User-Objekten
        all_data = cls.db_connector.all()
        return [cls(data['id'], data['name']) for data in all_data]
     
    def delete_data(self):
        UserQuery = Query()
        result = self.db_connector.remove(UserQuery.id == self.id)
        return result