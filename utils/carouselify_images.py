""" XXX: Helper script ... """

from os.path import basename
from PIL import Image

ASPECT_RATIOS = (1.5, 2, 2.5)
PREFIX = '/assets/img/'
STYLE_MAPPING = {
    '1.5': 'visible-sm',
    '2': 'visible-md',
    '2.5': 'visible-lg',
}


def distance(a, b):
    return (a-b) * (a-b)


def save_image(image, aspect_ratio, filename, format):
    """ Save the image with the aspect_ratio details in the name. """

    from os.path import splitext

    name, ext = splitext(filename)
    outfile = ''.join([name, '-', str(aspect_ratio), ext])

    image.save(outfile, format)

    return outfile


def get_image_aspect_ratio(image):
    """ Return the aspect ratio of the image. """

    width, height = image.size
    ratio = float(width)/height

    d = 1000000
    aspect_ratio = ASPECT_RATIOS[0]

    for r in ASPECT_RATIOS:
        d_ = distance(ratio, r)
        if d_ <= d:
            aspect_ratio = r
            d = d_

    return aspect_ratio


def convert_to(image, current_aspect_ratio, new_aspect_ratio, offset):
    """ Convert the image to the given aspect ratio. """

    crop_factor = current_aspect_ratio / new_aspect_ratio

    if crop_factor != 1.0:
        width, height = image.size
        top = int(height * (1-crop_factor) * (1 + offset) / 2.)
        bot = int(height * crop_factor) + top
        area = image.crop((0, top, width, bot))
    else:
        area = image.copy()

    return save_image(area, new_aspect_ratio, image.filename, image.format)


def carouselify_image(image_path, offset=0):
    """ Make the image usable in a carousel. """

    image = Image.open(image_path)
    aspect_ratio = get_image_aspect_ratio(image)

    for r in ASPECT_RATIOS:
        filename = basename(convert_to(image, aspect_ratio, r, offset))
        path = PREFIX + filename
        print('<img src="%s" class="%s">' % (path, STYLE_MAPPING[str(r)]))

if __name__ == '__main__':
    import sys

    if len(sys.argv) < 2:
        print('Usage: %s path/to/image [offset]' % sys.argv[0])
        print('    offset: the offset of the box from center. -1 is top.')

    else:

        offset = float(sys.argv[2]) if len(sys.argv) == 3 else 0
        if offset < -1:
            offset = -1
        elif offset > 1:
            offset = 1

        carouselify_image(sys.argv[1], offset)
