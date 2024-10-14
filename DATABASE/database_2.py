import peewee
from DATABASE.models import *
import Classes.classes as cl
import re


# with db:
#     db.create_tables([BusStop, BusStopTransport, BusRoute, TimeTable])


def set_bus_stops(stops_list, number, direction):
    with db:
        for stop in stops_list:
            stop_name = stop[0]
            stop_coords = stop[1]
            # if BusStop.select().where(BusStop.name == stop_name and BusStop.coordinates == str(stop_coords) and BusStop.dir == direction).exists():
            #     bs = BusStop.get(name=stop_name, coordinates=str(stop_coords), dir=direction)
            #     BusStopTransport(
            #         stop_id=bs,
            #         path_number=number
            #     ).save()
            # else:
            #     bs = BusStop(
            #         name=stop_name,
            #         coordinates=stop_coords,
            #         dir=direction
            #     )
            #     bs.save()
            #     BusStopTransport(
            #         stop_id=bs,
            #         path_number=number
            #     ).save()
            try:
                bs = BusStop.get(name=stop_name, coordinates=str(stop_coords), dir=direction)
                BusStopTransport(
                    stop_id=bs,
                    path_number=number
                ).save()
            except:
                bs = BusStop(
                    name=stop_name,
                    coordinates=stop_coords,
                    dir=direction
                )
                bs.save()
                BusStopTransport(
                    stop_id=bs,
                    path_number=number
                ).save()


def set_route(path_list, number, name_route, direction, time, active_state=True):
    with db:
        br = BusRoute(
            number=number,
            name=name_route,
            path=path_list,
            direction=direction,
            active=active_state
        )
        br.save()
        TimeTable(
            path_id=br,
            time_table=time
        ).save()


def generate_tuple_path(path_str):
    pattern = re.compile(r"\(([^)]+)\)")
    matches = pattern.findall(path_str)
    result = [tuple(map(float, match.split(','))) for match in matches]
    # Преобразование в список кортежей
    return result


def get_bus_route_info(number, dir):
    with db:
        br = BusRoute.get(number=number, direction=dir)
        tt = TimeTable.get(path_id=br)

        id = br.id
        path = generate_tuple_path(br.path)
        number = br.number
        name = br.name
        active = br.active
        direction = br.direction
        time = cl.Schedule(tt.id, tt.path_id, tt.time_table)
        return cl.BusRoute(id, name, number, time, path, active, direction)


def generate_tuple_bus_stops(str_coords):
    return tuple(map(float, str_coords.strip('()').split(', ')))


def get_bus_stops_for_routes(number, dir):
    stops_list = []
    with db:
        bus_stops = BusStop.select().where(BusStop.dir == dir).join(BusStopTransport).where(
            BusStopTransport.path_number == number)

        for stop in bus_stops:
            id = stop.id
            coords = generate_tuple_bus_stops(stop.coordinates)
            name = stop.name
            stops_list.append(cl.BusStop(id, name, coords))
    return stops_list


def get_end_bus_stop(number, dir, need_coords=True):
    with db:
        stop_list = BusStop.select().where(BusStop.dir == dir).join(BusStopTransport).where(
            BusStopTransport.path_number == number)
        start_stop = stop_list[0]
        finish_stop = stop_list[len(stop_list)-1]
        if need_coords:
            return [(start_stop.name, start_stop.coordinates), (finish_stop.name, finish_stop.coordinates)]
        else:
            return start_stop.name, finish_stop.name

def delete_stops(id):
    with db:
        BusStop[id].delete_instance()
