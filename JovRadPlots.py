
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body
from astropy.coordinates import EarthLocation, AltAz
from astropy import units as u
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime
from JovRad import compute

jupal = []
jupaz = []
time = []
distance = []
io_phase = []
cml = []

t = Time("2021-02-22 07:30", scale="utc")
loc = EarthLocation(lat=50.923901*u.deg, lon=8.008528*u.deg, height=300*u.m)

#with solar_system_ephemeris.set('jpl'):
for hour in range(0, 23):
    for minute in range(0, 10, 59):
        timestr="2021-02-24 "+str(hour)+":"+str(minute)
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
        fmt = '%Y-%m-%d %H:%M'
        t_diff = (datetime.datetime.strptime(timestr, fmt)-datetime.datetime.strptime("2021-01-01 00:00", fmt)).total_seconds()/60
        pos = compute(t_diff)
        print(pos)
        distance.append(pos[0])
        io_phase.append(pos[2])
        cml.append(pos[3])

# Data for plotting
#fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
img = plt.imread("Io-CML_Phase.jpg")
fig, ax = plt.subplots(1, 2)
#ax.plot(jupaz, jupal)
#ax.plot(time, jupal)
ax[0].plot(cml, io_phase)
ax[0].set(xlabel='CML-III (°)', ylabel='Io Phase (°)', title='CML-Io Phase Plane')
ax[0].set_xlim([40, 405])
ax[0].set_ylim([-5, 365])

ax[1].plot(time, jupal)
#ax.set_yticks(np.arange(0,91,15))

ax[1].set(xlabel='az', ylabel='alt', title='Jupiter')
#ax.grid()

ax[0].imshow(img, extent=[40, 405, -5, 365])
plt.show()
