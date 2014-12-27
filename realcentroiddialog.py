# -*- coding: utf-8 -*-
"""
/***************************************************************************
 RealCentroidDialog
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

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import Qt
from ui_realcentroid import Ui_RealCentroid
from qgis.core import *
from qgis.utils import *
import util

# create the dialog for real centroids
class RealCentroidDialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
        self.ui = Ui_RealCentroid()
        self.ui.setupUi(self)
        # add action to buttons
        self.ui.browseButton.clicked.connect(self.browse)
        self.ui.okButton.clicked.connect(self.ok)
        self.ui.cancelButton.clicked.connect(self.reject)
        # layer changed event
        self.ui.layerBox.currentIndexChanged.connect(self.sel)

    def showEvent(self, event):
        # remove previous entries from layer list
        self.ui.layerBox.clear()
        # remove previous shape path
        self.ui.pointEdit.clear()
        # add polygon layers to list
        names = util.getLayerNames([QGis.Polygon])
        self.ui.layerBox.addItems(names)
        if iface.activeLayer():
            # set active item in list to the active layer
            i = 0
            for name in names:
                l = util.getMapLayerByName(name)
                if l == iface.activeLayer():
                    self.ui.layerBox.setCurrentIndex(i)
                    break
                i += 1

    def sel(self):
        """ enable/disable selected features only checkbox
        """
        self.ui.selectedBox.setEnabled(False)
        self.ui.selectedBox.setCheckState(Qt.Unchecked)
        if i >= 0:
            l = util.getMapLayerByName(self.ui.layerBox.currentText())
            if l is not None:
                sf = l.selectedFeatures()
                if sf is not None and len(sf):
                    self.ui.selectedBox.setEnabled(True)
                    self.ui.selectedBox.setCheckState(Qt.Checked)

    def browse(self):
        self.ui.pointEdit.clear()    # clear output file field
        # open file dialog
        (self.shapefileName, self.encoding) = util.saveDialog(self)
        if self.shapefileName is None or self.encoding is None:
            return
        self.ui.pointEdit.setText(self.shapefileName)  # fill output file field

    def ok(self):
        if len(self.ui.layerBox.currentText()) == 0:
            QtGui.QMessageBox.information(self, "Realcentroid", "No polygon layer selected")
            return
        if len(self.ui.pointEdit.text()) == 0:
            QtGui.QMessageBox.information(self, "Realcentroid", "No point layer given")
            return
        self.accept()
