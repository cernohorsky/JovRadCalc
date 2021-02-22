from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, EarthLocation
from astropy.coordinates import get_body, get_moon
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy import units as u
import time;

t = Time("2019-08-11 11:00", scale="utc")
loc = EarthLocation(lat=38.2464000*u.deg, lon=274.236400*u.deg, height=0*u.m)

with solar_system_ephemeris.set('jpl'):
  moon = get_body('moon', t, loc)

altazframe = AltAz(obstime=t, location=loc, pressure=0)
moonaz=moon.transform_to(altazframe)

print(moonaz.alt.degree,moonaz.az.degree)

#https://astronomy.stackexchange.com/questions/33003/planets-positions-azimuth-altitude-api

