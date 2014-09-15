#!/usr/bin/env python
# encoding: utf-8

# Este programa revisa el header y la matriz de datos correspondiente al archivo fpC-000756-r1-0205.fit

from fits_lib import plot_image, get_fits_matrix, get_fits_header, print_header

hdr1 = get_fits_header('fpC-000756-r1-0205.fit')
img1 = get_fits_matrix('fpC-000756-r1-0205.fit')

print "\n>> ARCHIVO 1:\n"
print_header(hdr1)
plot_image(img1)
plot_image(img1,log_scale=True)



