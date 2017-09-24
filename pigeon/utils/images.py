"""
Utilitary module to manipulate images
"""
import logging
import uuid
import warnings
from PIL import Image as PILImage
from PIL import ImageOps
from pilkit.utils import save_image



def _read_image(file_path):
    with warnings.catch_warnings(record=True) as caught_warnings:
        img = PILImage.open(file_path)

    for warning in caught_warnings:
        if warning.category == PILImage.DecompressionBombWarning:
            logger = logging.getLogger(__name__)
            logger.info('PILImage reported a possible DecompressionBomb'
                        ' for file %s', file_path)
        else:
            warnings.showwarning(warning.message, warning.category,
                                 warning.filename, warning.lineno)
    return img


def generate_thumbnail(source, outname, box, fit=True, options=None):
    """Create a thumbnail image."""
    logger = logging.getLogger(__name__)
    img = _read_image(source)
    original_format = img.format

    if fit:
        img = ImageOps.fit(img, box, PILImage.ANTIALIAS)
    else:
        img.thumbnail(box, PILImage.ANTIALIAS)

    outformat = img.format or original_format or 'JPEG'
    logger.debug(u'Save thumnail image: %s (%s)', outname, outformat)
    save_image(img, outname, outformat, options=options, autoconvert=True)


def set_measure_thumbnail(measure):
    """Set thumbnail image for measure"""
    if measure.measure_image:
        thumb_name = measure.measure_image.url + str(uuid.uuid4())
        generate_thumbnail(measure.measure_image.url, thumb_name, (200, 200))
        measure.thumbnail = thumb_name
        measure.save()
