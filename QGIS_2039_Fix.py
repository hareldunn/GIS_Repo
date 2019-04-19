#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
***************************************************************************
    QGIS 2039 Fix.py
    ---------------------
    Date                 : February 2019
    Copyright            : (C) 2019 by Harel Dan
    Email                : harel dot dunn at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************
*                                                                         *
*   Update wrong EPSG:2039 transformation parameters with Systematic's    *
*   cludge of a fix for Esri button pushers. Note, the Rx value, -0.33009 *
*   IS WRONG on purpuse, official value in Measurments Regulation 2016 is *
*   -0.33077, but this is the value Systematics put in their 7 parameter  *
*   CoordFrame transformation in Esri products, so I'm using this as well.*
*   The resulting offset is 1.5 cm. Change to correct value if you need.  *
*   Change the srid_val to 6991 and put the correct value if you cherish  *
*   accuracy, as it is probably the correct thing to do.                  *
*   With this method, QGIS will recognise EPSG:2039 in the correct        *
*   position, and layers saved in QGIS will open as such in ArcWhatever.  *
*                                                                         *
*   To run, open QGIS' python console, paste and run, or load as file in  *
*   editor. Instant fix. Verify by checking the EPSG:2039 CRC parameters. *
*                                                                         *
***************************************************************************
"""

##
import os
import sqlite3
import qgis.utils

## QGIS installation verisons

db_network_path = "C:\\OSGeo4W64\\apps\\qgis\\resources\\srs.db" 
db_standalone_path = "C:\\Program Files\\QGIS "+ '.'.join(qgis.utils.Qgis.QGIS_VERSION.split('.')[:2])+"\\apps\\qgis\\resources\\srs.db" ## צובי

	
##These are the CRS/SRID to choose from:
## "2039", "Israel_TM_Grid"
## "6984", "Israel Grid 05"
## "6991", "Israel Grid 05/12"


srid_val = 2039 #Change if needed
parameters_val = "+proj=tmerc +lat_0=31.7343936111111 +lon_0=35.2045169444445 +k=1.0000067 +x_0=219529.584 +y_0=626907.39 +ellps=GRS80 +towgs84=-24.0024,-17.1032,-17.8444,-0.33077,-1.85269,1.66969,5.4248 +units=m +no_defs"

if os.path.isfile(db_network_path):
	db_path = db_network_path
else:
	db_path = db_standalone_path
	
	
db = sqlite3.connect(db_path)
cursor = db.cursor()
cursor.execute('''UPDATE tbl_srs SET parameters = ? WHERE srid = ? ''',
 (parameters_val, srid_val))
db.commit()
db.close()
print("Projection parameters for srid "+ str(srid_val) + " updated successfully")
