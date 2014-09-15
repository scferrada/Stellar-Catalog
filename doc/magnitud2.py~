#!/usr/bin/env python
# encoding: utf-8

# Este programa calcula la magnitud de un objeto corrigiendo la extinción atmosférica

import pyfits
import numpy as np

# Se abren dos archivos (uno con la imagen y otro con la tabla con datos)
arch_img   = pyfits.open('fpC-005183-u2-0406.fit')
arch_table = pyfits.open('tsField-005183-2-40-0406.fit')

# Obtengo parámetros
img           = arch_img[0].data
exptime       = float(arch_img[0].header['EXPTIME'])

kk_ugriz      = arch_table[1].data[0]['kk']
aa_ugriz      = arch_table[1].data[0]['aa']
airmass_ugriz = arch_table[1].data[0]['airmass']

kk_u          = kk_ugriz[0]
aa_u          = aa_ugriz[0]
airmass_u     = airmass_ugriz[0]

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

# Fórmula mágica: F/F0 = counts/exptime * 10 ** ( 0.4 * ( aa + kk * airmass ) )
FF0 = counts/exptime * 10 ** ( 0.4*(aa_u + kk_u * airmass_u) )
print "F/F0 = %f" % FF0

# Cálculo de magnitud
mag = -2.5 * np.log10(FF0)
print "Magnitud = %f" % mag

# Ahora se grafica la imagen
from fits_lib import plot_image
title = "Magnitud Calculada = %f\nApertura Circular en (%d,%d) con radio = %d" % (mag,pos_ver,pos_hor,radius)
plot_image(img,log_scale=True,title=title)
