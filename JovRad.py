import math

def compute(elmin):
    pi = 3.141593
    kr = pi / 180
    yy = 2021
    e = math.trunc(((yy - 1) / 100))
    f = 2 - e + math.trunc(e / 4)
    jd = math.trunc(365.25 * (yy - 1)) + 1721423 + f + .5
    d0 = jd - 2435108
    th = elmin / 60
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
    return [dt, s, U1, L3];