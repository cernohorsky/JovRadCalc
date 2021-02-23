#!usrbinenv python

import math
import datetime
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris
from astropy.coordinates import get_body
from astropy.coordinates import EarthLocation, AltAz
from astropy import units as u

def jupalt(t):
    #t = Time("2021-02-22 07:30", scale="utc")
    t = Time(t, scale="utc")
    loc = EarthLocation(lat=50.923901*u.deg, lon=8.008528*u.deg, height=300*u.m)
    with solar_system_ephemeris.set('builtin'):
        jupiter = get_body('jupiter', t, loc)

    altazframe = AltAz(obstime=t, location=loc, pressure=0)
    jupiter_position=jupiter.transform_to(altazframe)

    return jupiter_position.alt.degree

def compute(elmin):
    th=elmin/60
    d = d0 + (th / 24)
    v = (157.0456 + .0011159 * d) % 360
    m = (357.2148 + .9856003 * d) % 360
    n = (94.3455 + .0830853 * d + .33 * math.sin(kr * v)) % 360
    j = (351.4266 + .9025179 * d - .33 * math.sin(kr * v)) % 360
    a = 1.916 * math.sin(kr * m) + .02 * math.sin(kr * 2 * m)
    b = 5.552 * math.sin(kr * n) + .167 * math.sin(kr * 2 * n)
    k = j + a - b
    r = 1.00014 - .01672 * math.cos(kr * m) - .00014 * math.cos(kr * 2 * m)
    re = 5.20867 - .25192 * math.cos(kr * n) - .0061 * math.cos(kr * 2 * n)
    dt = math.sqrt(re * re + r * r - 2 * re * r * math.cos(kr * k))
    sp = r * math.sin(kr * k) / dt
    ps = sp / .017452
    dl = d - dt / 173
    pb = ps - b
    xi = 150.4529 * math.trunc((dl)) + 870.4529 * (dl - math.trunc((dl)))
    L3 = (274.319 + pb + xi + .01016 * 51) % 360
    U1 = 101.5265 + 203.405863 * dl + pb
    U2 = 67.81114 + 101.291632 * dl + pb
    z = (2 * (U1 - U2)) % 360
    U1 = U1 + .472 * math.sin(kr * z)
    U1 = (U1 + 180) % 360

    s = ""
    if L3 < 255 and L3 > 200 and U1 < 250 and U1 > 220:
        s = "Io-A"
    if L3 < 180 and L3 > 105 and U1 < 100 and U1 > 80:
        s = "Io-B"
    if L3 < 350 and L3 > 300 and U1 < 250 and U1 > 230:
        s = "Io-C"
    return [dt,s];


print('Program to flag Jovian Decametric windows')
month = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
week = 42.46360
pi = 3.141593
kr = pi / 180
num1 = open('jovrad.csv', 'w')
#yy = int(input(("Year for which predictions are required ")))
yy=2021
e = math.trunc(((yy-1) / 100))
f = 2 - e + math.trunc(e/4)
jd = math.trunc(365.25 * (yy - 1)) + 1721423 + f + .5
d0 = jd - 2435108
incr = 0
dmax = 0
tx = 0
ty = 0
yyly = 0
yylc = 0
if yy / 400 - math.trunc((yy / 400)) == 0:
    incr = 1
    print("in if-1")
yyly = yy / 4 - math.trunc((yy / 4))
yylc = yy / 100 - math.trunc((yy / 100))
if yyly == 0 and yylc != 0:
    print("in if-2")
    incr = 1
ty = 59 + incr
dmax = 365 + incr
tx = ty + .5
num1.write("**************************************************\n")
pout =     "JOVIAN IO-DECAMETRIC EMISSION PREDICTIONS FOR "  + str(yy) + "\n"
num1.write(pout)
num1.write("**************************************************\n")
num1.write("\n")
num1.write("Date       Begin End   Dist(AU) Source")
num1.write("\n")
elmin = 0

while int(elmin / 60 / 24) + 1 <= dmax:
    compute_output=compute(elmin)
    s=compute_output[1]
    if s != "":
        dy = math.trunc((elmin / 60 / 24)) + 1
        '''
        h = th - (dy - 1) * 24
        if(dy > th):
            m = math.trunc((dy - tx) / 30.6) + 3
            da = dy - ty - math.trunc((m - 3) * 30.6 + .5)
        else:
            m = math.trunc((dy - 1) / 31) + 1
            da = dy - (m - 1) * 31
        mn = month[(m-1)]
        #mn = month[(m-1)*3+1:(m-1)*3-1+3]
        '''
        emi_start = datetime.datetime(2021,1,1)+datetime.timedelta(minutes=elmin)
        #outstring = "%i  %s  %i  %5.3f  %5.3f  %5.3f  %5.3f  %s\n" % (dy, mn, da, h, U1, L3, dt, s)
        #outstring = "%i  %s  %5.3f  %5.3f  %5.3f  %s\n" % (dy, date, U1, L3, dt, s)
        x=s
        while x!= "":
            x=compute(elmin)
            x=x[1]
            elmin = elmin + 1

        emi_stop = datetime.datetime(2021,1,1)+datetime.timedelta(minutes=elmin)
        if jupalt(str(emi_start))>10 or jupalt(str(emi_stop))>10:
            print(emi_stop-emi_start)
            outstring = "%s %s %5.3f %s\n" % (str(emi_start)[0:16], str(emi_stop)[11:16], compute_output[0], "   "+s)
            num1.write(outstring)
            print(outstring)

    elmin = elmin + 1

num1.close()
print("Program Complete  - results in file jovrad.csv")
