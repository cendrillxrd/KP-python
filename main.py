from GUI.interfaceAutorization import open_window
from GUI.interface import startMain
import Classes.classes as cl
import DATABASE.database_2 as db
import numpy as np
from scipy.interpolate import splprep, splev
from JsonFilesImport.generate_paths_and_stops import *

# print(db.get_end_bus_stop(7, True, need_coords=False))
#generate_info(14, True, 45)
#user = cl.User('admin', 123, True, True)
#startMain(user)
open_window()
# print(db.get_end_bus_stop(7, False, False))
# print(db.get_end_bus_stop(7, True, False))