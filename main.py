from GUI.interfaceAutorization import open_window
from GUI.interface import startMain
import Classes.classes as cl
import DATABASE.database_2 as db
import numpy as np
from scipy.interpolate import splprep, splev
from JsonFilesImport.generate_paths_and_stops import *

# print(db.get_end_bus_stop(7, True, need_coords=False))
# generate_info(77, True, 20)
startMain()
# open_window()
# print(db.get_end_bus_stop(7, False, False))
# print(db.get_end_bus_stop(7, True, False))