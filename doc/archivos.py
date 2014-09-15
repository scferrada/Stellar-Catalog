#!/usr/bin/env python
# encoding: utf-8

# Este programa revisa el header y la matriz de datos correspondiente a los archivos m64.fits, m83.fits, fpC-005183-u2-0406.fit

from fits_lib import plot_image, get_fits_matrix, get_fits_header, print_header

hdr1 = get_fits_header('m64.fits')
img1 = get_fits_matrix('m64.fits')

print "\n>> ARCHIVO 1:\n"
print_header(hdr1)
plot_image(img1)

hdr2 = get_fits_header('m83.fits')
img2 = get_fits_matrix('m83.fits')

print "\n>> ARCHIVO 2:\n"
print_header(hdr2)
plot_image(img2)

hdr3 = get_fits_header('fpC-005183-u2-0406.fit')
img3 = get_fits_matrix('fpC-005183-u2-0406.fit')
print "\n>> ARCHIVO 3:\n"
print_header(hdr3)
plot_image(img3)
plot_image(img3,log_scale=True)



