import tkintermapview


class BusSystem:
    def __init__(self):
        self.routes = []
        self.users = []

    def add_route(self, route):
        self.routes.append(route)

    def remove_route(self, route_id):
        for route in self.routes:
            if route.id == route_id:
                self.routes.remove(route)
                return

    def add_user(self, user):
        self.users.append(user)

    def remove_user(self, user_id):
        for user in self.users:
            if user.id == user_id:
                self.users.remove(user)
                return


class BusStop:
    def __init__(self, id, name, coordinates):
        self.__id = id
        self.__name = name
        self.__coordinates = coordinates

    @staticmethod
    def get_info(self):
        pass

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @property
    def coordinates(self):
        return self.__coordinates

    @coordinates.setter
    def coordinates(self, coordinates):
        self.__coordinates = coordinates


class BusRoute:
    def __init__(self, id, name, schedule, path):
        self.__id = id
        self.__name = name
        self.schedule = schedule
        self.path = path

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, name):
        self.__name = name

    @staticmethod
    def get_schedule(self):
        pass

    @staticmethod
    def get_info(self):
        pass


class Schedule:
    def __init__(self, id, time, bus_stops):
        self.__id = id
        self.__time = time
        self.bus_stops = bus_stops

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, id):
        self.__id = id

    @property
    def time(self):
        return self.__time

    @time.setter
    def time(self, time):
        self.__time = time

    def get_times(self):
        return self.__time


class User:
    pass

