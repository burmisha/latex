import library

import qrcode  # https://pypi.org/project/qrcode/
import qrcode.image.svg
import qrcode.image.pure

import os

import logging
log = logging.getLogger(__name__)


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
        self.__Path = path
        self.__ErrorCorrectionLevel = correction_level

    def __MakeImage(self, data=None, method=None):
        qrCode = qrcode.QRCode(
            version=1,
            error_correction=self.__ErrorCorrectionLevel,
            box_size=5,
            border=1,
        )

        factory = self.FACTORIES[method]
        qrCode.add_data(data)
        qrCode.make()
        return qrCode.make_image(image_factory=factory)

    def Make(self, config=None, method=None, force=False):
        for link, file in config:
            filename = os.path.join(self.__Path, file)
            assert filename.endswith('.' + method.split('-')[0])
            if not os.path.exists(filename) or force:
                log.info(f'Saving {link} to {filename}')
                with open(filename, 'wb') as f:
                    self.__MakeImage(data=link, method=method).save(f)
            else:
                log.debug(f'Skipping {link} as {filename} exists')


def run(args):
    qrGenerator = Generator(
        path=library.location.udr('qrcodes'),
        correction_level=Generator.CORRECTION_LEVELS[args.correction_level],
    )
    qrGenerator.Make(
        method=args.method,
        force=args.force,
        config=[
            ('https://bit.ly/554-11T-2020', '2020-03-spring-11.png'),
            ('https://notion.so/33bad2ae867b489280e39046c97776eb', '2019-20-9A.png'),
            ('https://notion.so/f5d57ced2a224ccc9b142e21e3714a61', '2019-20-9L.png'),
            ('https://notion.so/ce257644b31d4cb5bfdef3d199446677', '2019-20-8M.png'),
            ('https://notion.so/3234ab6735f64635a34ae9550625a103', '2019-20-extra.png'),
            ('https://notion.so/8aa8591fcc00453eb19519f9faf6a1f8', '2020-summer.png'),
            ('https://notion.so/8acf3ff3b2874cefabbfa78d2db4f07e', '2020-summer-marathon.png'),
            ('https://notion.so/f28319ef853940bd88d8729ba23b1eab', '2020-21-10A.png'),
            ('https://notion.so/a7e4f5156a9b428397e3b495ffce7881', '2020-21-9M.png'),
            ('https://jamboard.google.com/d/1lI-2Lm1g38idTWHZuP8ZgnyBA_K0lyw9k8tsJaSKPHk/edit', '2021.07.09 Летний институт.png'),
            ('https://burmisha.notion.site/0c8b8d1351ee4f419df0ecabb11edf00', '2021-22-11BA.png'),
            ('https://burmisha.notion.site/d8c12e76df38443881b6524482e4d485', '2021-22-11B.png'),
            ('Нет, этот QR-код — лишь пасхалка, тут нет решений, но спасибо за попытку. На ЕГЭ так не получится.', '2021-22-no-solution.png'),
            ('https://docs.google.com/forms/d/e/1FAIpQLSdOU2U2NUijIxX4SN_Pj57_t4D1D3SHU4xplw6YlQ8xllFOLQ/viewform', '2021.09.22-11BA.png')
        ],
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
