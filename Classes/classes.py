import tkintermapview


class BusStop:
    def __init__(self, id, name, coordinates):
        self.id = id
        self.name = name
        self.coordinates = coordinates


class BusRoute:
    def __init__(self, id, name, number, schedule, path, active, direction):
        self.id = id
        self.number = number
        self.direction = direction
        self.active = active
        self.name = name
        self.schedule = schedule
        self.path = path

    def get_schedule(self):
        return f"Каждые {self.schedule.time} минут"

    @staticmethod
    def get_info(self):
        pass


class Schedule:
    def __init__(self, id, path_id, time):
        self.id = id
        self.path_id = path_id
        self.time = time

class User:
    def __init__(self, login, password, is_admin, is_driver):
        self.login = login
        self.password = password
        self.is_admin = is_admin
        self.is_driver = is_driver
