import tkintermapview


# class BusSystem:
#     def __init__(self):
#         self.routes = []
#
#     def add_route(self, route):
#         self.routes.append(route)
#
#     def remove_route(self, route_id):
#         for route in self.routes:
#             if route.id == route_id:
#                 self.routes.remove(route)
#                 return


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

    @staticmethod
    def get_schedule(self):
        return f"Каждые {self.time} минут"

    @staticmethod
    def get_info(self):
        pass


class Schedule:
    def __init__(self, id, path_id, time):
        self.id = id
        self.path_id = path_id
        self.time = time


class User:
    pass
