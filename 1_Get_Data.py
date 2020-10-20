'''
Receives catalogs from the vizier. Compares objects by coordinates.
Saves matching objects to a .dat file.
'''

from astropy.coordinates import SkyCoord
from astropy import units as u
import numpy as np
from Visier_query import Wise, Two_Mass, Gaia

import warnings
warnings.simplefilter("ignore")

##set here query parameters
Name = 'IC348'      #set name!
RA = '03 44 34'     #format: hh mm ss
DEC = '+32 09 48 '    #format: dd mm ss
Cone = 0.16          #cone radius, degrees
Max = 100000        #max number of objects


W = Wise(RA, DEC, Cone, Max)
##TM = Two_Mass(RA, DEC, Cone, Max) ##2MASS sources are included to WISE catalog
G = Gaia(RA, DEC, Cone, Max)

##set max separation for matching (arcsec)
max_sep = 2

##to find the closest coordinates in a catalog to a desired set of other sources
sources = SkyCoord(ra=W['RAJ2000'], dec=W['DEJ2000']) ##set WISE as sources
catalog = SkyCoord(ra=G['RAJ2000'], dec=G['DEJ2000']) ##set GAIA as catalog
idx, d2d, d3d = sources.match_to_catalog_sky(catalog)

##select from catalog only items with separation less than max_sep
idx = idx[d2d < max_sep*u.arcsec]
print('Matched sources:', idx.shape[0])

##create new table for matched sources
##copy matched sources
Matched = W[d2d < max_sep*u.arcsec]
##rename coordinate columns
Matched.rename_columns(('RAJ2000', 'DEJ2000'), ('W_RAJ2000', 'W_DEJ2000'))
##add info for matched sources from catalog
Matched.add_columns((G['RAJ2000'][idx], G['DEJ2000'][idx]), indexes=(0,1))
##add separation
Matched.add_column(np.round(d2d[d2d < max_sep*u.arcsec]*3600., 2), name = 'Separation', index=4)
Matched.add_columns((G['pmRA'][idx], G['pmDE'][idx], \
                     G['e_pmRA'][idx], G['e_pmDE'][idx], \
                     G['Plx'][idx], G['e_Plx'][idx], \
                     G['Gmag'][idx], G['BPmag'][idx], G['RPmag'][idx]))
print(Matched.info())

##save table Matched to local file
Matched.write(Name+'.dat', format = 'ascii', delimiter='\t', overwrite=True)



