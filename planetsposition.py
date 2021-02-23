
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body
from astropy.coordinates import EarthLocation, AltAz
from astropy import units as u
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
jupal=[]
jupaz=[]
time=[]

t = Time("2021-02-22 07:30", scale="utc")
loc = EarthLocation(lat=50.923901*u.deg, lon=8.008528*u.deg, height=300*u.m)

#with solar_system_ephemeris.set('jpl'):
for hour in range(0, 23):
    for minute in range(0, 10, 59):
        timestr="2021-02-22 "+str(hour)+":"+str(minute)
        print(timestr)
        t = Time(timestr, scale="utc")

        with solar_system_ephemeris.set('builtin'):
            jupiter = get_body('jupiter', t, loc)

        altazframe = AltAz(obstime=t, location=loc, pressure=0)
        jupiter_position=jupiter.transform_to(altazframe)

        #print(jupiter_position.alt.degree, jupiter_position.az.degree)
        if jupiter_position.alt.degree > 0:
            jupal.append(jupiter_position.alt.degree)
            jupaz.append(jupiter_position.az.degree)
            time.append(timestr)
# Data for plotting
#fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
fig, ax = plt.subplots()

#ax.plot(jupaz, jupal)
ax.plot(time,jupal)

#ax.set_yticks(np.arange(0,91,15))

ax.set(xlabel='az', ylabel='alt',
       title='Jupiter')
ax.grid()

plt.show()