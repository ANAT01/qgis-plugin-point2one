#-----------------------------------------------------------
# 
# Points2One
# Copyright (C) 2010 Pavol Kapusta <pavol.kapusta@gmail.com>
# Copyright (C) 2010, 2013 Goyo <goyodiaz@gmail.com>
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

def name():
	return 'Points2One'

def description():
	return 'Create lines and polygons from vertices.'

def version():
	return '0.2.14dev'

def icon():
	return 'points2one.png'

def qgisMinimumVersion():
	return '1.9'

def qgisMaximumVersion():
	return '2.9'

def author():
	return 'Pavol Kapusta'

def email():
	return 'goyodiaz@gmail.com'

def category():
  return 'Vector'

def classFactory(iface):
	from points2one_plugin import points2one
	return points2one(iface)
