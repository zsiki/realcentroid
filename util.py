# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import QgsEncodingFileDialog
import locale

# Return list of names of layers in QgsMapLayerRegistry
# vTypes - list of layer types allowed (e.g. QGis.Point, QGis.Line, QGis.Polygon or "all" or "raster")
# return sorted list of layer names
def getLayerNames(vTypes):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    layerlist = []
    if vTypes == "all":
        for name, layer in layermap.iteritems():
            layerlist.append(unicode(layer.name()))
    else:
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() in vTypes:
                    layerlist.append(unicode(layer.name()))
            elif layer.type() == QgsMapLayer.RasterLayer:
                if "raster" in vTypes:
                    layerlist.append(unicode(layer.name()))
    return sorted(layerlist, cmp=locale.strcoll)

# Generate a save file dialog with a dropdown box for choosing encoding style
def saveDialog(parent, filtering="Shapefiles (*.shp)"):
    settings = QSettings()
    dirName = settings.value("/UI/lastShapefileDir")
    encode = settings.value("/UI/encoding")
    fileDialog = QgsEncodingFileDialog(parent, "Output shape file", dirName, filtering, encode)
    fileDialog.setDefaultSuffix("shp")
    fileDialog.setFileMode(QFileDialog.AnyFile)
    fileDialog.setAcceptMode(QFileDialog.AcceptSave)
    fileDialog.setConfirmOverwrite(True)
    if not fileDialog.exec_() == QDialog.Accepted:
            return None, None
    files = fileDialog.selectedFiles()
    settings.setValue("/UI/lastShapefileDir", QFileInfo(unicode(files[0])).absolutePath())
    return (unicode(files[0]), unicode(fileDialog.encoding()))

# Return QgsMapLayer from a layer name (as string)
def getMapLayerByName(myName):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.name() == myName:
            if layer.isValid():
                return layer
            else:
                return None
    return None

# add shape to canvas
def addShape(shapefile_path):
    file_info = QFileInfo(shapefile_path)
    if file_info.exists():
        layer_name = file_info.completeBaseName()
    else:
        return False
    vlayer_new = QgsVectorLayer(shapefile_path,layer_name, "ogr")
    if vlayer_new.isValid():
        QgsMapLayerRegistry.instance().addMapLayer(vlayer_new)
        return True
    else:
        return False
