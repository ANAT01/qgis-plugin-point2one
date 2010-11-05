#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2010 Gregorio Díaz-Marta Mateos
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
# You should have received a copy of the GNU General Public License
# along with This program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA


"""Test module encodings."""


import os
import sys
sys.path.insert(0, os.path.join(os.pardir, 'points2one'))
import unittest

import PyQt4.QtCore as qtcore

import p2o_encodings


class Test_getEncodings(unittest.TestCase):
    """Test function getEncodings."""
    def setUp(self):
        """Run before every test in this class."""
        settings = qtcore.QSettings()
        settings.clear()

    def tearOff(self):
        """Run after every test in this class."""
        settings = qtcore.Qsettings()
        settings.clear()

    def test_getEncodings(self):
        """Basic test of function getEncodings."""
        names = p2o_encodings.getEncodings()

    def test_getDefaultEncoding(self):
        """Basic test of function getDefaultEncoding."""
        encoding = p2o_encodings.getDefaultEncoding()
        self.assertEqual(encoding, 'System')
        settings = qtcore.QSettings()
        settings.setValue('/UI/encoding', 'SomeEncoding')
        encoding = p2o_encodings.getDefaultEncoding()
        self.assertEqual(encoding, 'SomeEncoding')

    def test_setDefaultEncoding(self):
        p2o_encodings.setDefaultEncoding('NewEncoding')
        settings = qtcore.QSettings()
        encoding = settings.value('/UI/encoding').toString()
        self.assertEqual(encoding, 'NewEncoding')


if __name__ == '__main__':
    unittest.main()
