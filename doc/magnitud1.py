#!/usr/bin/env python
# encoding: utf-8

# Este programa calcula la magnitud de un objeto utilizando el parámetro FLUX20

from flux20_lib import *
import pyfits
import numpy as np

# Obtengo parámetros
arch   = pyfits.open('fpC-005183-u2-0406.fit')
hdr    = arch[0].header
img    = arch[0].data
flux20 = hdr['FLUX20']

# Suma de cuentas en un apertura circular
pos_ver = 650
pos_hor = 750
radius  = 50
counts  = 0.0
max_val = np.max(img)

for ver in range(pos_ver-radius,pos_ver+radius+1):
    for hor in range(pos_hor-radius,pos_hor+radius+1):
        r2 = radius**2
        if (ver-pos_ver)**2 + (hor-pos_hor)**2 <= r2: # Se suman las cuentas dentro de la apertura
           counts += img[ver][hor]
        if 0.98*r2 <= (ver-pos_ver)**2 + (hor-pos_hor)**2 <= 1.02*r2: # Se "pintan" los pixeles del borde para dibujar la apertura sobre la imagen
           img[ver][hor] = max_val

mag = magnitud_con_flux20(counts,flux20)
print "Magnitud = %f" % mag

# Ahora se grafica la imagen
from fits_lib import plot_image
title = "Magnitud Calculada = %f\nApertura Circular en (%d,%d) con radio = %d" % (mag,pos_ver,pos_hor,radius)
plot_image(img,log_scale=True,title=title)
