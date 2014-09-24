__author__ = 'Sebastian'

import numpy as np

def mToCounts(m, m0, F0):
    FF0 = (10 ** ((m0 - m)/2.5))
    counts = FF0 * (10 ** 8 * F0)
    return counts


def radec_to_pixels(hdr, ra, dec):
    diff_ra = ra - float(hdr['CRVAL1'])
    diff_dec = dec - float(hdr['CRVAL2'])

    diff_ver = (diff_dec/float(hdr['CD2_1']) - diff_ra/float(hdr['CD1_1']))/(float(hdr['CD2_2'])/float(hdr['CD2_1']) - float(hdr['CD1_2'])/float(hdr['CD1_1']))
    diff_hor = (diff_dec/float(hdr['CD2_2']) - diff_ra/float(hdr['CD1_2']))/(float(hdr['CD2_1'])/float(hdr['CD2_2']) - float(hdr['CD1_1'])/float(hdr['CD1_2']))

    calc_ver = float(hdr['CRPIX2']) + diff_ver
    calc_hor = float(hdr['CRPIX1'])+ diff_hor

    return calc_ver, calc_hor


def addStar(hdu, m, ra, dec):
    count = mToCounts(m, 20, hdu[0].header['FLUX20'])
    ver, hor = radec_to_pixels(hdu[0].header, ra, dec)
    max_ver, max_hor = hdu[0].data.shape
    if 0 <= ver < max_ver and 0 <= hor < max_hor:
        print ("added %d to %d, %d" % (count, ver, hor))
        hdu[0].data[ver][hor] = count
        i = 1


def addStellarCatalog(hdu, catalog):
    stars = open(catalog, "r")
    for star in stars:
        data = star.split("\t")
        magnitude = data[3]
        ra = data[1]
        dec = data[2]
        addStar(hdu, float(magnitude), float(ra), float(dec))


def addBackground(hdu, bg):
    max_ver, max_hor = hdu[0].data.shape
    img = hdu[0].data
    for ver in range(max_ver):
        for hor in range(max_hor):
            img[ver][hor] += bg

def convolvePSF(hdu, sigma_psf):
    import scipy.ndimage as ndimage
    return ndimage.gaussian_filter(hdu[0].data, sigma = sigma_psf, order = 0)

def addNoise(hdu, sigma_noise):
    img = hdu[0].data
    img += np.random.gauss(0, sigma_noise)
    img += np.random.poisson(sigma_noise)