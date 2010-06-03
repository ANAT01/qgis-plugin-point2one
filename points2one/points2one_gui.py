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
from os.path import splitext

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
from ui_frmPoints2One import Ui_Dialog

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
        """Set the list of available encodings to names."""
        self.cmbOutEncoding.clear()
        self.cmbOutEncoding.addItems(names)

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
        elif self.outShape.text() == "":
            QMessageBox.warning( self, "Points2One", self.tr( "Please specify output shapefile" ) )
        else:
            self.outShape.clear()
            if self.rdoPolyline.isChecked():
                wkbType = QGis.WKBLineString
            else:
                wkbType = QGis.WKBPolygon
            if self.rdoKeyName.isChecked():
                attrName = unicode(self.attrName.currentText())
            else:
                attrName = None
            self.progressBar.setRange(0, provider.featureCount())
            try:
                points2one(layer, self.shapefileName, self.getOutEncoding(), wkbType, attrName, self.updateProgressBar)
            except FileDeletionError:
                QMessageBox.warning(self, 'Points2One', self.tr('Unable to delete existing shapefile.'))
                return
            out_text = "\n"
            end_text = self.tr( "\nWould you like to add the new layer to the TOC?" )
            addToTOC = QMessageBox.question( self, "Points2One", self.tr( "Created output shapefile:" ) + "\n"
            + unicode( self.shapefileName ) + out_text + end_text, QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton )
            if addToTOC == QMessageBox.Yes:
                addShapeToCanvas( unicode( self.shapefileName ) )
            self.progressBar.setValue(0) 
        
    def outFile( self ):
        self.outShape.clear()
        self.shapefileName = saveDialog(self)
        if not self.shapefileName:
            return
        self.outShape.setText( QString( self.shapefileName ) )

    def getOutEncoding(self):
        """Return the selected encoding for the output shapefile."""
        return self.cmbOutEncoding.currentText()


def points2one(inLayer, outFileName, encoding, wkbType, attrName, hookFunc=None):
    """Create a shapefile of polygons or polylines from vertices."""
    check = QFile(outFileName)
    if check.exists():
        if not QgsVectorFileWriter.deleteShapeFile(outFileName):
            raise FileDeletionError
    provider = inLayer.dataProvider()
    provider.select(inLayer.pendingAllAttributesList(), QgsRectangle(), True, True)
    writer = QgsVectorFileWriter(outFileName, encoding, provider.fields(), wkbType, inLayer.srs())
    outFeatures = iterFeatures(inLayer, attrName, wkbType, hookFunc)
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


def iterGroups(layer, attrName, hookFunc=None):
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
        return groupby(points, lambda p: p[1][attrIdx])
    else:
        return [(None, points)]

 
def iterFeatures(layer, attrName, wkbType, hookFunc=None):
    """
    Iterate over features with vertices in a point layer.

    For each consecutive group of points with the same value for a given
    attribute, yield a feature (polygon o polyline depending on
    wkbType) with vertices in those points.
    Each time a vertice is read hookFunc is called.

    """

    groups = iterGroups(layer, attrName, hookFunc)
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
        feature.setGeometry(QgsGeometry.fromPolyline(pointList))
    elif wkbType == QGis.WKBPolygon:
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


# Generate a save file dialog with a dropdown box for choosing encoding style
# adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
def saveDialog_old( parent ):
    settings = QSettings()
    dirName = settings.value( "/UI/lastShapefileDir" ).toString()
    filtering = QString( "Shapefiles (*.shp)" )
    encode = settings.value( "/UI/encoding" ).toString()
    fileDialog = QgsEncodingFileDialog( parent, "Save output shapefile", dirName, filtering, encode )
    fileDialog.setDefaultSuffix( QString( "shp" ) )
    fileDialog.setFileMode( QFileDialog.AnyFile )
    fileDialog.setAcceptMode( QFileDialog.AcceptSave )
    fileDialog.setConfirmOverwrite( True )
    if not fileDialog.exec_() == QDialog.Accepted:
        return None, None
    files = fileDialog.selectedFiles()
    settings.setValue("/UI/lastShapefileDir", QVariant( QFileInfo( unicode( files.first() ) ).absolutePath() ) )
    # return ( unicode( files.first() ), unicode( fileDialog.encoding() ) )
    return unicode(files.first())


def saveDialog_new(parent):
    """Shows a save file dialog and return the selected file path."""
    settings = QSettings()
    key = '/UI/lastShapefileDir'
    outPath = settings.value(key).toString()
    filter = 'Shapefiles (*.shp)'
    outFilePath = QFileDialog.getSaveFileName(parent, parent.tr('Save output shapefile'), outPath, filter=filter)
    if outFilePath:
        # XXX outFilePath is not a directory path.
        dir = QDir(outFilePath)
        dir.cdUp()
        outPath = dir.absolutePath()
        settings.setValue(key, outPath)
    return outFilePath


saveDialog = saveDialog_new


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


def getEncodings_old():
    """Return a list of available encodings."""
    return ['BIG5', 'BIG5-HKSCS', 'EUCJP', 'EUCKR', 'GB2312', 'GBK',
            'GB18030', 'JIS7', 'SHIFT-JIS', 'TSCII', 'UTF-8', 'UTF-16',
            'KOI8-R', 'KOI8-U', 'ISO8859-1', 'ISO8859-2', 'ISO8859-3',
            'ISO8859-4', 'ISO8859-5', 'ISO8859-6', 'ISO8859-7',
            'ISO8859-8', 'ISO8859-8-I', 'ISO8859-9', 'ISO8859-10',
            'ISO8859-13', 'ISO8859-14', 'ISO8859-15', 'IBM 850',
            'IBM 866', 'CP874', 'CP1250', 'CP1251', 'CP1252', 'CP1253',
            'CP1254', 'CP1255', 'CP1256', 'CP1257', 'CP1258',
            'Apple Roman', 'TIS-620']


def getEncodings_new():
    """Return a list of available encodings."""
    names = [QString(QTextCodec.codecForMib(mib).name()) 
             for mib in QTextCodec.availableMibs()]
    return names


getEncodings = getEncodings_new


class FileDeletionError(Exception):
    """Exception raised when a file can't be deleted."""
    pass
