from GUI.interfaceAutorization import open_window
import Classes.classes as cl
import DATABASE.database_2 as db
import numpy as np
from scipy.interpolate import splprep, splev
from JsonFilesImport.generate_paths_and_stops import *

# print(db.get_end_bus_stop(7, True, need_coords=False))
# generate_info(2, False, 15)
# gui.startMain()
open_window()
# print(db.get_end_bus_stop(7, False, False))
# print(db.get_end_bus_stop(7, True, False))