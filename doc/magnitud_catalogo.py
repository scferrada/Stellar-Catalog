#!/usr/bin/env python
# encoding: utf-8

# Este programa calcula automáticamente la magnitud de un grupo de objetos presentes en una imagen (fpC-000756-r1-0205.fit)
# utilizando la información contenida en un catálogo (drObj-000756-1-44-0205.fit)

from flux20_lib import *
import pyfits
import numpy as np

arch   = pyfits.open('fpC-000756-r1-0205.fit')
hdr    = arch[0].header
img    = arch[0].data
flux20 = hdr['FLUX20']

ref_pix_hor   = float(hdr['CRPIX1']) # Column Pixel Coordinate of Ref. Pixel  
ref_pix_ver   = float(hdr['CRPIX2']) # Row Pixel Coordinate of Ref. Pixel
ref_pix_ra    = float(hdr['CRVAL1']) # RA at Reference Pixel
ref_pix_dec   = float(hdr['CRVAL2']) # DEC at Reference Pixel

delta_ra_col  = float(hdr['CD1_1'])  # RA  degrees per column pixel
delta_ra_row  = float(hdr['CD1_2'])  # RA  degrees per row pixel
delta_dec_col = float(hdr['CD2_1'])  # DEC degrees per column pixel
delta_dec_row = float(hdr['CD2_2'])  # DEC degrees per row pixel

# De pixeles (ver,hor) a (ra,dec)
def pix_2_ra_dec(ver,hor):

    diff_ver = ver - ref_pix_ver
    diff_hor = hor - ref_pix_hor

    diff_ra  = (diff_hor * delta_ra_col) + diff_ver * delta_ra_row
    diff_dec =  diff_hor * delta_dec_col  + (diff_ver * delta_dec_row)

    calc_ra  = ref_pix_ra  + diff_ra
    calc_dec = ref_pix_dec + diff_dec

    return (calc_ra,calc_dec)

# De (ra,dec) a pixeles (ver,hor)
def ra_dec_2_pix(ra,dec):

    diff_ra  = ra  - ref_pix_ra
    diff_dec = dec - ref_pix_dec

    diff_ver = (diff_dec/delta_dec_col - diff_ra/delta_ra_col)/(delta_dec_row/delta_dec_col - delta_ra_row/delta_ra_col)
    diff_hor = (diff_dec/delta_dec_row - diff_ra/delta_ra_row)/(delta_dec_col/delta_dec_row - delta_ra_col/delta_ra_row)

    calc_ver = ref_pix_ver + diff_ver
    calc_hor = ref_pix_hor + diff_hor

    return (calc_ver,calc_hor)

# Cálculo de magnitud con flux20
def magnitude_flux20(pos_ver,pos_hor,radius):

    counts = 0.0
    ver_max,hor_max = img.shape
    for ver in range(pos_ver-radius,pos_ver+radius+1):
        for hor in range(pos_hor-radius,pos_hor+radius+1):
            r2 = radius**2
            if (ver-pos_ver)**2 + (hor-pos_hor)**2 <= r2 and 0 <= ver < ver_max and 0 <= hor < hor_max:
               counts += img[ver][hor]

    mag = magnitud_con_flux20(counts,flux20)
    return mag

# Marcar objetos en la imagen
def mark_objects(pos_ver,pos_hor):

   max_value = np.max(img)
   coord_ver = range(pos_ver-3,pos_ver+3+1) + [pos_ver] * 3            + [pos_ver] * 3
   coord_hor = [pos_hor]*7                  + range(pos_hor-3,pos_hor) + range(pos_hor+1,pos_hor+3+1)

   max_ver,max_hor = img.shape

   for i in range(len(coord_ver)):
       ver = coord_ver[i]
       hor = coord_hor[i]
       if 0 <= ver < max_ver and 0 <= hor < max_hor:
          img[ver][hor] = max_value

# Lista de tuplas (ra,dec) para los objetos del catálogo
def coordinates_from_catalog():

    resp = []
    ctlg = pyfits.open('drObj-000756-1-44-0205.fit')
    for table in ctlg[1].data:
        ra  = table['ra']
        dec = table['dec']
        resp.append((ra,dec))
    ctlg.close()
    return resp

print "Cálculo automático de magnitudes"

# Algunos parámetros
max_ver,max_hor = img.shape
radius          = 5 # pixels
i               = 1

# Cálculo de magnitudes
for ra,dec in coordinates_from_catalog():

    ver,hor   = ra_dec_2_pix(ra,dec)
    ver_int   = int(np.round(ver))
    hor_int   = int(np.round(hor))
    magnitude = magnitude_flux20(ver_int,hor_int,radius)
    print ">> Objeto N°%d:\n\n\t(ra,dec)\t= (%f,%f)\n\t(ver,hor)\t= (%d,%d)\n\tmagnitud\t= %f\n" % (i,ra,dec,ver_int,hor_int,magnitude)
    i += 1

print "Ahora marcamos los objetos del catálogo sobre la imagen ... \n"

# Marcamos los objetos para visualizarlos
for ra,dec in coordinates_from_catalog():

    ver,hor   = ra_dec_2_pix(ra,dec)
    ver_int   = int(np.round(ver))
    hor_int   = int(np.round(hor))
    mark_objects(ver_int,hor_int)

print "Listo, los objetos están marcados con un signo + !!\n"

# Ahora graficamos
from fits_lib import plot_image
plot_image(img,log_scale=True,title=r'$\mathrm{\mathbb{Objetos\,del\,cat\acute{a}logo\,marcados\,con\,signo\,\plus}}$')

