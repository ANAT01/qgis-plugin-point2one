# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmPoints2One.ui'
#
# Created: Thu Jun  3 13:38:20 2010
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(313, 403)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.rdoPolygon = QtGui.QRadioButton(self.groupBox)
        self.rdoPolygon.setChecked(True)
        self.rdoPolygon.setAutoRepeat(False)
        self.rdoPolygon.setObjectName("rdoPolygon")
        self.verticalLayout.addWidget(self.rdoPolygon)
        self.rdoPolyline = QtGui.QRadioButton(self.groupBox)
        self.rdoPolyline.setChecked(False)
        self.rdoPolyline.setAutoRepeat(False)
        self.rdoPolyline.setObjectName("rdoPolyline")
        self.verticalLayout.addWidget(self.rdoPolyline)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout.addWidget(self.progressBar)
        self.buttonBox_2 = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_2.setObjectName("buttonBox_2")
        self.horizontalLayout.addWidget(self.buttonBox_2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 6, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(0, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem, 5, 0, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName("groupBox_2")
        self._2 = QtGui.QVBoxLayout(self.groupBox_2)
        self._2.setObjectName("_2")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")
        self.outShape = QtGui.QLineEdit(self.groupBox_2)
        self.outShape.setReadOnly(True)
        self.outShape.setObjectName("outShape")
        self.hboxlayout.addWidget(self.outShape)
        self.btnBrowse = QtGui.QPushButton(self.groupBox_2)
        self.btnBrowse.setObjectName("btnBrowse")
        self.hboxlayout.addWidget(self.btnBrowse)
        self._2.addLayout(self.hboxlayout)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.encodingLabel = QtGui.QLabel(self.groupBox_2)
        self.encodingLabel.setObjectName("encodingLabel")
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.encodingLabel)
        self.cmbOutEncoding = QtGui.QComboBox(self.groupBox_2)
        self.cmbOutEncoding.setObjectName("cmbOutEncoding")
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmbOutEncoding)
        self._2.addLayout(self.formLayout)
        self.gridLayout_2.addWidget(self.groupBox_2, 4, 0, 1, 1)
        self.groupBox1 = QtGui.QGroupBox(Dialog)
        self.groupBox1.setObjectName("groupBox1")
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.rdoKeyName = QtGui.QCheckBox(self.groupBox1)
        self.rdoKeyName.setAutoExclusive(False)
        self.rdoKeyName.setObjectName("rdoKeyName")
        self.verticalLayout_3.addWidget(self.rdoKeyName)
        self.attrName = QtGui.QComboBox(self.groupBox1)
        self.attrName.setEnabled(False)
        self.attrName.setObjectName("attrName")
        self.verticalLayout_3.addWidget(self.attrName)
        self.gridLayout_2.addWidget(self.groupBox1, 2, 0, 1, 1)
        self.groupBox2 = QtGui.QGroupBox(Dialog)
        self.groupBox2.setObjectName("groupBox2")
        self.vboxlayout = QtGui.QVBoxLayout(self.groupBox2)
        self.vboxlayout.setObjectName("vboxlayout")
        self.inShape = QtGui.QComboBox(self.groupBox2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inShape.sizePolicy().hasHeightForWidth())
        self.inShape.setSizePolicy(sizePolicy)
        self.inShape.setObjectName("inShape")
        self.vboxlayout.addWidget(self.inShape)
        self.gridLayout_2.addWidget(self.groupBox2, 0, 0, 1, 1)
        self.verticalLayout_4.addLayout(self.gridLayout_2)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox_2, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QObject.connect(self.buttonBox_2, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.rdoKeyName, QtCore.SIGNAL("clicked(bool)"), self.attrName.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Points2One", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dialog", "Points to one", None, QtGui.QApplication.UnicodeUTF8))
        self.rdoPolygon.setText(QtGui.QApplication.translate("Dialog", "Polygon", None, QtGui.QApplication.UnicodeUTF8))
        self.rdoPolyline.setText(QtGui.QApplication.translate("Dialog", "Polyline", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Dialog", "Output shapefile", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowse.setText(QtGui.QApplication.translate("Dialog", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.encodingLabel.setText(QtGui.QApplication.translate("Dialog", "Encoding", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox1.setTitle(QtGui.QApplication.translate("Dialog", "Multiple processing", None, QtGui.QApplication.UnicodeUTF8))
        self.rdoKeyName.setText(QtGui.QApplication.translate("Dialog", "Create output features based on input field ", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox2.setTitle(QtGui.QApplication.translate("Dialog", "Input point layer", None, QtGui.QApplication.UnicodeUTF8))
