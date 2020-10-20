from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.coordinates import Angle
import numpy as np

def Spitzer(RA, DEC, Cone, Max):
    ##make astropy SkyCoord object
    Coo = SkyCoord(RA + ' ' + DEC, unit=(u.hourangle, u.deg))
    ##set search cone
    Cone = Angle(Cone*u.deg)
    catalogs = Vizier.get_catalogs(['J/ApJS/184/18'])
    print(catalogs)
    #names of columns to use
    V = Vizier(columns=['**', '+_r'])
     ##set limit of rows
    V.ROW_LIMIT=int(Max)
    Vizier_result = V.query_region(Coo, radius=Cone, \
                                   catalog=['J/ApJS/184/18/table4'])
    Vizier_stars = Vizier_result[0]
    Vizier_stars.remove_columns(['_r', 'Cluster', 'Seq', '_24mag', 'e_24mag',\
                                 'AKs', 'alpha', \
                                 'Cl', '_2M', 'SimbadName'])
    ##convert hms and dms to degrees
    S = SkyCoord(ra=Vizier_stars['RAJ2000'], dec=Vizier_stars['DEJ2000'], \
                  unit=(u.hourangle, u.deg))
    Vizier_stars['RAJ2000'] = np.round(S.ra.degree, 5)
    Vizier_stars['DEJ2000'] = np.round(S.dec.degree, 5)
    print('Spitzer:')
    print(Vizier_stars.info())
    print()
    return Vizier_stars

def Two_Mass(RA, DEC, Cone, Max):
    Coo = SkyCoord(RA + ' ' + DEC, unit=(u.hourangle, u.deg))
    Cone = Angle(Cone * u.deg)
    V = Vizier(columns=['RAJ2000', 'DEJ2000', \
                        'Jmag', 'e_Jmag', 'Hmag', 'e_Hmag', 'Kmag', 'e_Kmag', \
                       "+_r"])
    V.ROW_LIMIT=int(Max)
    Vizier_result = V.query_region(Coo, radius=Cone, catalog=['II/246'])
    Vizier_stars = Vizier_result[0]
    print('2MASS:')
    print(Vizier_stars.info())
    print()
    return Vizier_stars

def Gaia(RA, DEC, Cone, Max):
    Coo = SkyCoord(RA + ' ' + DEC, unit=(u.hourangle, u.deg))
    Cone = Angle(Cone * u.deg)
    V = Vizier(columns=['RAJ2000', 'DEJ2000', 'pmRA', 'pmDE', \
                        'e_pmRA', 'e_pmDE',\
                        'Plx', 'e_Plx',
                        'Gmag', 'BPmag', 'RPmag', \
                        "+_r"])
    V.ROW_LIMIT=int(Max)
    Vizier_result = V.query_region(Coo, radius=Cone, catalog=['I/345'])
    Vizier_stars = Vizier_result[0]
    print('GAIA:')
    print(Vizier_stars.info())
    print()
    return Vizier_stars


