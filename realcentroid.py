# i*- coding: utf-8 -*-
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
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import QSettings, QCoreApplication, QTranslator, Qt
from PyQt4.QtGui import QAction, QIcon, QApplication, QMessageBox
from qgis.core import *
from qgis.utils import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from realcentroiddialog import RealCentroidDialog
import os.path
import util
from math import sqrt

class RealCentroid:

    def __init__(self, iface):
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'realcentroid_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = RealCentroidDialog()

    def initGui(self):
        # Create action that will start plugin configuration
        self.action = QAction(
            QIcon(":/plugins/realcentroid/icon.png"),
            u"Real centroids", self.iface.mainWindow())
        # connect the action to the run method
        self.action.triggered.connect(self.run)

        # Add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(u"&realcentroid", self.action)

    def unload(self):
        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&realcentroid", self.action)
        self.iface.removeToolBarIcon(self.action)

    # create centroids shape file
    def centroids(self):
        vlayer = util.getMapLayerByName(self.dlg.ui.layerBox.currentText())
        vprovider = vlayer.dataProvider()
        writer = QgsVectorFileWriter(self.dlg.shapefileName, self.dlg.encoding, vprovider.fields(), QGis.WKBPoint, vprovider.crs())
        inFeat = QgsFeature()
        outFeat = QgsFeature()
        if self.dlg.ui.selectedBox.isChecked():
            features = vlayer.selectedFeatures()
        else:
            features = vlayer.getFeatures()
        nElement = 0
        nError = 0
        for inFeat in features:
            nElement += 1
            inGeom = inFeat.geometry()
            if inGeom is None or inGeom.isGeosEmpty() or not inGeom.isGeosValid():
                
                QgsMessageLog.logMessage("Feature %d skipped (empty or invalid geometry)" % nElement, 'realcentroid')
                nError += 1
                continue
            if inGeom.isMultipart():
                # find largest part in case of multipart
                maxarea = 0
                tmpGeom = QgsGeometry()
                for part in inGeom.asGeometryCollection():
                    area = part.area()
                    if area > maxarea:
                        tmpGeom = part
                        maxarea = area
                inGeom = tmpGeom
            atMap = inFeat.attributes()
            if QGis.QGIS_VERSION > '2.4':
                outGeom = inGeom.pointOnSurface()
                if outGeom is None:
                    # pointOnSurface failed
                    outGeom = inGeom.centroid()
            else:
                outGeom = inGeom.centroid()
            if not inGeom.contains(outGeom):
                # weight point outside the polygon
                # find intersection of horizontal line through the weight pont
                rect = inGeom.boundingBox()
                horiz = QgsGeometry.fromPolyline([QgsPoint(rect.xMinimum(), outGeom.asPoint()[1]), QgsPoint(rect.xMaximum(), outGeom.asPoint()[1])])
                line = horiz.intersection(inGeom)
                if line is None:
                    # skip invalid geometry
                    QgsMessageLog.logMessage("Feature %d skipped (empty or invalid geometry)" % nElement, 'realcentroid')
                    nError += 1
                    continue
                elif line.isMultipart():
                    # find longest intersection
                    mline = line.asMultiPolyline()
                    l = 0
                    for i in range(len(mline)):
                        d = sqrt((mline[i][0][0] - mline[i][1][0])**2 + (mline[i][0][1] - mline[i][1][1])**2)
                        if d > l:
                            l = d
                            xMid = (mline[i][0][0] + mline[i][1][0]) / 2.0
                            yMid = (mline[i][0][1] + mline[i][1][1]) / 2.0
                else:
                    xMid = (line.vertexAt(0).x() + line.vertexAt(1).x()) / 2.0
                    yMid = (line.vertexAt(0).y() + line.vertexAt(1).y()) / 2.0
                outGeom = QgsGeometry.fromPoint(QgsPoint(xMid, yMid))
            outFeat.setAttributes(atMap)
            outFeat.setGeometry(outGeom)
            writer.addFeature(outFeat)
        del writer
        # add centroid shape to canvas
        if self.dlg.ui.addBox.checkState() == Qt.Checked:
            if not util.addShape(self.dlg.shapefileName):
                QMessageBox.warning(None, "RealCentroid", \
                    QApplication.translate("RealCentroid", \
                    "Error loading shapefile:\n", None, \
                    QApplication.UnicodeUTF8) + self.dlg.shapefileName)
        if nError > 0:
            QMessageBox.warning(None, "RealCentroid", \
                QApplication.translate("RealCentroid", \
                "Invalid or empty geometries found, see log messages"))

    # run method that performs all the real work
    def run(self):
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result == 1 and len(self.dlg.ui.layerBox.currentText()) and len(self.dlg.ui.pointEdit.text()):
            self.centroids()
