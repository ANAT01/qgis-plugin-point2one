# -*- coding: utf-8 -*-
#-----------------------------------------------------------
# 
# Points2One
# Copyright (C) 2010 Pavol Kapusta & Goyo Diaz
# pavol.kapusta@gmail.com
# goyodiaz@gmail.com
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


class points2One( QDialog, Ui_Dialog ):
    def __init__( self, iface ):
        QDialog.__init__( self )
        self.iface = iface
        self.setupUi( self )
        QObject.connect( self.btnBrowse, SIGNAL( "clicked()" ), self.outFile )
        QObject.connect( self.inShape, SIGNAL( "currentIndexChanged(QString)" ), self.checkLayer )
        QObject.connect( self.inShape, SIGNAL( "currentIndexChanged(QString)" ), self.update )
        self.setEncodings(getEncodings())
        self.manageGui()   
        self.show()

    def setEncodings(self, names):
        """Populate the combo box of available encodings."""
        self.cmbOutEncoding.clear()
        self.cmbOutEncoding.addItems(names)
        index = self.cmbOutEncoding.findText(getDefaultEncoding())
        if index == -1:
            index = 0  # Make sure some encoding is selected.
        self.cmbOutEncoding.setCurrentIndex(index)

    def updateProgressBar(self):
        self.progressBar.setValue(self.progressBar.value() + 1)

    def checkLayer( self ):
        inputLayer = unicode( self.inShape.currentText() )
        if inputLayer != "":
            changedLayer = getVectorLayerByName( inputLayer )

    def update( self ):
        self.attrName.clear()
        inputLayer = unicode( self.inShape.currentText() )
        if inputLayer != "":
            changedLayer = getVectorLayerByName( inputLayer )
            changedField = changedLayer.dataProvider().fields()
            for i in changedField:
                self.attrName.addItem( unicode( changedField[i].name() ) )

    def manageGui( self ):
        myList = []
        self.inShape.clear()
        myList = getLayerNames( [ QGis.Point ] )
        self.inShape.addItems( myList )
        return

    def accept( self ):
        if self.inShape.currentText() == "":
            QMessageBox.warning( self, "Points2One", self.tr( "Please specify an input layer" ) )
            return
        else:
            inputLayer = unicode( self.inShape.currentText() )  
            layer = getVectorLayerByName( inputLayer )
            provider = layer.dataProvider()
        if self.rdoPolyline.isChecked() and provider.featureCount() < 2:
            QMessageBox.warning( self, "Points2One", self.tr( "Polyline: Please select input layer with at least 2 points" ) )
        elif self.rdoPolygon.isChecked() and provider.featureCount() < 3:            
            QMessageBox.warning( self, "Points2One", self.tr( "Polygon: Please select input layer with at least 3 points" ) )
        elif self.attrName.isEnabled() and self.attrName.currentText() == "":
            QMessageBox.warning( self, "Points2One", self.tr( "Please define specific input field" ) )
        elif self.getOutFilePath() == "":
            QMessageBox.warning( self, "Points2One", self.tr( "Please specify output shapefile" ) )
        else:
            if self.rdoPolyline.isChecked():
                wkbType = QGis.WKBLineString
            else:
                wkbType = QGis.WKBPolygon
            if self.rdoKeyName.isChecked():
                attrName = unicode(self.attrName.currentText())
            else:
                attrName = None
            self.progressBar.setRange(0, provider.featureCount())
            setDefaultEncoding(self.getOutEncoding())
            try:
                points2one(layer, self.getOutFilePath(), self.getOutEncoding(), wkbType, attrName, self.updateProgressBar, self.getSort())
            except FileDeletionError:
                QMessageBox.warning(self, 'Points2One', self.tr('Unable to delete existing shapefile.'))
                return
            out_text = "\n"
            end_text = self.tr( "\nWould you like to add the new layer to the TOC?" )
            addToTOC = QMessageBox.question(self, "Points2One", self.tr("Created output shapefile:") + "\n"
            + unicode(self.getOutFilePath()) + out_text + end_text, QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton)
            if addToTOC == QMessageBox.Yes:
                addShapeToCanvas(unicode(self.getOutFilePath()))
            self.progressBar.setValue(0) 
        
    def outFile(self):
        """Open a file save dialog and set the output file path."""
        outFilePath = saveDialog(self)
        if not outFilePath:
            return
        self.setOutFilePath(QString(outFilePath))

    def getOutEncoding(self):
        """Return the selected encoding for the output shapefile."""
        return self.cmbOutEncoding.currentText()

    def getSort(self):
        return self.chbSort.isChecked()

    def getOutFilePath(self):
        """Return the output file path."""
        return self.outShape.text()

    def setOutFilePath(self, outFilePath):
        """Set the output file path."""
        self.outShape.setText(outFilePath)


def points2one(inLayer, outFileName, encoding, wkbType, attrName, hookFunc=None, sort=False):
    """Create a shapefile of polygons or polylines from vertices."""
    check = QFile(outFileName)
    if check.exists():
        if not QgsVectorFileWriter.deleteShapeFile(outFileName):
            raise FileDeletionError
    provider = inLayer.dataProvider()
    provider.select(inLayer.pendingAllAttributesList(), QgsRectangle(), True, True)
    writer = QgsVectorFileWriter(outFileName, encoding, provider.fields(), wkbType, inLayer.srs())
    outFeatures = iterFeatures(inLayer, attrName, wkbType, hookFunc, sort)
    for outFeat in outFeatures:
        writer.addFeature(outFeat)
    del writer

def iterPoints(layer, hookFunc=None):
    """Iterate over the features of a point layer.

    Yield pairs of the form (QgsPoint, attributeMap).
    Each time a vertice is read hookFunc is called.

    """

    provider = layer.dataProvider()
    feat = QgsFeature()
    while(provider.nextFeature(feat)):
        hookFunc()
        geom = feat.geometry()
        x = geom.asPoint().x()
        y = geom.asPoint().y()
        yield(QgsPoint(x, y), feat.attributeMap())

def iterGroups(layer, attrName, hookFunc=None, sort=False):
    """Iterate over the features of a point layer grouping by attribute.

    Return an iterator of (key, points) pairs where key is the attribute
    value and points is an iterator of (QgsPoint, attributeMap) pairs.
    Each time a point is read hookFunc is called.

    """

    points = iterPoints(layer, hookFunc)
    provider = layer.dataProvider()
    if attrName:
        attrIdx = provider.fieldNameIndex(attrName)
        if attrIdx < 0:
            raise UnknownAttributeError
        if sort:
            points = sorted(points, key=lambda p: p[1][attrIdx].toString())
        return groupby(points, lambda p: p[1][attrIdx])
    else:
        return [(None, points)]

def iterFeatures(layer, attrName, wkbType, hookFunc=None, sort=False):
    """
    Iterate over features with vertices in a point layer.

    For each consecutive group of points with the same value for a given
    attribute, yield a feature (polygon o polyline depending on
    wkbType) with vertices in those points.
    Each time a vertice is read hookFunc is called.

    """

    groups = iterGroups(layer, attrName, hookFunc, sort)
    for key, points in groups:
        feature = makeFeature(points, wkbType)
        yield feature

def makeFeature(points, wkbType):
    """Return a feature with given vertices.

    Vertices are given as (QgsPoint, attributeMap) pairs. Returned
    feature is polygon or polyline depending on wkbType.

    """

    pointList = []
    for point in points:
        pointList.append(point[0])
    atMap = point[1]
    feature = QgsFeature()
    if wkbType == QGis.WKBLineString:
        if len(pointList) < 2:
            raise ValueError, 'Can\'t make a plyline out of %s points' % len(pointList)
        feature.setGeometry(QgsGeometry.fromPolyline(pointList))
    elif wkbType == QGis.WKBPolygon:
        if len(pointList) < 3:
            raise ValueError, 'Can\'t make a polygon out of %s points' % len(pointList)
        feature.setGeometry(QgsGeometry.fromPolygon([pointList]))
    else:
        raise ValueError, 'Invalid geometry type: %s.' % wkbType
    feature.setAttributeMap(atMap)
    return feature
                                                                       
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
def getLayerNames( vTypes ):
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    layerlist = []
    if vTypes == "all":
        for name, layer in layermap.iteritems():
            layerlist.append( unicode( layer.name() ) )
    else:
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer:
                if layer.geometryType() in vTypes:
                    layerlist.append( unicode( layer.name() ) )
    return layerlist

def saveDialog(parent):
    """Shows a save file dialog and return the selected file path."""
    settings = QSettings()
    key = '/UI/lastShapefileDir'
    outDir = settings.value(key).toString()
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

# Convinience function to add a vector layer to canvas based on input shapefile path ( as string )
# adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
def addShapeToCanvas(shapeFilePath):
    layerName = basename(shapeFilePath)
    root, ext = splitext(layerName)
    if ext == '.shp':
        layerName = root
    vlayer_new = QgsVectorLayer(shapeFilePath, layerName, "ogr")
    if vlayer_new.isValid():
        QgsMapLayerRegistry.instance().addMapLayer(vlayer_new)
        return True
    else:   
        return False


class FileDeletionError(Exception):
    """Exception raised when a file can't be deleted."""
    pass
