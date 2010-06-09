#-----------------------------------------------------------
# 
# Points2One
# Copyright (C) 2010 Pavol Kapusta
# pavol.kapusta@gmail.com
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
	return "Points2One"

def description():
	return "Tool for creating polygon or polyline from ordered points. Does not deal with rings and parts"

def version():
	return "0.2.5dev"
  
def qgisMinimumVersion():
	return "1.0"
	
def authorName():
	return "Pavol Kapusta & Goyo"

def classFactory( iface ):
	from points2one_plugin import points2one
	return points2one( iface )
