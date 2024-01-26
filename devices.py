import os
from datetime import datetime

from users import User
from serializable import Serializable
from database_inheritance import DatabaseConnector
from tinydb import Query

class Device(Serializable):

    def __init__(self, device_name: str, managed_by_user_id: str, maintenance_date: datetime = None, reservierung_start = None, reservierung_end = None, end_of_life: datetime = None, creation_date: datetime = None, last_update: datetime = None):
        super().__init__(device_name)
        self.device_name = device_name
        # The user id of the user that manages the device
        # We don't store the user object itself, but only the id (as a key)
        self.managed_by_user_id = managed_by_user_id

        self.is_active = True
        self.end_of_life = end_of_life if end_of_life else datetime.today().date()
        self.__creation_date = creation_date if creation_date else datetime.today().date()
        self.__last_update = last_update if last_update else datetime.today().date()
        self.maintenance_date = maintenance_date if maintenance_date else datetime.today().date()
        self.reservierung_start = reservierung_start if reservierung_start else datetime.today().date()
        self.reservierung_end = reservierung_end if reservierung_end else datetime.today().date()
    
    @classmethod
    def get_db_connector(cls):
        return DatabaseConnector().get_devices_table()

    def store(self):
        print("Storing device...")
        self.__last_update = datetime.today().date() # we need to update the last update date before storing the object
        super().store()
    
    @classmethod
    def load_by_id(cls, id):
        print("Loading device...")
        data = super().load_by_id(id)
        if data:
            return cls(data['device_name'], data['managed_by_user_id'], data['end_of_life'], data['_Device__creation_date'], data['_Device__last_update'])
        else:
            return None
    
    def delete(self):
        super().delete()
        print("Device deleted.")

    def __str__(self) -> str:
        return F"Device: {self.device_name} ({self.managed_by_user_id}) - Active: {self.is_active} - Created: {self.__creation_date} - Last Update: {self.__last_update}"

    def __repr__(self) -> str:
        return self.__str__()
    
    def wartungsdatum_aendern(self, wartungsdatum: datetime):
        self.maintenance_date = wartungsdatum
        self.store()

    def Reservierungszeitraum(self, start: datetime, end: datetime):
        self.is_active = False
        self.resrvierung_start = start
        self.reservierung_end = end
        self.store() 

    def Wartung_löschen(self, wartungsdatum: datetime):
        self.maintenance_date = wartungsdatum
        self.delete()

if __name__ == "__main__":
    # Create a device
    device1 = Device("Device1", "one@mci.edu")
    device2 = Device("Device2", "two@mci.edu") 
    device3 = Device("Device3", "two@mci.edu") 
    device1.store()
    device2.store()
    device3.store()
    device4 = Device("Device3", "four@mci.edu") 
    device4.store()

    loaded_device = Device.load_by_id("Device2")
    if loaded_device:
        print(f"Loaded: {loaded_device}")
    else:
        print("Device not found.")

    all_devices = Device.find_all()
    for device in all_devices:
        print(device)