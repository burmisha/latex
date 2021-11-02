import library.files
import library.location

import qrcode  # https://pypi.org/project/qrcode/
import qrcode.image.svg
import qrcode.image.pure

import os

import logging
log = logging.getLogger(__name__)

from library.logging import colorize_json, cm, color


class Generator:
    DEFAULT_CORRECTION_LEVEL = 7
    CORRECTION_LEVELS = {
        7: qrcode.constants.ERROR_CORRECT_L,  # About 7% or less errors can be corrected
        15: qrcode.constants.ERROR_CORRECT_M,  # About 15% or less errors can be corrected
        25: qrcode.constants.ERROR_CORRECT_Q,  # About 25% or less errors can be corrected
        30: qrcode.constants.ERROR_CORRECT_H,  # About 30% or less errors can be corrected
    }

    DEFAULT_FACTORY = 'png'
    FACTORIES =  {
        'png': qrcode.image.pure.PymagingImage,
        'svg-basic': qrcode.image.svg.SvgImage,  # Simple factory, just a set of rects.
        'svg-fragment': qrcode.image.svg.SvgFragmentImage,  # Fragment factory (also just a set of rects)
        'svg': qrcode.image.svg.SvgPathImage,  # Combined path factory, fixes white space that may occur when zooming
    }

    def __init__(self, path=None, correction_level=None):
        self.__path = path
        self.__error_correction_level = correction_level

    def __MakeImage(self, data=None, method=None):
        qrCode = qrcode.QRCode(
            version=1,
            error_correction=self.__error_correction_level,
            box_size=5,
            border=1,
        )

        factory = self.FACTORIES[method]
        qrCode.add_data(data)
        qrCode.make()
        return qrCode.make_image(image_factory=factory)

    def Make(self, config=None, method=None, force=False):
        log.info(f'Destination dir: {cm(self.__path, color=color.Green)}')
        for link, file in config:
            filename = os.path.join(self.__path, file)
            assert filename.endswith('.' + method.split('-')[0])
            if not os.path.exists(filename) or force:
                log.info(f'Saving {link} to {cm(file, color=color.Green)}')
                with open(filename, 'wb') as f:
                    self.__MakeImage(data=link, method=method).save(f)
            else:
                log.debug(f'Skipping {link} as {cm(file, color=color.Green)} exists')


def run(args):
    qrGenerator = Generator(
        path=library.location.udr('qrcodes'),
        correction_level=Generator.CORRECTION_LEVELS[args.correction_level],
    )

    qr_config = library.files.load_yaml_data('qr.yaml')

    qrGenerator.Make(
        method=args.method,
        force=args.force,
        config=sorted(qr_config.items()),
    )


def populate_parser(parser):
    parser.add_argument(
        '-f',
        '--force',
        help='Force updates',
        action='store_true',
    )
    parser.add_argument(
        '-l',
        '--correction-level',
        help='How many errors could be corrected',
        choices=sorted(Generator.CORRECTION_LEVELS),
        default=Generator.DEFAULT_CORRECTION_LEVEL,
    )
    parser.add_argument(
        '-m',
        '--method',
        help='Result format',
        choices=sorted(Generator.FACTORIES),
        default=Generator.DEFAULT_FACTORY,
    )
    parser.set_defaults(func=run)
