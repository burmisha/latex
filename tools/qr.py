import qrcode
import qrcode.image.svg
import qrcode.image.pure

import os

import logging
log = logging.getLogger('qr')

# handler based on https://pypi.org/project/qrcode/
class Generator(object):
    def __init__(self, path=None, force=False):
        self.__Path = path
        self.__Force = force
        # ERROR_CORRECT_L  # About 7% or less errors can be corrected
        # ERROR_CORRECT_M  # About 15% or less errors can be corrected
        # ERROR_CORRECT_Q  # About 25% or less errors can be corrected
        # ERROR_CORRECT_H  # About 30% or less errors can be corrected
        self.__ErrorCorrectionLevel = qrcode.constants.ERROR_CORRECT_L

    def __MakeImage(self, data=None, method=None):
        qrCode = qrcode.QRCode(
            version=1,
            error_correction=self.__ErrorCorrectionLevel,
            box_size=5,
            border=1,
        )

        if method == 'svg-basic':
            # Simple factory, just a set of rects.
            factory = qrcode.image.svg.SvgImage
        elif method == 'svg-fragment':
            # Fragment factory (also just a set of rects)
            factory = qrcode.image.svg.SvgFragmentImage
        elif method == 'svg':
            # Combined path factory, fixes white space that may occur when zooming
            factory = qrcode.image.svg.SvgPathImage
        elif method == 'png':
            factory = qrcode.image.pure.PymagingImage
        else:
            raise RuntimeError('Invalid method %r' % method)
        qrCode.add_data(data)
        qrCode.make()
        return qrCode.make_image(image_factory=factory)

    def MakeAll(self, path=None, method='png', force=False):
        for link, file in [
            ('https://bit.ly/554-11T-2020', '2020-03-spring-11.png'),
            ('https://notion.so/33bad2ae867b489280e39046c97776eb', '2019-20-9A.png'),
            ('https://notion.so/f5d57ced2a224ccc9b142e21e3714a61', '2019-20-9L.png'),
            ('https://notion.so/ce257644b31d4cb5bfdef3d199446677', '2019-20-8M.png'),
            ('https://notion.so/3234ab6735f64635a34ae9550625a103', '2019-20-extra.png'),
        ]:
            filename = os.path.join(path or self.__Path, file)
            assert filename.endswith(method)
            if not os.path.exists(filename) or self.__Force or force:
                log.info('Saving %s to %s', link, filename)
                with open(filename, 'w') as f:
                    self.__MakeImage(data=link, method=method).save(f)
            else:
                log.debug('Skipping %s as %s exists', link, filename)
