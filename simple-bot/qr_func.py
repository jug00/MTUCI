import qrcode
import string, random


def qr_create(data, img_name):
    img = qrcode.make(data)
    img.save(img_name)
    return img


def random_pass():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = random.randint(10, 16)
    return ''.join(random.choice(chars) for x in range(size))
