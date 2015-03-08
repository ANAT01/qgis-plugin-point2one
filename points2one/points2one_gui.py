# -*- coding: utf-8 -*-
#-----------------------------------------------------------
# 
# Points2One
# Copyright (C) 2010 Pavol Kapusta <pavol.kapusta@gmail.com>
# Copyright (C) 2010, 2013 Goyo <goyodiaz@gmail.com>
#-----------------------------------------------------------
# 
# licensed under the terms of GNU GPL 2
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
# 
#---------------------------------------------------------------------

from itertools import groupby
from os.path import basename
from os.path import dirname
from os.path import splitext

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from ui_frmPoints2One import Ui_Dialog
from p2o_encodings import getEncodings
from p2o_encodings import getDefaultEncoding
from p2o_encodings import setDefaultEncoding
from p2o_engine import Engine


class points2One(QDialog, Ui_Dialog):
    def __init__(self, iface):
        QDialog.__init__(self)
        self.iface = iface
        self.setupUi(self)
        QObject.connect(self.btnBrowse, SIGNAL('clicked()'), self.outFile)
        QObject.connect(self.inShape, SIGNAL('currentIndexChanged(QString)'), self.update)
        self.populate_encodings(getEncodings())
        self.manageGui()
        self.show()

    def layer_name(self):
        """Return the selected layer name as unicode."""
        return unicode(self.inShape.currentText())

    def layer(self):
        """Return the selected layer."""
        name = self.layer_name()
        if name:
            return getVectorLayerByName(self.layer_name())

    def output_geometry(self):
        """Return the selected output geometry."""
        if self.rdoPolyline.isChecked():
            return QGis.WKBLineString
        else:
            return QGis.WKBPolygon

    def polyline_closed(self):
        """Return the selected output geometry."""
        if self.rdoPolylineClosed.isChecked():
            return True
        else:
            return False

    def group_attr_enabled(self):
        """Return whether grouping by attribute is enabled."""
        return self.rdoKeyName.isChecked()

    def group_attr_name(self):
        """Return the name of the grouping attribute."""
        if self.group_attr_enabled():
            return unicode(self.attrName.currentText())

    def sort_enabled(self):
        """Return whether sorting is enabled."""
        return self.chbSort.isChecked()

    def output_encoding(self):
        """Return the selected encoding for the output shapefile."""
        return unicode(self.cmbOutEncoding.currentText())

    def check_input(self):
        """Check whether the input is valid."""
        layer = self.layer()
        if layer is None:
            msg = self.tr('Please specify an input layer')
            QMessageBox.warning(self, 'Points2One', msg)
            return False

        provider = layer.dataProvider()
        if (self.output_geometry() == QGis.WKBLineString and
                provider.featureCount() < 2):
            msg = self.tr('Polyline: Please select input layer with at least 2 points')
            QMessageBox.warning(self, 'Points2One', msg)
            return False

        if (self.output_geometry() == QGis.WKBPolygon and
                provider.featureCount() < 3):
            self.tr('Polygon: Please select input layer with at least 3 points')
            QMessageBox.warning(self, 'Points2One', msg)
            return False

        if self.group_attr_enabled() and self.group_attr_name() == '':
            msg = self.tr('Please define specific input field')
            QMessageBox.warning(self, 'Points2One', msg)
            return False

        if self.getOutFilePath() == '':
            msg = self.tr('Please specify output shapefile')
            QMessageBox.warning(self, 'Points2One', msg)
            return False

        return True

    def populate_encodings(self, names):
        """Populate the combo box of available encodings."""
        self.cmbOutEncoding.clear()
        self.cmbOutEncoding.addItems(names)
        index = self.cmbOutEncoding.findText(getDefaultEncoding())
        if index == -1:
            index = 0  # Make sure some encoding is selected.
        self.cmbOutEncoding.setCurrentIndex(index)

    def update_progress_bar(self):
        """Update the progress bar."""
        self.progressBar.setValue(self.progressBar.value() + 1)

    def update(self):
        self.attrName.clear()
        layer = self.layer()
        if layer is not None:
            fields = layer.dataProvider().fields()
            for field in fields:
                name = field.name()
                self.attrName.addItem(name)

    def manageGui(self):
        myList = []
        self.inShape.clear()
        myList = getLayerNames([QGis.Point])
        self.inShape.addItems(myList)

    def accept(self):
        if not self.check_input():
            return

        layer = self.layer()
        self.progressBar.setRange(0, layer.dataProvider().featureCount())
        setDefaultEncoding(self.output_encoding())
        engine = Engine(
            layer,
            self.getOutFilePath(),
            self.output_encoding(),
            self.output_geometry(),
            self.polyline_closed(),
            self.group_attr_name(),
            self.update_progress_bar,
            self.sort_enabled()
        )
        try:
            engine.run()
        except FileDeletionError:
            message = self.tr('Unable to delete existing shapefile.')
            QMessageBox.warning(self, 'Points2One', message)
            return

        # Show warning
        log_msg = '\n'.join(engine.get_logger())
        if log_msg:
            warningBox = QMessageBox(self)
            warningBox.setWindowTitle('Points2One')
            message = self.tr('Output shapefile created')
            warningBox.setText(message)
            message = self.tr('There were some issues, maybe some features could not be created.')
            warningBox.setInformativeText(message)
            warningBox.setDetailedText(log_msg)
            warningBox.setIcon(QMessageBox.Warning)
            warningBox.exec_()

        message = unicode(self.tr('Created output shapefile:'))
        message = '\n'.join([message, unicode(self.getOutFilePath())])
        message = '\n'.join([message,
            unicode(self.tr('Would you like to add the new layer to the TOC?'))])
        addToTOC = QMessageBox.question(self, "Points2One", message,
            QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
        if addToTOC == QMessageBox.Yes:
            addShapeToCanvas(unicode(self.getOutFilePath()))
        self.progressBar.setValue(0)

    def outFile(self):
        """Open a file save dialog and set the output file path."""
        outFilePath = saveDialog(self)
        if not outFilePath:
            return
        self.setOutFilePath(outFilePath)

    def getOutFilePath(self):
        """Return the output file path."""
        return self.outShape.text()

    def setOutFilePath(self, outFilePath):
        """Set the output file path."""
        self.outShape.setText(outFilePath)


# Return QgsVectorLayer from a layer name ( as string )
# adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
def getVectorLayerByName( myName ):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type() == QgsMapLayer.VectorLayer and layer.name() == myName:
            if layer.isValid():
                return layer
            else:
                return None


# Return list of names of all layers in QgsMapLayerRegistry
# adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
def getLayerNames(vTypes):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    layerlist = []
    if vTypes == 'all':
        for name, layer in layermap.iteritems():
            layerlist.append(unicode(layer.name()))
    else:
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() in vTypes:
                    layerlist.append(unicode(layer.name()))
    return layerlist


def saveDialog(parent):
    """Shows a save file dialog and return the selected file path."""
    settings = QSettings()
    key = '/UI/lastShapefileDir'
    outDir = settings.value(key)
    filter = 'Shapefiles (*.shp)'
    outFilePath = QFileDialog.getSaveFileName(parent, parent.tr('Save output shapefile'), outDir, filter)
    outFilePath = unicode(outFilePath)
    if outFilePath:
        root, ext = splitext(outFilePath)
        if ext.upper() != '.SHP':
            outFilePath = '%s.shp' % outFilePath
        outDir = dirname(outFilePath)
        settings.setValue(key, outDir)
    return outFilePath


# Convenience function to add a vector layer to canvas based on input
# shapefile path (as string).
# Adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
def addShapeToCanvas(shapeFilePath):
    layerName = basename(shapeFilePath)
    root, ext = splitext(layerName)
    if ext == '.shp':
        layerName = root
    vlayer_new = QgsVectorLayer(shapeFilePath, layerName, "ogr")
    ret = QgsMapLayerRegistry.instance().addMapLayer(vlayer_new)
    return ret


class FileDeletionError(Exception):
    """Exception raised when a file can't be deleted."""
    pass
