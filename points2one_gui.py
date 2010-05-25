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
        self.manageGui()            
        self.show()
        self.success = False
        self.cancel_close = self.buttonBox_2.button( QDialogButtonBox.Close )
        self.progressBar.setValue(0)

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
            self.points2oneMulti( self.inShape.currentText(), wkbType, attrName)
            out_text = "\n"
            end_text = self.tr( "\nWould you like to add the new layer to the TOC?" )
            addToTOC = QMessageBox.question( self, "Points2One", self.tr( "Created output shapefile:" ) + "\n"
            + unicode( self.shapefileName ) + out_text + end_text, QMessageBox.Yes, QMessageBox.No, QMessageBox.NoButton )
            if addToTOC == QMessageBox.Yes:
                addShapeToCanvas( unicode( self.shapefileName ) )
            self.progressBar.setValue(0) 
        
    def outFile( self ):
        self.outShape.clear()
        ( self.shapefileName, self.encoding ) = saveDialog( self )
        if self.shapefileName is None or self.encoding is None:
            return
        self.outShape.setText( QString( self.shapefileName ) )

    #developed by Goyo Diaz (goyodiaz@gmail.com)  
    def points2oneMulti( self, myLayer, wkbType, attrName ):
        check = QFile( self.shapefileName )
        if check.exists():
            if not QgsVectorFileWriter.deleteShapeFile( self.shapefileName ):
                QMessageBox.warning( self, "Points2One", self.tr( "Unable to delete existing shapefile." ) )
                return
        layer = getVectorLayerByName( myLayer )
        provider = layer.dataProvider()
        provider.select(layer.pendingAllAttributesList(), QgsRectangle(), True, True)
        self.progressBar.setRange(0, provider.featureCount())
        writer = QgsVectorFileWriter( self.shapefileName, self.encoding, provider.fields(), wkbType, layer.srs() )
        outFeatures = iterFeatures(layer, attrName, wkbType, self.updateProgressBar)
        for outFeat in outFeatures:
            writer.addFeature(outFeat)
        del writer


#developed by Goyo Diaz (goyodiaz@gmail.com)            
def iterPoints(layer, hookFunc=None):
    """
    Iterate over the features of a point layer.

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


#developed by Goyo Diaz (goyodiaz@gmail.com)   
def iterGroups(layer, attrName, hookFunc=None):
    """
    Iterate over the features of a point layer grouping by attribute.

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


#developed by Goyo Diaz (goyodiaz@gmail.com)  
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


#developed by Goyo Diaz (goyodiaz@gmail.com)   
def makeFeature(points, wkbType):
    """
    Return a feature with given vertices.

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
def saveDialog( parent ):
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
    return ( unicode( files.first() ), unicode( fileDialog.encoding() ) )


# Convinience function to add a vector layer to canvas based on input shapefile path ( as string )
# adopted from 'fTools Plugin', Copyright (C) 2009  Carson Farmer
def addShapeToCanvas( shapeFilePath ):
    shapeFilePathList = shapeFilePath.split( "/" )
    layerName = QString( shapeFilePathList[len(shapeFilePathList)-1] )
    if layerName.endsWith( ".shp" ):
        layerName = unicode( layerName ).rstrip( ".shp" )
    vlayer_new = QgsVectorLayer( shapeFilePath, layerName, "ogr" )

    if vlayer_new.isValid():
        QgsMapLayerRegistry.instance().addMapLayer(vlayer_new)
        return True
    else:   
        return False

