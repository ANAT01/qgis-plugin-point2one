# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frmPoints2One.ui'
#
# Created: Sun Mar  8 04:15:15 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(289, 377)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.vboxlayout = QtGui.QVBoxLayout(self.groupBox)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.inShape = QtGui.QComboBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inShape.sizePolicy().hasHeightForWidth())
        self.inShape.setSizePolicy(sizePolicy)
        self.inShape.setObjectName(_fromUtf8("inShape"))
        self.vboxlayout.addWidget(self.inShape)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox1 = QtGui.QGroupBox(Dialog)
        self.groupBox1.setObjectName(_fromUtf8("groupBox1"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox1)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rdoPolygon = QtGui.QRadioButton(self.groupBox1)
        self.rdoPolygon.setChecked(True)
        self.rdoPolygon.setAutoRepeat(False)
        self.rdoPolygon.setObjectName(_fromUtf8("rdoPolygon"))
        self.horizontalLayout_2.addWidget(self.rdoPolygon)
        self.rdoPolyline = QtGui.QRadioButton(self.groupBox1)
        self.rdoPolyline.setChecked(False)
        self.rdoPolyline.setAutoRepeat(False)
        self.rdoPolyline.setObjectName(_fromUtf8("rdoPolyline"))
        self.horizontalLayout_2.addWidget(self.rdoPolyline)
        self.rdoPolylineClosed = QtGui.QCheckBox(self.groupBox1)
        self.rdoPolylineClosed.setEnabled(False)
        self.rdoPolylineClosed.setCheckable(True)
        self.rdoPolylineClosed.setChecked(True)
        self.rdoPolylineClosed.setObjectName(_fromUtf8("rdoPolylineClosed"))
        self.horizontalLayout_2.addWidget(self.rdoPolylineClosed)
        self.gridLayout.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.groupBox1)
        self.groupBox2 = QtGui.QGroupBox(Dialog)
        self.groupBox2.setObjectName(_fromUtf8("groupBox2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox2)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.rdoKeyName = QtGui.QCheckBox(self.groupBox2)
        self.rdoKeyName.setAutoExclusive(False)
        self.rdoKeyName.setObjectName(_fromUtf8("rdoKeyName"))
        self.verticalLayout_3.addWidget(self.rdoKeyName)
        self.attrName = QtGui.QComboBox(self.groupBox2)
        self.attrName.setEnabled(False)
        self.attrName.setObjectName(_fromUtf8("attrName"))
        self.verticalLayout_3.addWidget(self.attrName)
        self.chbSort = QtGui.QCheckBox(self.groupBox2)
        self.chbSort.setEnabled(False)
        self.chbSort.setObjectName(_fromUtf8("chbSort"))
        self.verticalLayout_3.addWidget(self.chbSort)
        self.verticalLayout.addWidget(self.groupBox2)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self._2 = QtGui.QVBoxLayout(self.groupBox_2)
        self._2.setObjectName(_fromUtf8("_2"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.outShape = QtGui.QLineEdit(self.groupBox_2)
        self.outShape.setObjectName(_fromUtf8("outShape"))
        self.hboxlayout.addWidget(self.outShape)
        self.btnBrowse = QtGui.QPushButton(self.groupBox_2)
        self.btnBrowse.setObjectName(_fromUtf8("btnBrowse"))
        self.hboxlayout.addWidget(self.btnBrowse)
        self._2.addLayout(self.hboxlayout)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.encodingLabel = QtGui.QLabel(self.groupBox_2)
        self.encodingLabel.setObjectName(_fromUtf8("encodingLabel"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.encodingLabel)
        self.cmbOutEncoding = QtGui.QComboBox(self.groupBox_2)
        self.cmbOutEncoding.setObjectName(_fromUtf8("cmbOutEncoding"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.cmbOutEncoding)
        self._2.addLayout(self.formLayout)
        self.verticalLayout.addWidget(self.groupBox_2)
        spacerItem = QtGui.QSpacerItem(13, 13, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(6)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.horizontalLayout.addWidget(self.progressBar)
        self.buttonBox_2 = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_2.setObjectName(_fromUtf8("buttonBox_2"))
        self.horizontalLayout.addWidget(self.buttonBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox_2, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QObject.connect(self.buttonBox_2, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.rdoKeyName, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.attrName.setEnabled)
        QtCore.QObject.connect(self.rdoKeyName, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chbSort.setEnabled)
        QtCore.QObject.connect(self.rdoPolyline, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.rdoPolylineClosed.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.inShape, self.rdoPolygon)
        Dialog.setTabOrder(self.rdoPolygon, self.rdoPolyline)
        Dialog.setTabOrder(self.rdoPolyline, self.rdoKeyName)
        Dialog.setTabOrder(self.rdoKeyName, self.attrName)
        Dialog.setTabOrder(self.attrName, self.chbSort)
        Dialog.setTabOrder(self.chbSort, self.outShape)
        Dialog.setTabOrder(self.outShape, self.btnBrowse)
        Dialog.setTabOrder(self.btnBrowse, self.cmbOutEncoding)
        Dialog.setTabOrder(self.cmbOutEncoding, self.buttonBox_2)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Points2One", None))
        self.groupBox.setTitle(_translate("Dialog", "Input point layer", None))
        self.groupBox1.setTitle(_translate("Dialog", "Output geometries", None))
        self.rdoPolygon.setText(_translate("Dialog", "Polygons", None))
        self.rdoPolyline.setText(_translate("Dialog", "Lines", None))
        self.rdoPolylineClosed.setText(_translate("Dialog", "Closed", None))
        self.groupBox2.setTitle(_translate("Dialog", "Multiple processing", None))
        self.rdoKeyName.setText(_translate("Dialog", "Create output features based on input field ", None))
        self.chbSort.setText(_translate("Dialog", "Sort points by this field", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Output shapefile", None))
        self.btnBrowse.setText(_translate("Dialog", "Browse", None))
        self.encodingLabel.setText(_translate("Dialog", "Encoding", None))

