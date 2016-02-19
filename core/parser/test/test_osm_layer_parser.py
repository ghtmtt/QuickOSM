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
from QuickOSM.core.parser.osm_layer_parser import OsmLayerParser


class TestOsmLayerParser(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_read_keys(self):
        path = '%s|points' % test_data_path('town-metadata.osm')
        vector_layer = QgsVectorLayer(path, 'test', 'ogr')
        osm_layer = OsmLayerParser(vector_layer)
        expected = [
            u'mountain_pass', u'natural', u'waterway', u'addr:postcode',
            u'ref:FR:SIREN', u'source:population', u'ref:INSEE', u'population',
            u'foot', u'bicycle', u'tourism', u'amenity', u'uic_ref',
            u'network', u'wikipedia', u'official_name', u'train',
            u'public_transport', u'operator', u'railway', u'power',
            u'traffic_sign', u'tower:type', u'historic', u'pipeline',
            u'name:wikipedia', u'fuel:octane_98', u'opening_hours',
            u'fuel:octane_95', u'fuel:diesel', u'cuisine', u'addr:housenumber',
            u'dirty', u'shop', u'recycling:glass', u'information', u'riser',
            u'url', u'description', u'recycling_type', u'crossing',
            u'map_size', u'map_type', u'atm', u'craft', u'office',
            u'traffic_calming', u'internet_access', u'addr:street',
            u'material', u'seats', u'shelter', u'bench', u'emergency',
            u'drinking_water', u'payment:electronic_purses', u'vending',
            u'payment:credit_cards', u'recycling:clothes', u'board_type',
            u'mtb', u'hiking', u'entrance', u'access', u'mhs:inscription_date',
            u'ref:mhs', u'heritage', u'heritage:operator',
            u'fire_hydrant:position', u'fire_hydrant:type', u'name:uk',
            u'climbing', u'species', u'species:fr', u'distance',
            u'ref:FR:FINESS', u'phone', u'alt_name', u'dispensing',
            u'addr:city', u'wheelchair'
        ]
        self.assertItemsEqual(expected, osm_layer.read_keys())

if __name__ == '__main__':
    suite = unittest.makeSuite(TestOsmLayerParser)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
