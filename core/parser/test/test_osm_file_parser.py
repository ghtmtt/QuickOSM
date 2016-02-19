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

import unittest

# This import is to enable SIP API V2
# noinspection PyUnresolvedReferences
import qgis  # pylint: disable=unused-import
from test.utilities import get_qgis_app, test_data_path
QGIS_APP, CANVAS, IFACE, PARENT = get_qgis_app()

from qgis.core import QgsVectorLayer
from QuickOSM.core.parser.osm_file_parser import OsmFileParser


class TestOsmFileParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_check_osm_order(self):
        """Test if we can detect the OSM order in a file."""
        good_file = test_data_path('town-metadata.osm')
        osm_file_parser = OsmFileParser(good_file)
        msg = 'Wrong OSM order in the file.'
        self.assertTrue(osm_file_parser.check_osm_order(), msg)

    def test_get_layer(self):
        """Test if we can get a valid layer."""
        good_file = test_data_path('town-metadata.osm')
        osm_file_parser = OsmFileParser(good_file)
        valid, vector_layer = osm_file_parser.get_layer('points')
        self.assertTrue(valid)
        self.assertTrue(isinstance(vector_layer, QgsVectorLayer))

        valid, vector_layer = osm_file_parser.get_layer('fake')
        self.assertFalse(valid)
        self.assertTrue(isinstance(vector_layer, str))

    def test_get_layers(self):
        """Test if we can get every valid layers."""
        good_file = test_data_path('town-metadata.osm')
        osm_file_parser = OsmFileParser(good_file)
        layers = osm_file_parser.get_layers()
        self.assertTrue(isinstance(layers, dict))
        self.assertTrue(len(layers), 4)

if __name__ == '__main__':
    suite = unittest.makeSuite(TestOsmFileParser)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
