"""View DICOM images using Python image Library (PIL)
Usage:
>>> import pydicom
>>> from pydicom.contrib.pydicom_PIL import show_PIL
>>> ds = pydicom.read_file("filename")
>>> show_PIL(ds)
Requires Numpy:
    http://numpy.scipy.org/
and Python Imaging Library:
    http://www.pythonware.com/products/pil/
"""
# Copyright (c) 2009 Darcy Mason, Adit Panchal
# This file is part of pydicom, relased under an MIT license.
#    See the file LICENSE included with this distribution, also
#    available at https://github.com/pydicom/pydicom

# Based on image.py from pydicom version 0.9.3,
#    LUT code added by Adit Panchal
# Tested on Python 2.5.4 (32-bit) on Mac OS X 10.6
#    using numpy 1.3.0 and PIL 1.1.7b1

have_PIL = True
try:
    import PIL.Image
except ImportError:
    have_PIL = False

have_numpy = True
try:
    import numpy as np
except ImportError:
    have_numpy = False


def get_LUT_value(data, window, level):
    """Apply the RGB Look-Up Table for the given
       data and window/level value."""
    if not have_numpy:
        raise ImportError("Numpy is not available."
                          "See http://numpy.scipy.org/"
                          "to download and install")
    try:
        window = window[0]
    except TypeError:
        pass
    try:
        level = level[0]
    except TypeError:
        pass

    return np.piecewise(data,
                        [data <= (level - 0.5 - (window - 1) / 2),
                         data > (level - 0.5 + (window - 1) / 2)],
                        [0, 255, lambda data: ((data - (level - 0.5)) /
                         (window - 1) + 0.5) * (255 - 0)])


def get_PIL_image(dataset):
    """Get Image object from Python Imaging Library(PIL)"""
    if not have_PIL:
        raise ImportError("Python Imaging Library is not available. "
                          "See http://www.pythonware.com/products/pil/ "
                          "to download and install")

    if ('PixelData' not in dataset):
        raise TypeError("Cannot show image -- DICOM dataset does not have "
                        "pixel data")

    bits = dataset.BitsAllocated
    samples = dataset.SamplesPerPixel
    if bits == 8 and samples == 1:
        mode = "L"
    elif bits == 8 and samples == 3:
        mode = "RGB"
    elif bits == 16:
        # not sure about this -- PIL source says is 'experimental'
        # and no documentation. Also, should bytes swap depending
        # on endian of file and system??
        mode = "I;16"
    else:
        raise TypeError("Don't know PIL mode for %d BitsAllocated "
                            "and %d SamplesPerPixel" % (bits, samples))

    # PIL size = (width, height)
    size = (dataset.Columns, dataset.Rows)

    # can only apply LUT if these window info exists
    if ('WindowWidth' not in dataset) or ('WindowCenter' not in dataset):
        image = dataset.pixel_array
    else:
        image = get_LUT_value(dataset.pixel_array, dataset.WindowWidth,
                              dataset.WindowCenter)

    image = PIL.Image.frombytes(mode, size, image.tobytes(), "raw", mode, 0, 1)
    if mode == "I;16":
        image = image.convert("L")
    return image

def show_PIL(dataset):
    """Display an image using the Python Imaging Library (PIL)"""
    im = get_PIL_image(dataset)
    im.show()
