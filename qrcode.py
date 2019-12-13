import qrcode
from PIL import Image


class QRCodeObjectNotCreated(Exception):
    pass


class QRCodeCreator:
    def __init__(self):
        self.info = None
        self.logo_path = None
        self.save_path = None
        self.img = None

    def process(self, info: str, save_path: str, logo_path: str = None):
        self.create_qrcode(info)
        if logo_path:
            self.add_logo(logo_path)
        self.save_image(save_path)

    def create_qrcode(self, info: str):
        qr_code = qrcode.QRCode(
            error_correction=qrcode.constants.ERROR_CORRECT_H,
        )
        qr_code.add_data(info)
        qr_code.make()
        self.img = qr_code.make_image().convert('RGB')
        self.info = info
        return self.img

    def add_logo(self, logo_path: str, logo_width: str = 100):
        if not self.img:
            raise QRCodeObjectNotCreated("QR object hasn't been created, Please execute QRCodeCreator.create_qrcode")

        width, _ = self.img.size

        logo = Image.open(logo_path)
        logo_natural_width, logo_natural_height = logo.size
        ratio = logo_natural_width/logo_width
        logo_height = int(logo_natural_height/ratio)
        xmin = int((width/2) - (logo_width))
        ymin = int((width/2) - (logo_height))
        xmax = int((width/2) + (logo_width))
        ymax = int((width/2) + (logo_height))
        logo = logo.resize((xmax - xmin, ymax - ymin))
        self.img.paste(logo, (xmin, ymin, xmax, ymax))

    def save_image(self, save_path: str, size: tuple = None):
        if size:
            self.img.resize(size)
        self.img.save(save_path)

