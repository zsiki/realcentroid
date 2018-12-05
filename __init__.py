# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RealCentroid
                                 A QGIS plugin
 Create point shape from polygon centroids
                             -------------------
        begin                : 2013-10-27
        copyright            : (C) 2013 by Zoltan Siki
        email                : siki at agt.bme.hu
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
from __future__ import absolute_import

def classFactory(iface):
    # load RealCentroid class from file RealCentroid
    from .realcentroid import RealCentroid
    return RealCentroid(iface)
