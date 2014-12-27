# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_realcentroid.ui'
#
# Created: Sat Dec 27 17:35:18 2014
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_RealCentroid(object):
    def setupUi(self, RealCentroid):
        RealCentroid.setObjectName(_fromUtf8("RealCentroid"))
        RealCentroid.resize(389, 233)
        RealCentroid.setWindowTitle(QtGui.QApplication.translate("RealCentroid", "RealCentroid", None, QtGui.QApplication.UnicodeUTF8))
        RealCentroid.setModal(True)
        self.label = QtGui.QLabel(RealCentroid)
        self.label.setGeometry(QtCore.QRect(10, 10, 111, 21))
        self.label.setText(QtGui.QApplication.translate("RealCentroid", "Polygon layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.layerBox = QtGui.QComboBox(RealCentroid)
        self.layerBox.setGeometry(QtCore.QRect(10, 30, 371, 31))
        self.layerBox.setObjectName(_fromUtf8("layerBox"))
        self.label_2 = QtGui.QLabel(RealCentroid)
        self.label_2.setGeometry(QtCore.QRect(10, 100, 201, 21))
        self.label_2.setText(QtGui.QApplication.translate("RealCentroid", "Output point on surface layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pointEdit = QtGui.QLineEdit(RealCentroid)
        self.pointEdit.setEnabled(False)
        self.pointEdit.setGeometry(QtCore.QRect(10, 120, 291, 31))
        self.pointEdit.setObjectName(_fromUtf8("pointEdit"))
        self.browseButton = QtGui.QPushButton(RealCentroid)
        self.browseButton.setGeometry(QtCore.QRect(310, 120, 71, 31))
        self.browseButton.setText(QtGui.QApplication.translate("RealCentroid", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.addBox = QtGui.QCheckBox(RealCentroid)
        self.addBox.setGeometry(QtCore.QRect(10, 160, 361, 26))
        self.addBox.setText(QtGui.QApplication.translate("RealCentroid", "Add to map canvas", None, QtGui.QApplication.UnicodeUTF8))
        self.addBox.setObjectName(_fromUtf8("addBox"))
        self.cancelButton = QtGui.QPushButton(RealCentroid)
        self.cancelButton.setGeometry(QtCore.QRect(310, 190, 71, 31))
        self.cancelButton.setText(QtGui.QApplication.translate("RealCentroid", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.okButton = QtGui.QPushButton(RealCentroid)
        self.okButton.setGeometry(QtCore.QRect(220, 190, 71, 31))
        self.okButton.setText(QtGui.QApplication.translate("RealCentroid", "Ok", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setObjectName(_fromUtf8("okButton"))
        self.selectedBox = QtGui.QCheckBox(RealCentroid)
        self.selectedBox.setGeometry(QtCore.QRect(10, 70, 361, 26))
        self.selectedBox.setText(QtGui.QApplication.translate("RealCentroid", "Selected features only", None, QtGui.QApplication.UnicodeUTF8))
        self.selectedBox.setObjectName(_fromUtf8("selectedBox"))

        self.retranslateUi(RealCentroid)
        QtCore.QMetaObject.connectSlotsByName(RealCentroid)

    def retranslateUi(self, RealCentroid):
        pass

