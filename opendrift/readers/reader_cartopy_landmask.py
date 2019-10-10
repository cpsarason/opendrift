# This file is part of OpenDrift.
#
# OpenDrift is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2
#
# OpenDrift is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with OpenDrift.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2019, Gaute Hope, MET Norway

from opendrift.readers.basereader import BaseReader
import opendrift_landmask_data.contains as cold

import logging
import pyproj

class Reader(BaseReader):
    name = 'cartopy_landmask'
    return_block = False
    variables = ['land_binary_mask']
    proj4 = None
    crs   = None

    def __init__(self):
        """
        Initialize land mask using GSHHS dataset.
        """

        # this projection is copied from cartopy.PlateCarree()
        self.proj4 = '+ellps=WGS84 +a=57.29577951308232 +proj=eqc +lon_0=0.0 +no_defs'
        self.crs   = pyproj.CRS(self.proj4)

        super (Reader, self).__init__ ()

        # Depth
        self.z = None

        # Read and store min, max and step of x and y
        self.xmin, self.ymin, self.xmax, self.ymax = (-180, -90, 180, 90)
        self.xmin, self.ymin = self.lonlat2xy(self.xmin, self.ymin)
        self.xmax, self.ymax = self.lonlat2xy(self.xmax, self.ymax)
        self.delta_x = None
        self.delta_y = None

        # setup landmask
        self.mask = cold.Landmask()

    def zoom_map(self, buffer=0.2,
                 lonmin=None, lonmax=None, latmin=None, latmax=None):
        logging.warning('Zooming not implemented for cartopy reader: (%s to %s E), (%s to %s N)' %
                     (lonmin, lonmax, latmin, latmax) )

    def __on_land__(self, x, y):
        return self.mask.contains (x,y)

    def get_variables(self, requestedVariables, time = None,
                      x = None, y = None, z = None, block = False):
        """
        Get binary mask of whether elements are on land or not.

        Args:
            x (deg[]): longitude (decimal degrees)
            y (deg[]): latitude (decimal degrees)
            ...

        x, y is given in reader local projection.

        Returns:
            Binary mask of point x, y on land.

        """

        self.check_arguments(requestedVariables, time, x, y, z)
        return { 'land_binary_mask': self.__on_land__(x,y) }
