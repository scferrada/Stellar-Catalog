__author__ = 'Sebastián'

ref_pix_ra = 0
ref_pix_dec = 0
ref_pix_hor = 0
ref_pix_ver = 0
delta_ra_col = 0
delta_dec_col = 0
delta_ra_row = 0
delta_dec_row = 0

flux20 = 0
img = None

'''
Always should call this function before start adding stars from the catalog
'''
def init(hdu):
    global ref_pix_dec, ref_pix_hor, ref_pix_ra, ref_pix_ver
    global delta_dec_col, delta_dec_row, delta_ra_col, delta_ra_row
    global flux20, img
    hdr = hdu[0].header
    img = hdu[0].data
    flux20 = hdr['FLUX20']

    ref_pix_hor = float(hdr['CRPIX1']) # Column Pixel Coordinate of Ref. Pixel
    ref_pix_ver = float(hdr['CRPIX2']) # Row Pixel Coordinate of Ref. Pixel
    ref_pix_ra = float(hdr['CRVAL1']) # RA at Reference Pixel
    ref_pix_dec = float(hdr['CRVAL2']) # DEC at Reference Pixel

    delta_ra_col = float(hdr['CD1_1'])  # RA  degrees per column pixel
    delta_ra_row = float(hdr['CD1_2'])  # RA  degrees per row pixel
    delta_dec_col = float(hdr['CD2_1'])  # DEC degrees per column pixel
    delta_dec_row = float(hdr['CD2_2'])  # DEC degrees per row pixel


def mToCounts(m, m0, F0):
    FF0 = (10 ** ((m0 - m)/2.5))
    counts = FF0 * (10 ** 8 * F0)
    return counts


def radec_to_pixels(ra, dec):
    diff_ra = ra - ref_pix_ra
    diff_dec = dec - ref_pix_dec

    diff_ver = (diff_dec/delta_dec_col - diff_ra/delta_ra_col)/(delta_dec_row/delta_dec_col - delta_ra_row/delta_ra_col)
    diff_hor = (diff_dec/delta_dec_row - diff_ra/delta_ra_row)/(delta_dec_col/delta_dec_row - delta_ra_col/delta_ra_row)

    calc_ver = ref_pix_ver + diff_ver
    calc_hor = ref_pix_hor + diff_hor

    return calc_ver, calc_hor


def addStar(hdu, m, ra, dec):
    count = mToCounts(m, 20, flux20)
    ver, hor = radec_to_pixels(ra, dec)

    max_ver,max_hor = img.shape
    if 0 <= ver < max_ver and 0 <= hor < max_hor:
        img[ver][hor] = count