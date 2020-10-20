from astroquery.vizier import Vizier
from astropy.coordinates import SkyCoord
from astropy import units as u
from astropy.coordinates import Angle

def Wise(RA, DEC, Cone, Max):
    ##make astropy SkyCoord object
    Coo = SkyCoord(RA + ' ' + DEC, unit=(u.hourangle, u.deg))
    ##set search cone
    Cone = Angle(Cone * u.deg)
    V = Vizier(columns=['RAJ2000', 'DEJ2000', \
                        'W1mag', 'e_W1mag', 'W2mag', 'e_W2mag', \
                        'W3mag', 'e_W3mag', 'W4mag', 'e_W4mag', \
                        'Jmag', 'e_Jmag', 'Hmag', 'e_Hmag', 'Kmag', 'e_Kmag', \
                        "+_r"])
    ##set limit of rows
    V.ROW_LIMIT=int(Max)
    Vizier_result = V.query_region(Coo, radius=Cone, catalog=['II/328'])
    Vizier_stars = Vizier_result[0]
    print('WISE:')
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
