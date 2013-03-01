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
from qgis.core import *


class Engine(object):
    """Data processing for Point2One."""

    def __init__(self, layer, fname, encoding, wkb_type, attr_name=None,
                 hook=None, sort=False):
        self.layer = layer
        self.fname = fname
        self.encoding = encoding
        self.wkb_type = wkb_type
        self.attr_name = attr_name
        self.hook = hook
        self.sort = sort
        self.logger = []

    def run(self):
        """Create the output shapefile."""
        check = QFile(self.fname)
        if check.exists():
            if not QgsVectorFileWriter.deleteShapeFile(self.fname):
                raise FileDeletionError
        provider = self.layer.dataProvider()
        try:
            # XXX I have no idea why I wrote this!
            # XXX Is it useful at all with old API?
            provider.select(self.layer.pendingAllAttributesList(),
                QgsRectangle(), True, True)
        except AttributeError:
            # This fails with the 2.0 API but is not necessary.
            pass
        try:
            # 2.0 API
            crs = self.layer.crs()
        except AttributeError:
            # Old API
            crs = self.layer.srs()
        writer = QgsVectorFileWriter(self.fname, self.encoding,
            provider.fields(), self.wkb_type, crs)
        for feature in self.iter_features():
            writer.addFeature(feature)
        del writer

    def iter_features(self):
        """Iterate over features with vertices in the input layer.

        For each consecutive group of points with the same value for the
        given attribute, yields a feature (polygon o polyline depending
        on wkb_ype) with vertices in those points.

        """

        for key, points in self.iter_groups():
            try:
                feature = self.make_feature(points)
            except ValueError, e:
                message = 'Key value %s: %s' % (key.toString(), e.message)
                self.log_warning(message)
            else:
                yield feature

    def iter_groups(self):
        """Iterate over the input layer grouping by attribute.
    
        Returns an iterator of (key, points) pairs where key is the
        attribute value and points is an iterator of (QgsPoint,
        attributeMap) pairs.

        """

        points = self.iter_points()
        provider = self.layer.dataProvider()
        if self.attr_name:
            attr_idx = provider.fieldNameIndex(self.attr_name)
            if attr_idx < 0:
                raise UnknownAttributeError
            if self.sort:
                points = sorted(points,
                                key=lambda p: p[1][attr_idx].toString())
            return groupby(points, lambda p: p[1][attr_idx])
        else:
            return [(None, points)]

    def iter_points(self):
        """Iterate over the features of the input layer.
    
        Yields pairs of the form (QgsPoint, attributeMap).
        Each time a vertice is read hook is called.
    
        """

        provider = self.layer.dataProvider()
        try:
            # 2.0 API
            features = provider.getFeatures()
        except AttributeError:
            # Old API. QgsVectorDataProvider itself iterates over features.
            features = provider
        
        feature = QgsFeature()
        while(features.nextFeature(feature)):
            self.hook()
            geom = feature.geometry().asPoint()
            try:
                # 2.0 API
                attributes = feature.attributes()
            except AttributeError:
                # Old API
                attributes = feature.attributeMap()
            yield(QgsPoint(geom.x(), geom.y()), attributes)

    def make_feature(self, points):
        """Return a feature with given vertices.
    
        Vertices are given as (QgsPoint, attributeMap) pairs. Returned
        feature is polygon or polyline depending on wkb_type.
    
        """
    
        point_list = []
        for point in points:
            point_list.append(point[0])
        attributes = point[1]
        feature = QgsFeature()
        if self.wkb_type == QGis.WKBLineString:
            if len(point_list) < 2:
                raise ValueError, 'Can\'t make a polyline out of %s points' % len(point_list)
            feature.setGeometry(QgsGeometry.fromPolyline(point_list))
        elif self.wkb_type == QGis.WKBPolygon:
            if len(point_list) < 3:
                raise ValueError, 'Can\'t make a polygon out of %s points' % len(point_list)
            geom = QgsGeometry.fromPolygon([point_list])
            if geom is None:
                # This should not happen but lp:1133082 suggest it can
                # actually happen so I do this for debugging.
                fname = 'lp_1133082_debug.txt'
                with open(fname, 'w') as f:
                    f.write(repr(point_list))
            feature.setGeometry(geom)
        else:
            raise ValueError, 'Invalid geometry type: %s.' % self.wkb_type
        try:
            # 2.0 API
            feature.setAttributes(attributes)
        except AttributeError:
            # Old API
            feature.setAttributeMap(attributes)
        return feature
                                                                       
    def log_warning(self, message):
        """Log a warning."""
        self.logger.append(message)

    def get_logger(self):
        """Return the list of logged warnings."""
        return self.logger
