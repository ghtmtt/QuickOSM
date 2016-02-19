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

import pghstore
import tempfile
import re
from os.path import dirname, realpath, join, isfile, basename
from osgeo import gdal
from PyQt4.QtCore import QObject, pyqtSignal, QVariant
from qgis.core import \
    QgsVectorLayer, QgsFields, QgsField, QgsVectorFileWriter, QgsFeature

from QuickOSM.core.exceptions import \
    GeoAlgorithmExecutionException, WrongOrderOSMException
from QuickOSM.core.utilities.tools import tr
from QuickOSM.core.utilities.operating_system import get_default_encoding

OSM_TYPE = {'node': 'n', 'way': 'w', 'relation': 'r'}
WHITE_LIST = {
    'multilinestrings': None,
    'points': None,
    'lines': None,
    'multipolygons': None
}


class OsmLayerParser(QObject):

    # Signal percentage
    signalPercentage = pyqtSignal(int, name='signalPercentage')
    # Signal text
    signalText = pyqtSignal(str, name='signalText')

    def __init__(self, vector_layer):
        self.vector_layer = vector_layer
        self.geometry_type = vector_layer.wkbType()
        self.feature_count = 0
        self.keys = []

        QObject.__init__(self)

    def read_keys(self):
        fields = self.vector_layer.pendingFields()
        field_names = [field.name() for field in fields]
        other_tags_index = field_names.index('other_tags')

        features = self.vector_layer.getFeatures()
        for i, feature in enumerate(features):
            self.feature_count += 1

            attributes = feature.attributes()[other_tags_index]

            if attributes:
                h_store = pghstore.loads(attributes)
                for key in h_store:
                    if key not in self.keys:
                        self.keys.append(key)

        return self.keys
