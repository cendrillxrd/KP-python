from peewee import *

db = SqliteDatabase('C:/Users/Admin/PycharmProjects/КП/DATABASE/routes.db', pragmas={'foreign_keys': 1})


class BaseModel(Model):
    id = PrimaryKeyField(unique=True)

    class Meta:
        database = db
        order_by = 'id'


class User(BaseModel):
    login = TextField()
    password = TextField()
    admin = BooleanField()
    driver = BooleanField()

    class Meta:
        db_table = 'users'


class BusStop(BaseModel):
    name = TextField()
    coordinates = TextField()
    dir = BooleanField()

    class Meta:
        db_table = 'bus_stops'


class BusStopTransport(BaseModel):
    stop_id = ForeignKeyField(BusStop, on_delete='CASCADE')
    path_number = IntegerField()

    class Meta:
        db_table = 'bus_stops_transports'


class BusRoute(BaseModel):
    number = IntegerField()
    name = TextField()
    path = TextField()
    active = BooleanField()
    direction = BooleanField()

    class Meta:
        db_table = 'bus_routes'


class TimeTable(BaseModel):
    path_id = ForeignKeyField(BusRoute, on_delete='CASCADE')
    time_table = IntegerField()

    class Meta:
        db_table = 'time_tables'
