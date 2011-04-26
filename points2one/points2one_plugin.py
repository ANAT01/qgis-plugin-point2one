#-----------------------------------------------------------
# 
# Points2One
# Copyright (C) 2010 Pavol Kapusta
# Copyright (C) 2011 Pavol Kapusta & Goyo Diaz
# pavol.kapusta@gmail.com
# goyodiaz@gmail.com
# 
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

import os.path

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import resources
import points2one_gui


class points2one:

    def __init__(self, iface):
        self.iface = iface
        self.load_translation()

    def load_translation(self):
        ## Initialise the translation environment.
        locale = QSettings().value("locale/userLocale").toString()
        locale_path = os.path.join(os.path.dirname(__file__), 'i18n',
            ''.join(['points2one_', unicode(locale), '.qm']))
        if QFileInfo(locale_path).exists():
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


    def initGui(self):
        # create action 
        self.action = QAction(QIcon(':/plugins/points2one/points2one.png'), 'Points2One', self.iface.mainWindow())
        self.action.setWhatsThis('Tool for creating polygon or polyline from ordered points. Does not deal with rings and parts')
        QObject.connect(self.action, SIGNAL('triggered()'), self.run)
        # add toolbar button and menu item
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu('&Points2One', self.action)

    def unload(self):
        # remove the plugin menu item and icon
        self.iface.removePluginMenu('&Points2One',self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        dialog = points2one_gui.points2One(self.iface)
        dialog.exec_()
