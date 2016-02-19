# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QuickOSM
 A QGIS plugin
 OSM Overpass API frontend
                             -------------------
        begin                : 2014-06-11
        copyright            : (C) 2014 by 3Liz
        email                : info at 3liz dot com
        contributor          : Etienne Trimaille
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

from re import search
from os.path import dirname, realpath, join, isfile, basename
from PyQt4.QtCore import QObject
from osgeo import gdal
from qgis.core import QgsVectorLayer
from QuickOSM.core.parser.osm_layer_parser import OsmLayerParser

OSM_LAYERS = ['points', 'lines', 'multilinestrings', 'multipolygons']


class OsmFileParser(QObject):

    def __init__(self, osm_file, osmconf_file=None, layers=None):

        self.osm_file = osm_file
        self.osmconf_file = osmconf_file
        self.layers = layers
        self.vector_layers = {}

        self.check_osm_conf_file()

        if not isfile(self.osm_file):
            print 'File  %s does not exist' % self.osm_file
        if not isfile(self.osmconf_file):
            print 'File %s does not exist' % self.osmconf_file
        if not self.layers:
            self.layers = OSM_LAYERS

        QObject.__init__(self)

    def set_ogr_config(self):
        """Set the minimum config for OGR.
        * Check if OSM Conf is defined. If not, we use the default one.
        * Set some custom settings
        """
        if not self.osmconf_file:
            current_dir = dirname(realpath(__file__))
            self.osmconf_file = join(current_dir, 'QuickOSMconf.ini')

        gdal.SetConfigOption('OSM_CONFIG_FILE', self.osmconf_file)
        gdal.SetConfigOption('OSM_USE_CUSTOM_INDEXING', 'NO')

    def check_osm_order(self):
        """Check if the OSM file starts with a node.
        OGR can't read if the layer starts with a way or a relation.

        :return The status.
        :rtype bool
        """
        with open(self.osm_file) as f:
            for line in f:
                if search(r'node', line):
                    return True
                if search(r'(way|relation)', line):
                    raise False

    def get_layer(self, layer):
        """Get a QgsVectorLayer for a specific layer in the file.

        :param layer: The layer.
        :type layer: str

        :return The validity and the vector layer if it is valid.
        :rtype list
        """
        file_name = basename(self.osm_file)
        uri = '%s|layername=%s' % (self.osm_file, layer)
        layer_name = '%s %s' % (file_name, layer)

        vector_layer = QgsVectorLayer(uri, layer_name, 'ogr')

        if vector_layer.isValid():
            return True, vector_layer
        else:
            msg = '%s is not valid.' % layer
            return False, msg

    def get_layers(self):
        """Get a list of QgsVectorLayer.

        :return The list.
        :rtype list
        """
        for layer in self.layers:
            status, vector_layer = self.get_layer(layer)
            if status:
                self.vector_layers[layer] = vector_layer

    def parse_layers(self):
        for layer, vector_layer in self.vector_layers.iteritems():
            vector_layer = OsmLayerParser()
            vector_layer.read_keys()

            if vector_layer.feature_count < 1:
                self.layers.remove()
                continue
                # remove layer from self.layers
            print 'do something with %s' % layer
